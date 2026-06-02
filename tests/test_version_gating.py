"""Version-gating behaviour against the matched demo NetBox target.

When the netbox-mcp target version matches the demo NetBox version,
the gated tools should both be registered AND succeed against the
backend (no 404). Schema-level presence is covered in
``test_schema.py``; here we exercise each gated tool end-to-end.

Tests skip when the target version doesn't include a given gated
feature (e.g. running against a demo NetBox 4.5).
"""

from __future__ import annotations

from typing import Tuple

import pytest


async def _call(client, name, args):
    result = await client.call_tool(name, {"args": args})
    return result.data if hasattr(result, "data") else result.structured_content


def _assert_search_envelope(payload):
    assert isinstance(payload, dict), payload
    assert isinstance(payload.get("count"), int), payload
    assert isinstance(payload.get("results"), list), payload


# ---------------------------------------------------------------------------
# 4.6 endpoint coverage
# ---------------------------------------------------------------------------


async def test_search_rack_groups_responds(
    mcp_client, target_version: Tuple[int, int]
):
    if target_version < (4, 6):
        pytest.skip("search_rack_groups requires target >= 4.6")
    payload = await _call(mcp_client, "search_rack_groups", {"limit": 5})
    _assert_search_envelope(payload)


async def test_search_cable_bundles_responds(
    mcp_client, target_version: Tuple[int, int]
):
    if target_version < (4, 6):
        pytest.skip("search_cable_bundles requires target >= 4.6")
    payload = await _call(mcp_client, "search_cable_bundles", {"limit": 5})
    _assert_search_envelope(payload)


async def test_search_virtual_machine_types_responds(
    mcp_client, target_version: Tuple[int, int]
):
    if target_version < (4, 6):
        pytest.skip("search_virtual_machine_types requires target >= 4.6")
    payload = await _call(
        mcp_client, "search_virtual_machine_types", {"limit": 5}
    )
    _assert_search_envelope(payload)


# ---------------------------------------------------------------------------
# 4.6 filter coverage on shared tools
# ---------------------------------------------------------------------------


async def test_search_asns_role_filter_accepted(
    mcp_client, target_version: Tuple[int, int]
):
    """The 4.6-only ``role`` filter on search_asns must reach the API.

    NetBox 4.6 strictly validates the filter value against the set of
    defined IPAM roles; passing a bogus value returns HTTP 400. To
    avoid coupling the test to specific demo seed data, we first
    discover a real role ID by searching IPAM roles, then use it.
    If the demo has no roles at all, we skip rather than fail - the
    inability to *exercise* the filter against this data doesn't
    invalidate the gating refactor.
    """
    if target_version < (4, 6):
        pytest.skip("role filter on search_asns requires target >= 4.6")
    # The ASN role filter on /api/ipam/asns/ accepts the role slug, not
    # the integer ID. Request brief=False so the slug field is in the
    # response (brief returns only id/url/display).
    roles = await _call(
        mcp_client, "search_ipam_roles",
        {"limit": 1, "brief": False},
    )
    _assert_search_envelope(roles)
    if not roles["results"]:
        pytest.skip("demo NetBox has no IPAM roles; can't exercise filter")
    role_slug = roles["results"][0].get("slug")
    if not role_slug:
        pytest.skip("IPAM role result has no 'slug' field")
    payload = await _call(
        mcp_client, "search_asns", {"role": role_slug, "limit": 5}
    )
    _assert_search_envelope(payload)


async def test_search_virtual_machines_vmtype_filter_accepted(
    mcp_client, target_version: Tuple[int, int]
):
    """4.6-only ``virtual_machine_type`` filter on search_virtual_machines.

    Same approach as the ASN role test: discover a real virtual
    machine type ID first, then use it. Skip if demo has none.
    """
    if target_version < (4, 6):
        pytest.skip(
            "virtual_machine_type filter requires target >= 4.6"
        )
    vmts = await _call(
        mcp_client, "search_virtual_machine_types", {"limit": 1}
    )
    _assert_search_envelope(vmts)
    if not vmts["results"]:
        pytest.skip(
            "demo NetBox has no virtual machine types; can't exercise filter"
        )
    vmt_id = vmts["results"][0]["id"]
    payload = await _call(
        mcp_client, "search_virtual_machines",
        {"virtual_machine_type": vmt_id, "limit": 5},
    )
    _assert_search_envelope(payload)


# ---------------------------------------------------------------------------
# Detail tools for 4.6 endpoints
# ---------------------------------------------------------------------------


async def test_get_rack_group_details_missing_id(
    mcp_client, target_version: Tuple[int, int]
):
    """Detail tools return [] when called without id, even when gated."""
    if target_version < (4, 6):
        pytest.skip("get_rack_group_details requires target >= 4.6")
    assert await _call(mcp_client, "get_rack_group_details", {}) == []


async def test_get_cable_bundle_details_missing_id(
    mcp_client, target_version: Tuple[int, int]
):
    if target_version < (4, 6):
        pytest.skip("get_cable_bundle_details requires target >= 4.6")
    assert await _call(mcp_client, "get_cable_bundle_details", {}) == []


async def test_get_virtual_machine_type_details_missing_id(
    mcp_client, target_version: Tuple[int, int]
):
    if target_version < (4, 6):
        pytest.skip(
            "get_virtual_machine_type_details requires target >= 4.6"
        )
    assert await _call(
        mcp_client, "get_virtual_machine_type_details", {}
    ) == []
