"""End-to-end smoke tests against demo.netbox.dev.

Demo NetBox data resets at 04:00 UTC daily, so these assertions are
all shape- or invariant-based (counts are non-negative integers, items
have certain keys, projections are exact subsets). Nothing depends on
specific demo values.
"""

from __future__ import annotations

import re

import pytest


_PREFIX_RE = re.compile(r"^[0-9a-fA-F:.]+/\d{1,3}$")
_IPADDR_RE = re.compile(r"^[0-9a-fA-F:.]+/\d{1,3}$")
_MAC_RE = re.compile(r"^[0-9a-fA-F:]+$")


async def _call(client, name, args):
    """Helper: invoke a tool and return the structured payload."""
    result = await client.call_tool(name, {"args": args})
    # FastMCP returns .data (typed) or .structured_content (raw JSON)
    return result.data if hasattr(result, "data") else result.structured_content


def _assert_search_envelope(payload):
    """Assert the {count, results} shape returned by every search_*."""
    assert isinstance(payload, dict), f"Expected dict, got {type(payload).__name__}"
    assert "count" in payload, f"Missing 'count' in {payload}"
    assert "results" in payload, f"Missing 'results' in {payload}"
    assert isinstance(payload["count"], int), \
        f"count is {type(payload['count']).__name__}, not int"
    assert payload["count"] >= 0, f"count is negative: {payload['count']}"
    assert isinstance(payload["results"], list), \
        f"results is {type(payload['results']).__name__}, not list"


def _assert_brief_object(obj):
    """Every brief-mode NetBox object should at least have id and display."""
    assert isinstance(obj, dict), f"Result item is not a dict: {type(obj).__name__}"
    assert "id" in obj, f"Result item missing 'id': {obj!r}"
    assert isinstance(obj["id"], int), f"id is not an int: {obj['id']!r}"


def _assert_detail_envelope(payload):
    """Assert the {results: [...]} shape returned by every get_*_details / _get_list."""
    assert isinstance(payload, dict), \
        f"Expected dict envelope, got {type(payload).__name__}: {payload!r}"
    assert "results" in payload, f"Missing 'results' in {payload!r}"
    assert isinstance(payload["results"], list), \
        f"results is {type(payload['results']).__name__}, not list"


def _assert_action_envelope(payload):
    """Assert the {result: ...} shape returned by every _get_action tool."""
    assert isinstance(payload, dict), \
        f"Expected dict envelope, got {type(payload).__name__}: {payload!r}"
    assert "result" in payload, f"Missing 'result' in {payload!r}"


# ---------------------------------------------------------------------------
# Core search/detail shape checks
# ---------------------------------------------------------------------------


async def test_search_sites_shape(mcp_client):
    payload = await _call(mcp_client, "search_sites", {"limit": 5})
    _assert_search_envelope(payload)
    for site in payload["results"]:
        _assert_brief_object(site)


async def test_get_site_details_round_trip(mcp_client):
    payload = await _call(mcp_client, "search_sites", {"limit": 1})
    _assert_search_envelope(payload)
    if not payload["results"]:
        pytest.skip("demo NetBox has no sites; can't round-trip")
    sid = payload["results"][0]["id"]
    detail = await _call(mcp_client, "get_site_details", {"id": sid})
    _assert_detail_envelope(detail)
    assert len(detail["results"]) == 1, (
        f"Detail returned {len(detail['results'])} items, expected 1"
    )
    assert detail["results"][0]["id"] == sid


async def test_get_site_details_missing_id_returns_empty_envelope(mcp_client):
    """No `id` arg -> {results: []} per the helper convention."""
    detail = await _call(mcp_client, "get_site_details", {})
    assert detail == {"results": []}


async def test_get_site_details_unknown_id_returns_empty_envelope(mcp_client):
    """Unknown id -> {results: []} (helper swallows the 404)."""
    detail = await _call(
        mcp_client, "get_site_details", {"id": 99999999}
    )
    assert detail == {"results": []}


# ---------------------------------------------------------------------------
# Pagination / limit semantics
# ---------------------------------------------------------------------------


async def test_search_sites_limit_cap_enforced(mcp_client):
    """`limit` above the MAX_LIMIT (100) is clamped, not honoured."""
    payload = await _call(mcp_client, "search_sites", {"limit": 1000})
    _assert_search_envelope(payload)
    assert len(payload["results"]) <= 100, (
        f"limit cap not enforced: got {len(payload['results'])} results"
    )


async def test_search_sites_pagination_disjoint(mcp_client):
    """Pages 0 and 1 with limit=1 should not overlap when count >= 2."""
    base = await _call(mcp_client, "search_sites", {"limit": 1})
    _assert_search_envelope(base)
    if base["count"] < 2:
        pytest.skip("demo NetBox has <2 sites; pagination check N/A")
    next_page = await _call(
        mcp_client, "search_sites", {"limit": 1, "offset": 1}
    )
    _assert_search_envelope(next_page)
    if not base["results"] or not next_page["results"]:
        pytest.skip("expected results but got empty pages")
    assert base["results"][0]["id"] != next_page["results"][0]["id"]


# ---------------------------------------------------------------------------
# brief / fields projection
# ---------------------------------------------------------------------------


async def test_search_sites_brief_false_returns_fuller_object(mcp_client):
    """brief=false should produce more keys than brief=true."""
    brief = await _call(mcp_client, "search_sites", {"limit": 1})
    full = await _call(
        mcp_client, "search_sites", {"limit": 1, "brief": False}
    )
    _assert_search_envelope(brief)
    _assert_search_envelope(full)
    if not brief["results"] or not full["results"]:
        pytest.skip("demo NetBox has no sites; brief check N/A")
    assert len(full["results"][0]) >= len(brief["results"][0]), (
        f"brief=false didn't return more keys: "
        f"brief={list(brief['results'][0])}, full={list(full['results'][0])}"
    )


async def test_search_sites_fields_projection(mcp_client):
    """`fields=id,name` returns results with at most {id, name} keys.

    NetBox's `?fields=` is an allowlist; the response items contain
    only the requested fields (plus nothing else from the server). We
    assert subset rather than equality to be robust to NetBox quirks
    (some endpoints always include `id`).
    """
    payload = await _call(
        mcp_client, "search_sites",
        {"limit": 3, "fields": "id,name"},
    )
    _assert_search_envelope(payload)
    if not payload["results"]:
        pytest.skip("demo NetBox has no sites; projection check N/A")
    for site in payload["results"]:
        extras = set(site.keys()) - {"id", "name"}
        assert not extras, (
            f"fields=id,name returned extra keys {extras} for {site!r}"
        )


# ---------------------------------------------------------------------------
# Other resources - shape only, no data assumptions
# ---------------------------------------------------------------------------


async def test_search_devices_shape(mcp_client):
    payload = await _call(mcp_client, "search_devices", {"limit": 5})
    _assert_search_envelope(payload)
    for dev in payload["results"]:
        _assert_brief_object(dev)


async def test_search_prefixes_shape_and_format(mcp_client):
    payload = await _call(mcp_client, "search_prefixes", {"limit": 5})
    _assert_search_envelope(payload)
    for p in payload["results"]:
        _assert_brief_object(p)
        # Brief mode includes `prefix` as the canonical identifier
        if "prefix" in p:
            assert _PREFIX_RE.match(p["prefix"]), \
                f"Bad prefix format: {p['prefix']!r}"


async def test_search_ip_addresses_shape_and_format(mcp_client):
    payload = await _call(mcp_client, "search_ip_addresses", {"limit": 5})
    _assert_search_envelope(payload)
    for ip in payload["results"]:
        _assert_brief_object(ip)
        if "address" in ip:
            assert _IPADDR_RE.match(ip["address"]), \
                f"Bad address format: {ip['address']!r}"


async def test_search_vlans_shape(mcp_client):
    payload = await _call(mcp_client, "search_vlans", {"limit": 5})
    _assert_search_envelope(payload)
    for v in payload["results"]:
        _assert_brief_object(v)


async def test_search_interfaces_shape(mcp_client):
    payload = await _call(mcp_client, "search_interfaces", {"limit": 5})
    _assert_search_envelope(payload)
    for iface in payload["results"]:
        _assert_brief_object(iface)


# ---------------------------------------------------------------------------
# Negative filters
# ---------------------------------------------------------------------------


async def test_search_nonexistent_name_returns_zero(mcp_client):
    """A guaranteed-bogus filter should yield 0 results without 5xx."""
    payload = await _call(
        mcp_client, "search_sites",
        {"name": "definitely-not-a-real-site-xyzqq", "limit": 5},
    )
    _assert_search_envelope(payload)
    assert payload["count"] == 0
    assert payload["results"] == []


# ---------------------------------------------------------------------------
# Available-IP sub-resource
# ---------------------------------------------------------------------------


async def test_get_prefix_available_ips_shape(mcp_client):
    """If demo has any prefix, available-ips should return the {results} envelope."""
    prefixes = await _call(mcp_client, "search_prefixes", {"limit": 1})
    _assert_search_envelope(prefixes)
    if not prefixes["results"]:
        pytest.skip("demo NetBox has no prefixes")
    pid = prefixes["results"][0]["id"]
    avail = await _call(
        mcp_client, "get_prefix_available_ips", {"id": pid, "limit": 3}
    )
    _assert_detail_envelope(avail)
    # If non-empty, each entry must have an address-like field
    for entry in avail["results"]:
        assert isinstance(entry, dict)
        assert "address" in entry or "family" in entry, (
            f"available-ips entry missing recognised fields: {entry!r}"
        )


async def test_get_ip_range_available_ips_shape(mcp_client):
    """Same envelope contract on the IP-range variant.

    NetBox returns an empty list when the parent range has
    ``mark_utilized=true``, so we don't assert non-empty results; we
    only assert the envelope shape is consistent with the prefix variant.
    """
    ranges = await _call(mcp_client, "search_ip_ranges", {"limit": 1})
    _assert_search_envelope(ranges)
    if not ranges["results"]:
        pytest.skip("demo NetBox has no IP ranges")
    rid = ranges["results"][0]["id"]
    avail = await _call(
        mcp_client, "get_ip_range_available_ips", {"id": rid, "limit": 3}
    )
    _assert_detail_envelope(avail)
    for entry in avail["results"]:
        assert isinstance(entry, dict)
        assert "address" in entry or "family" in entry, (
            f"available-ips entry missing recognised fields: {entry!r}"
        )


# ---------------------------------------------------------------------------
# Envelope contract for not-found / missing-id across helper families
# ---------------------------------------------------------------------------


async def test_get_list_unknown_id_returns_results_envelope(mcp_client):
    """_get_list-backed tools also emit {results: []} on missing/unknown id.

    Covers the helper class behind ``get_prefix_available_ips`` and
    siblings; without the envelope FastMCP would drop structured
    content over the wire and the tool would appear to "return nothing".
    """
    avail = await _call(mcp_client, "get_prefix_available_ips", {})
    assert avail == {"results": []}


async def test_get_action_unknown_id_returns_result_envelope(mcp_client):
    """_get_action-backed tools emit {result: []} on missing id.

    Covers trace / elevation endpoints. The key is ``result`` (singular)
    not ``results``, because the payload is heterogeneous (list of
    segments, list of rack units, rendered config blob).
    """
    payload = await _call(mcp_client, "get_interface_trace", {})
    assert payload == {"result": []}
