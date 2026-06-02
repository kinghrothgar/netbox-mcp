"""Small reusable helpers to reduce repetition across tools.

This module concentrates token-reduction behaviour for all NetBox search
and detail tools. Three knobs are exposed via the standard `args` dict:

* ``brief`` (search only, default ``True``) - use NetBox's ``brief=true``
  representation, which returns ``{id, url, display, ...}`` instead of the
  full object. The LLM can pass ``brief=False`` to opt into full objects in
  one round-trip when it really needs them.
* ``fields`` / ``exclude`` - forwarded to NetBox as ``?fields=`` and
  ``?exclude=`` respectively. Accept either a comma-separated string or a
  list. Lets the LLM project arbitrary subsets without an extra tool.
* ``raw`` (detail only, default ``False``) - when ``False`` we strip a
  small set of known-noisy keys (empty ``custom_fields``/``tags``,
  ``display_url``, ``created``, ``last_updated``) from the returned
  object. Pass ``raw=True`` to disable.

In addition, ``limit`` is hard-capped at :data:`MAX_LIMIT` (100) to prevent
pathological-size responses, and ``offset`` is honoured so the LLM can
paginate. Search tools return ``{"count": int, "results": [...]}`` instead
of a bare list so the LLM knows whether to refine filters or page through.
"""

from typing import Any, Dict, Iterable, List, Optional, Union

from .client import NETBOX_TOKEN, NETBOX_URL, NetBoxClient

# Hard ceiling for `limit` to guard against accidental large dumps.
MAX_LIMIT = 100

# Keys stripped from detail responses unless the caller passes raw=True.
# Empty values for `custom_fields` and `tags` are dropped; the others are
# always dropped because they're rarely useful to an LLM and are verbose.
_NOISY_DETAIL_KEYS = ("display_url", "created", "last_updated")


def _coerce_csv(value: Union[str, Iterable[str], None]) -> Optional[str]:
    """Normalise ``fields``/``exclude`` to a comma-separated string."""
    if value is None:
        return None
    if isinstance(value, str):
        return value
    try:
        return ",".join(str(v) for v in value)
    except TypeError:
        return str(value)


def _apply_common_args(args: Dict[str, Any], params: Dict[str, Any]) -> None:
    """Pull ``fields``/``exclude``/``offset`` out of args into NetBox params."""
    fields = _coerce_csv(args.get("fields"))
    if fields:
        params["fields"] = fields
    exclude = _coerce_csv(args.get("exclude"))
    if exclude:
        params["exclude"] = exclude
    if "offset" in args:
        params["offset"] = args["offset"]


def _capped_limit(args: Dict[str, Any], default_limit: int) -> int:
    """Return ``args['limit']`` capped at :data:`MAX_LIMIT`."""
    try:
        requested = int(args.get("limit", default_limit))
    except (TypeError, ValueError):
        requested = default_limit
    if requested < 1:
        requested = default_limit
    return min(requested, MAX_LIMIT)


def _build_params(
    args: Dict[str, Any],
    mappings: Dict[str, str],
    default_limit: int = 10,
) -> Dict[str, Any]:
    """Build query params for NetBox from incoming args using a mapping.

    mappings: dict of incoming arg name -> NetBox query param name
    """
    params: Dict[str, Any] = {"limit": _capped_limit(args, default_limit)}
    for incoming_name, query_name in mappings.items():
        if incoming_name in args:
            params[query_name] = args[incoming_name]
    _apply_common_args(args, params)
    return params


async def _search(
    endpoint: str,
    args: Dict[str, Any],
    mappings: Dict[str, str],
    default_limit: int = 10,
) -> Dict[str, Any]:
    """Search a NetBox list endpoint.

    Defaults to ``brief=true`` for compact representations. Pass
    ``brief=False`` in ``args`` to fetch full objects. Returns
    ``{"count": int, "results": [...]}``; ``count`` is the total NetBox
    result count (not the page size) so the LLM can decide whether to
    refine filters or paginate via ``offset``.
    """
    params = _build_params(args, mappings, default_limit)
    # Default to brief unless caller explicitly opts out. NetBox accepts
    # `brief=true` and returns id/url/display plus a handful of identifying
    # fields per object, dropping nested expansions entirely.
    if args.get("brief", True):
        params["brief"] = "true"

    netbox_client = NetBoxClient(NETBOX_URL, NETBOX_TOKEN)
    result = await netbox_client.get(endpoint, params)
    return {
        "count": result.get("count", 0),
        "results": result.get("results", []),
    }


def _compact_detail(obj: Dict[str, Any]) -> Dict[str, Any]:
    """Strip known-noisy keys from a NetBox detail object."""
    out = {k: v for k, v in obj.items() if k not in _NOISY_DETAIL_KEYS}
    # Drop empty custom_fields/tags - they're verbose and add no signal.
    cf = out.get("custom_fields")
    if isinstance(cf, dict) and not cf:
        out.pop("custom_fields", None)
    tags = out.get("tags")
    if isinstance(tags, list) and not tags:
        out.pop("tags", None)
    return out


async def _get_detail(endpoint_base: str, id_value: Any, args: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    """Fetch a single NetBox object by ID.

    Honours ``fields`` and ``exclude`` from ``args`` for server-side
    projection. Strips a small set of noisy keys from the result unless
    ``args['raw']`` is truthy.
    """
    args = args or {}
    params: Dict[str, Any] = {}
    _apply_common_args(args, params)
    # offset has no meaning on detail endpoints; drop it silently.
    params.pop("offset", None)

    netbox_client = NetBoxClient(NETBOX_URL, NETBOX_TOKEN)
    try:
        result = await netbox_client.get(
            f"{endpoint_base}{id_value}/",
            params or None,
        )
        if not isinstance(result, dict):
            return []
        if args.get("raw"):
            return [result]
        return [_compact_detail(result)]
    except Exception:
        return []


async def _get_list(endpoint: str, args: Dict[str, Any], default_limit: int = 10) -> List[Dict[str, Any]]:
    """Fetch an endpoint that returns a JSON list directly (no `results` envelope).

    Used for NetBox sub-resources like `available-ips`, `available-prefixes`,
    `available-asns`, `available-vlans`, which return a bare list and have
    no notion of a NetBox-level count or brief representation.
    """
    params: Dict[str, Any] = {"limit": _capped_limit(args, default_limit)}
    _apply_common_args(args, params)
    netbox_client = NetBoxClient(NETBOX_URL, NETBOX_TOKEN)
    try:
        result = await netbox_client.get(endpoint, params)
        return result if isinstance(result, list) else []
    except Exception:
        return []
