"""Small reusable helpers to reduce repetition across tools."""

from typing import Any, Dict, List

from .client import NETBOX_TOKEN, NETBOX_URL, NetBoxClient


def _build_params(args: Dict[str, Any], mappings: Dict[str, str], default_limit: int = 10) -> Dict[str, Any]:
    """Build query params for NetBox from incoming args using a mapping.

    mappings: dict of incoming arg name -> NetBox query param name
    """
    params: Dict[str, Any] = {"limit": args.get("limit", default_limit)}
    for incoming_name, query_name in mappings.items():
        if incoming_name in args:
            params[query_name] = args[incoming_name]
    return params


async def _search(endpoint: str, args: Dict[str, Any], mappings: Dict[str, str], default_limit: int = 10) -> List[Dict[str, Any]]:
    params = _build_params(args, mappings, default_limit)
    netbox_client = NetBoxClient(NETBOX_URL, NETBOX_TOKEN)
    result = await netbox_client.get(endpoint, params)
    return result.get("results", [])


async def _get_detail(endpoint_base: str, id_value: Any) -> List[Dict[str, Any]]:
    netbox_client = NetBoxClient(NETBOX_URL, NETBOX_TOKEN)
    try:
        result = await netbox_client.get(f"{endpoint_base}{id_value}/")
        return [result] if isinstance(result, dict) else []
    except Exception:
        return []


async def _get_list(endpoint: str, args: Dict[str, Any], default_limit: int = 10) -> List[Dict[str, Any]]:
    """Fetch an endpoint that returns a JSON list directly (no `results` envelope).

    Used for NetBox sub-resources like `available-ips`, `available-prefixes`,
    `available-asns`, `available-vlans`, which return a bare list.
    """
    params: Dict[str, Any] = {"limit": args.get("limit", default_limit)}
    netbox_client = NetBoxClient(NETBOX_URL, NETBOX_TOKEN)
    try:
        result = await netbox_client.get(endpoint, params)
        return result if isinstance(result, list) else []
    except Exception:
        return []
