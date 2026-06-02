"""Tools for the NetBox wireless app."""

from typing import Any, Dict

from ..helpers import _get_detail, _get_list, _search  # noqa: F401
from ..server import mcp


# --- wireless (wireless LANs and links) ---

# wireless/wireless-lan-groups

@mcp.tool(
    annotations={
        "title": "Search Wireless LAN Groups",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_wireless_lan_groups(args: Dict[str, Any]) -> Dict[str, Any]:
    """Search wireless LAN groups (wireless/wireless-lan-groups/).
    Accepts: name, slug, parent, ancestor, q, tag, limit
        name: Group name (case-insensitive contains match)
        slug: Group slug (exact match)
        parent: Parent group ID
        ancestor: Ancestor group ID (any depth)
        q: Free-text search across name and description
        tag: Tag slug (single)
        limit: Maximum number of results to return (default 10)

    Returns `{count, results}` (NetBox total + page). Default `brief=true`
    for compact wireless LAN group objects; pass `brief=false` for full objects. Use
    `offset` to paginate, `fields`/`exclude` to project, `limit` capped at 100.
    """
    mappings = {
        "name": "name__ic",
        "slug": "slug",
        "parent": "parent_id",
        "ancestor": "ancestor_id",
        "q": "q",
        "tag": "tag",
    }
    return await _search("wireless/wireless-lan-groups/", args, mappings)


@mcp.tool(
    annotations={
        "title": "Get Wireless LAN Group Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_wireless_lan_group_details(args: Dict[str, Any]) -> Dict[str, Any]:
    """Get wireless LAN group by ID (wireless/wireless-lan-groups/{id}/).
    Accepts: id (required)
        id: Numeric ID of the wireless LAN group to fetch. Returns the envelope `{"results": [obj]}` or `{"results": []}`.
    """
    if "id" not in args:
        return {"results": []}
    return await _get_detail("wireless/wireless-lan-groups/", args["id"], args)


# wireless/wireless-lans

@mcp.tool(
    annotations={
        "title": "Search Wireless LANs",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_wireless_lans(args: Dict[str, Any]) -> Dict[str, Any]:
    """Search wireless LANs (wireless/wireless-lans/).
    Accepts: ssid, status, group, vlan, interface, auth_type, auth_cipher,
             tenant, scope_type, scope_id, q, tag, limit
        ssid: SSID (case-insensitive contains match)
        status: Status (e.g. 'active', 'reserved', 'disabled', 'deprecated')
        group: Wireless LAN group ID or slug
        vlan: VLAN ID
        interface: Interface ID
        auth_type: 'open', 'wep', 'wpa-personal', 'wpa-enterprise', etc.
        auth_cipher: 'auto', 'tkip', 'aes'
        tenant: Tenant ID or slug
        scope_type: Scope content type (e.g. 'dcim.site')
        scope_id: Numeric scope object ID
        q: Free-text search across SSID and description
        tag: Tag slug (single)
        limit: Maximum number of results to return (default 10)

    Returns `{count, results}` (NetBox total + page). Default `brief=true`
    for compact wireless LAN objects; pass `brief=false` for full objects. Use
    `offset` to paginate, `fields`/`exclude` to project, `limit` capped at 100.
    """
    mappings = {
        "ssid": "ssid__ic",
        "status": "status",
        "group": "group",
        "vlan": "vlan_id",
        "interface": "interface_id",
        "auth_type": "auth_type",
        "auth_cipher": "auth_cipher",
        "tenant": "tenant",
        "scope_type": "scope_type",
        "scope_id": "scope_id",
        "q": "q",
        "tag": "tag",
    }
    return await _search("wireless/wireless-lans/", args, mappings)


@mcp.tool(
    annotations={
        "title": "Get Wireless LAN Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_wireless_lan_details(args: Dict[str, Any]) -> Dict[str, Any]:
    """Get wireless LAN by ID (wireless/wireless-lans/{id}/).
    Accepts: id (required)
        id: Numeric ID of the wireless LAN to fetch. Returns the envelope `{"results": [obj]}` or `{"results": []}`.
    """
    if "id" not in args:
        return {"results": []}
    return await _get_detail("wireless/wireless-lans/", args["id"], args)


# wireless/wireless-links

@mcp.tool(
    annotations={
        "title": "Search Wireless Links",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_wireless_links(args: Dict[str, Any]) -> Dict[str, Any]:
    """Search wireless links (wireless/wireless-links/).
    Accepts: ssid, status, interface_a, interface_b, auth_type, auth_cipher,
             distance, tenant, q, tag, limit
        ssid: SSID (case-insensitive contains match)
        status: Status (e.g. 'connected', 'planned', 'decommissioning')
        interface_a: Interface A ID
        interface_b: Interface B ID
        auth_type: 'open', 'wep', 'wpa-personal', 'wpa-enterprise', etc.
        auth_cipher: 'auto', 'tkip', 'aes'
        distance: Link distance value
        tenant: Tenant ID or slug
        q: Free-text search across SSID and description
        tag: Tag slug (single)
        limit: Maximum number of results to return (default 10)

    Returns `{count, results}` (NetBox total + page). Default `brief=true`
    for compact wireless link objects; pass `brief=false` for full objects. Use
    `offset` to paginate, `fields`/`exclude` to project, `limit` capped at 100.
    """
    mappings = {
        "ssid": "ssid__ic",
        "status": "status",
        "interface_a": "interface_a_id",
        "interface_b": "interface_b_id",
        "auth_type": "auth_type",
        "auth_cipher": "auth_cipher",
        "distance": "distance",
        "tenant": "tenant",
        "q": "q",
        "tag": "tag",
    }
    return await _search("wireless/wireless-links/", args, mappings)


@mcp.tool(
    annotations={
        "title": "Get Wireless Link Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_wireless_link_details(args: Dict[str, Any]) -> Dict[str, Any]:
    """Get wireless link by ID (wireless/wireless-links/{id}/).
    Accepts: id (required)
        id: Numeric ID of the wireless link to fetch. Returns the envelope `{"results": [obj]}` or `{"results": []}`.
    """
    if "id" not in args:
        return {"results": []}
    return await _get_detail("wireless/wireless-links/", args["id"], args)
