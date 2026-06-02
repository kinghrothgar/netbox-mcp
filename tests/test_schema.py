"""Tool-registry shape assertions.

These tests describe *our* code (which tools exist, what their schemas
look like) rather than demo NetBox data, so the assertions can be
exact even though seed data is volatile.
"""

from __future__ import annotations

from typing import Tuple

import pytest


# Tool counts and gated tool names per target version. Updating either
# of these tables is the canonical way to record a new gated endpoint.
_EXPECTED_TOOL_COUNT = {
    (4, 5): 224,
    (4, 6): 230,
}

_GATED_TOOL_NAMES = {
    "search_rack_groups",
    "get_rack_group_details",
    "search_cable_bundles",
    "get_cable_bundle_details",
    "search_virtual_machine_types",
    "get_virtual_machine_type_details",
}


async def _tool_names(client) -> list[str]:
    tools = await client.list_tools()
    return sorted(t.name for t in tools)


async def test_tool_count_matches_target_version(
    mcp_client, target_version: Tuple[int, int]
):
    """The registered tool count is exactly what we expect for the target."""
    expected = _EXPECTED_TOOL_COUNT.get(target_version)
    if expected is None:
        pytest.skip(
            f"No expected tool count recorded for target "
            f"{target_version[0]}.{target_version[1]}; update the table."
        )
    names = await _tool_names(mcp_client)
    assert len(names) == expected, (
        f"Expected {expected} tools on target "
        f"{target_version[0]}.{target_version[1]}, got {len(names)}: "
        f"diff={set(names).symmetric_difference(set())}"
    )


async def test_gated_tools_presence_matches_target(
    mcp_client, target_version: Tuple[int, int]
):
    """4.6-only tools are registered only when target >= (4, 6)."""
    names = set(await _tool_names(mcp_client))
    present = _GATED_TOOL_NAMES & names
    if target_version >= (4, 6):
        assert present == _GATED_TOOL_NAMES, (
            f"Missing gated tools on {target_version}: "
            f"{_GATED_TOOL_NAMES - present}"
        )
    else:
        assert not present, (
            f"Gated tools leaked into target {target_version}: {present}"
        )


async def test_every_tool_has_description(mcp_client):
    """No tool should ship without a docstring."""
    tools = await mcp_client.list_tools()
    missing = [t.name for t in tools if not (t.description or "").strip()]
    assert not missing, f"Tools without description: {missing}"


async def test_every_tool_accepts_args_object(mcp_client):
    """Every tool takes a single ``args`` parameter typed as an object.

    This is the calling convention enforced across the package; a
    regression here would mean a tool was added without following the
    pattern.
    """
    tools = await mcp_client.list_tools()
    bad = []
    for t in tools:
        schema = getattr(t, "inputSchema", None) or {}
        props = (schema.get("properties") or {})
        if list(props.keys()) != ["args"]:
            bad.append((t.name, list(props.keys())))
            continue
        args_schema = props["args"]
        if args_schema.get("type") != "object":
            bad.append((t.name, args_schema.get("type")))
    assert not bad, f"Tools with non-standard input schema: {bad[:10]}"


async def test_search_get_pairs_consistent(mcp_client):
    """For every ``get_<x>_details`` there should be a ``search_<x>s``.

    The repo convention is that each resource has both. A mismatch
    usually means somebody added one and forgot the other. The naive
    ``+s`` plural misses English-language irregulars (policy/policies,
    address/addresses, etc.); we handle the common cases here.
    """
    names = set(await _tool_names(mcp_client))
    detail_tools = {
        n for n in names
        if n.startswith("get_") and n.endswith("_details")
    }
    missing_search = []
    for d in detail_tools:
        stem = d[len("get_"):-len("_details")]
        candidates = {
            f"search_{stem}s",            # site -> sites
            f"search_{stem}",             # virtual_chassis stays singular
            f"search_{stem}es",           # address -> addresses, prefix -> prefixes
        }
        # policy -> policies, entry -> entries
        if stem.endswith("y"):
            candidates.add(f"search_{stem[:-1]}ies")
        if not candidates & names:
            missing_search.append(d)
    assert not missing_search, (
        f"Detail tools without a search counterpart: {missing_search}"
    )
