"""Tools for the NetBox ipam app."""

from typing import Any, Dict, List

from ..helpers import _get_detail, _get_list, _search
from ..server import mcp


# --- ipam (vrfs, prefixes, ip-addresses, vlans, etc.) ---

# ipam/vrfs

@mcp.tool(
    annotations={
        "title": "Search VRFs",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_vrfs(args: Dict[str, Any]) -> Dict[str, Any]:
    """Search VRFs (ipam/vrfs/).
    Accepts: name, rd, tenant, import_target, export_target, enforce_unique, tag, q, limit
        name: VRF name (case-insensitive contains match)
        rd: Route distinguisher (exact match)
        tenant: Tenant ID or slug
        import_target: Import route target name
        export_target: Export route target name
        enforce_unique: Boolean - whether the VRF enforces unique IP space
        tag: Tag slug (single)
        q: Free-text search across name, RD, and description
        limit: Maximum number of results to return (default 10)

    Returns `{count, results}` (NetBox total + page). Default `brief=true`
    for compact VRF objects; pass `brief=false` for full objects. Use
    `offset` to paginate, `fields`/`exclude` to project, `limit` capped at 100.
    """
    mappings = {
        "name": "name__ic",
        "rd": "rd",
        "tenant": "tenant",
        "import_target": "import_target",
        "export_target": "export_target",
        "enforce_unique": "enforce_unique",
        "tag": "tag",
        "q": "q",
    }
    return await _search("ipam/vrfs/", args, mappings)


@mcp.tool(
    annotations={
        "title": "Get VRF Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_vrf_details(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Get VRF by ID (ipam/vrfs/{id}/).
    Accepts: id (required)
        id: Numeric ID of the VRF to fetch. Returns `[obj]` or `[]`.
    """
    if "id" not in args:
        return []
    return await _get_detail("ipam/vrfs/", args["id"], args)


# ipam/route-targets

@mcp.tool(
    annotations={
        "title": "Search Route Targets",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_route_targets(args: Dict[str, Any]) -> Dict[str, Any]:
    """Search route targets (ipam/route-targets/).
    Accepts: name, tenant, importing_vrf, exporting_vrf, tag, q, limit
        name: Route target name (case-insensitive contains match)
        tenant: Tenant ID or slug
        importing_vrf: RD of an importing VRF
        exporting_vrf: RD of an exporting VRF
        tag: Tag slug (single)
        q: Free-text search across name and description
        limit: Maximum number of results to return (default 10)

    Returns `{count, results}` (NetBox total + page). Default `brief=true`
    for compact route target objects; pass `brief=false` for full objects. Use
    `offset` to paginate, `fields`/`exclude` to project, `limit` capped at 100.
    """
    mappings = {
        "name": "name__ic",
        "tenant": "tenant",
        "importing_vrf": "importing_vrf",
        "exporting_vrf": "exporting_vrf",
        "tag": "tag",
        "q": "q",
    }
    return await _search("ipam/route-targets/", args, mappings)


@mcp.tool(
    annotations={
        "title": "Get Route Target Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_route_target_details(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Get route target by ID (ipam/route-targets/{id}/).
    Accepts: id (required)
        id: Numeric ID of the route target to fetch. Returns `[obj]` or `[]`.
    """
    if "id" not in args:
        return []
    return await _get_detail("ipam/route-targets/", args["id"], args)


# ipam/rirs

@mcp.tool(
    annotations={
        "title": "Search RIRs",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_rirs(args: Dict[str, Any]) -> Dict[str, Any]:
    """Search RIRs (ipam/rirs/).
    Accepts: name, slug, is_private, tag, q, limit
        name: RIR name (case-insensitive contains match)
        slug: RIR slug (exact match)
        is_private: Boolean - whether this RIR represents private address space
        tag: Tag slug (single)
        q: Free-text search
        limit: Maximum number of results to return (default 10)

    Returns `{count, results}` (NetBox total + page). Default `brief=true`
    for compact RIR objects; pass `brief=false` for full objects. Use
    `offset` to paginate, `fields`/`exclude` to project, `limit` capped at 100.
    """
    mappings = {
        "name": "name__ic",
        "slug": "slug",
        "is_private": "is_private",
        "tag": "tag",
        "q": "q",
    }
    return await _search("ipam/rirs/", args, mappings)


@mcp.tool(
    annotations={
        "title": "Get RIR Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_rir_details(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Get RIR by ID (ipam/rirs/{id}/).
    Accepts: id (required)
        id: Numeric ID of the RIR to fetch. Returns `[obj]` or `[]`.
    """
    if "id" not in args:
        return []
    return await _get_detail("ipam/rirs/", args["id"], args)


# ipam/aggregates

@mcp.tool(
    annotations={
        "title": "Search Aggregates",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_aggregates(args: Dict[str, Any]) -> Dict[str, Any]:
    """Search aggregates (ipam/aggregates/).
    Accepts: prefix, family, rir, tenant, tag, q, limit
        prefix: Exact CIDR (e.g. '10.0.0.0/8')
        family: IP family (4 or 6)
        rir: RIR ID or slug
        tenant: Tenant ID or slug
        tag: Tag slug (single)
        q: Free-text search across prefix and description
        limit: Maximum number of results to return (default 10)

    Returns `{count, results}` (NetBox total + page). Default `brief=true`
    for compact aggregate objects; pass `brief=false` for full objects. Use
    `offset` to paginate, `fields`/`exclude` to project, `limit` capped at 100.
    """
    mappings = {
        "prefix": "prefix",
        "family": "family",
        "rir": "rir",
        "tenant": "tenant",
        "tag": "tag",
        "q": "q",
    }
    return await _search("ipam/aggregates/", args, mappings)


@mcp.tool(
    annotations={
        "title": "Get Aggregate Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_aggregate_details(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Get aggregate by ID (ipam/aggregates/{id}/).
    Accepts: id (required)
        id: Numeric ID of the aggregate to fetch. Returns `[obj]` or `[]`.
    """
    if "id" not in args:
        return []
    return await _get_detail("ipam/aggregates/", args["id"], args)


# ipam/roles

@mcp.tool(
    annotations={
        "title": "Search IPAM Roles",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_ipam_roles(args: Dict[str, Any]) -> Dict[str, Any]:
    """Search IPAM roles (ipam/roles/).

    IPAM roles tag prefixes and VLANs with a logical role (e.g. Production,
    Staging). Distinct from device-roles, rack-roles, etc.

    Accepts: name, slug, weight, tag, q, limit
        name: Role name (case-insensitive contains match)
        slug: Role slug (exact match)
        weight: Numeric weight (exact match)
        tag: Tag slug (single)
        q: Free-text search
        limit: Maximum number of results to return (default 10)

    Returns `{count, results}` (NetBox total + page). Default `brief=true`
    for compact IPAM role objects; pass `brief=false` for full objects. Use
    `offset` to paginate, `fields`/`exclude` to project, `limit` capped at 100.
    """
    mappings = {
        "name": "name__ic",
        "slug": "slug",
        "weight": "weight",
        "tag": "tag",
        "q": "q",
    }
    return await _search("ipam/roles/", args, mappings)


@mcp.tool(
    annotations={
        "title": "Get IPAM Role Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_ipam_role_details(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Get IPAM role by ID (ipam/roles/{id}/).
    Accepts: id (required)
        id: Numeric ID of the IPAM role to fetch. Returns `[obj]` or `[]`.
    """
    if "id" not in args:
        return []
    return await _get_detail("ipam/roles/", args["id"], args)


# ipam/prefixes

@mcp.tool(
    annotations={
        "title": "Search Prefixes",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_prefixes(args: Dict[str, Any]) -> Dict[str, Any]:
    """Search prefixes (ipam/prefixes/).

    Accepts: prefix, within, within_include, contains, family, mask_length,
             mask_length__gte, mask_length__lte, vrf, vlan, vlan_vid, role,
             site, tenant, status, is_pool, mark_utilized, tag, q, limit
        prefix: Exact CIDR (e.g. '10.0.0.0/24')
        within: Return prefixes strictly within this CIDR
        within_include: Return prefixes within or equal to this CIDR
        contains: Return prefixes that contain this CIDR or IP
        family: IP family (4 or 6)
        mask_length: Exact mask length
        mask_length__gte: Mask length >= value
        mask_length__lte: Mask length <= value
        vrf: VRF RD or ID
        vlan: VLAN ID (numeric)
        vlan_vid: VLAN VID (1-4094)
        role: IPAM role slug or ID
        site: Site slug or ID (via prefix scope)
        tenant: Tenant ID or slug
        status: Status (e.g. 'active', 'reserved', 'container', 'deprecated')
        is_pool: Boolean
        mark_utilized: Boolean
        tag: Tag slug (single)
        q: Free-text search across prefix and description
        limit: Maximum number of results to return (default 10)

    Returns `{count, results}` (NetBox total + page). Default `brief=true`
    for compact prefix objects; pass `brief=false` for full objects. Use
    `offset` to paginate, `fields`/`exclude` to project, `limit` capped at 100.
    """
    mappings = {
        "prefix": "prefix",
        "within": "within",
        "within_include": "within_include",
        "contains": "contains",
        "family": "family",
        "mask_length": "mask_length",
        "mask_length__gte": "mask_length__gte",
        "mask_length__lte": "mask_length__lte",
        "vrf": "vrf",
        "vlan": "vlan_id",
        "vlan_vid": "vlan_vid",
        "role": "role",
        "site": "site",
        "tenant": "tenant",
        "status": "status",
        "is_pool": "is_pool",
        "mark_utilized": "mark_utilized",
        "tag": "tag",
        "q": "q",
    }
    return await _search("ipam/prefixes/", args, mappings)


@mcp.tool(
    annotations={
        "title": "Get Prefix Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_prefix_details(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Get prefix by ID (ipam/prefixes/{id}/).
    Accepts: id (required)
        id: Numeric ID of the prefix to fetch. Returns `[obj]` or `[]`.
    """
    if "id" not in args:
        return []
    return await _get_detail("ipam/prefixes/", args["id"], args)


# ipam/prefixes/{id}/available-prefixes

@mcp.tool(
    annotations={
        "title": "Get Available Child Prefixes",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_prefix_available_prefixes(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """List free child prefixes inside a parent prefix
    (ipam/prefixes/{id}/available-prefixes/).

    Accepts: id (required), limit
        id: Numeric ID of the parent prefix
        limit: Maximum number of results (default 10)

    Returns a list of available prefix candidates, or `[]`.
    """
    if "id" not in args:
        return []
    return await _get_list(f"ipam/prefixes/{args['id']}/available-prefixes/", args)


# ipam/prefixes/{id}/available-ips

@mcp.tool(
    annotations={
        "title": "Get Available IPs in Prefix",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_prefix_available_ips(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """List free IP addresses inside a prefix
    (ipam/prefixes/{id}/available-ips/).

    Accepts: id (required), limit
        id: Numeric ID of the prefix
        limit: Maximum number of IPs to return (default 10)

    Returns a list of available IP address candidates, or `[]`.
    """
    if "id" not in args:
        return []
    return await _get_list(f"ipam/prefixes/{args['id']}/available-ips/", args)


# ipam/ip-ranges

@mcp.tool(
    annotations={
        "title": "Search IP Ranges",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_ip_ranges(args: Dict[str, Any]) -> Dict[str, Any]:
    """Search IP ranges (ipam/ip-ranges/).
    Accepts: start_address, end_address, parent, contains, vrf, role, status,
             tenant, tag, q, limit
        start_address: Range start IP
        end_address: Range end IP
        parent: Parent CIDR
        contains: An IP or CIDR that ranges must contain
        vrf: VRF RD or ID
        role: IPAM role slug or ID
        status: Status (e.g. 'active', 'reserved', 'deprecated')
        tenant: Tenant ID or slug
        tag: Tag slug (single)
        q: Free-text search across description, start, and end addresses
        limit: Maximum number of results to return (default 10)

    Returns `{count, results}` (NetBox total + page). Default `brief=true`
    for compact IP range objects; pass `brief=false` for full objects. Use
    `offset` to paginate, `fields`/`exclude` to project, `limit` capped at 100.
    """
    mappings = {
        "start_address": "start_address",
        "end_address": "end_address",
        "parent": "parent",
        "contains": "contains",
        "vrf": "vrf",
        "role": "role",
        "status": "status",
        "tenant": "tenant",
        "tag": "tag",
        "q": "q",
    }
    return await _search("ipam/ip-ranges/", args, mappings)


@mcp.tool(
    annotations={
        "title": "Get IP Range Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_ip_range_details(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Get IP range by ID (ipam/ip-ranges/{id}/).
    Accepts: id (required)
        id: Numeric ID of the IP range to fetch. Returns `[obj]` or `[]`.
    """
    if "id" not in args:
        return []
    return await _get_detail("ipam/ip-ranges/", args["id"], args)


# ipam/ip-ranges/{id}/available-ips

@mcp.tool(
    annotations={
        "title": "Get Available IPs in IP Range",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_ip_range_available_ips(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """List free IP addresses inside an IP range
    (ipam/ip-ranges/{id}/available-ips/).

    Accepts: id (required), limit
        id: Numeric ID of the IP range
        limit: Maximum number of IPs to return (default 10)

    Returns a list of available IP address candidates, or `[]`.
    """
    if "id" not in args:
        return []
    return await _get_list(f"ipam/ip-ranges/{args['id']}/available-ips/", args)


# ipam/ip-addresses

@mcp.tool(
    annotations={
        "title": "Search IP Addresses",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_ip_addresses(args: Dict[str, Any]) -> Dict[str, Any]:
    """Search IP addresses (ipam/ip-addresses/).

    Accepts: address, parent, family, mask_length, vrf, present_in_vrf, device,
             virtual_machine, interface, vminterface, assigned,
             assigned_to_interface, status, role, dns_name, tenant, tag, q, limit
        address: Specific address (with or without mask)
        parent: Parent CIDR (filter IPs contained within)
        family: IP family (4 or 6)
        mask_length: Exact mask length
        vrf: VRF RD or ID
        present_in_vrf: VRF RD or ID - includes IPs imported via route targets
        device: Device name
        virtual_machine: Virtual machine name
        interface: Interface name (on a device)
        vminterface: VM interface name
        assigned: Boolean - whether address is assigned to anything
        assigned_to_interface: Boolean - whether assigned to a device/VM interface
        status: Status (e.g. 'active', 'reserved', 'deprecated', 'dhcp', 'slaac')
        role: Role (e.g. 'loopback', 'secondary', 'anycast', 'vip', 'vrrp', etc.)
        dns_name: DNS name (case-insensitive contains via NetBox default)
        tenant: Tenant ID or slug
        tag: Tag slug (single)
        q: Free-text search across address, DNS name, and description
        limit: Maximum number of results to return (default 10)

    Returns `{count, results}` (NetBox total + page). Default `brief=true`
    for compact IP address objects; pass `brief=false` for full objects. Use
    `offset` to paginate, `fields`/`exclude` to project, `limit` capped at 100.
    """
    mappings = {
        "address": "address",
        "parent": "parent",
        "family": "family",
        "mask_length": "mask_length",
        "vrf": "vrf",
        "present_in_vrf": "present_in_vrf",
        "device": "device",
        "virtual_machine": "virtual_machine",
        "interface": "interface",
        "vminterface": "vminterface",
        "assigned": "assigned",
        "assigned_to_interface": "assigned_to_interface",
        "status": "status",
        "role": "role",
        "dns_name": "dns_name",
        "tenant": "tenant",
        "tag": "tag",
        "q": "q",
    }
    return await _search("ipam/ip-addresses/", args, mappings)


@mcp.tool(
    annotations={
        "title": "Get IP Address Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_ip_address_details(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Get IP address by ID (ipam/ip-addresses/{id}/).
    Accepts: id (required)
        id: Numeric ID of the IP address to fetch. Returns `[obj]` or `[]`.
    """
    if "id" not in args:
        return []
    return await _get_detail("ipam/ip-addresses/", args["id"], args)


# ipam/fhrp-groups

@mcp.tool(
    annotations={
        "title": "Search FHRP Groups",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_fhrp_groups(args: Dict[str, Any]) -> Dict[str, Any]:
    """Search FHRP groups (ipam/fhrp-groups/).

    Accepts: group_id, name, protocol, auth_type, related_ip, tag, q, limit
        group_id: Numeric group identifier
        name: Group name (case-insensitive contains match)
        protocol: One of 'vrrp2', 'vrrp3', 'carp', 'clusterxl', 'hsrp', 'glbp', 'other'
        auth_type: Authentication type
        related_ip: IP address ID
        tag: Tag slug (single)
        q: Free-text search across name, group_id, and description
        limit: Maximum number of results to return (default 10)

    Returns `{count, results}` (NetBox total + page). Default `brief=true`
    for compact FHRP group objects; pass `brief=false` for full objects. Use
    `offset` to paginate, `fields`/`exclude` to project, `limit` capped at 100.
    """
    mappings = {
        "group_id": "group_id",
        "name": "name__ic",
        "protocol": "protocol",
        "auth_type": "auth_type",
        "related_ip": "related_ip",
        "tag": "tag",
        "q": "q",
    }
    return await _search("ipam/fhrp-groups/", args, mappings)


@mcp.tool(
    annotations={
        "title": "Get FHRP Group Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_fhrp_group_details(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Get FHRP group by ID (ipam/fhrp-groups/{id}/).
    Accepts: id (required)
        id: Numeric ID of the FHRP group to fetch. Returns `[obj]` or `[]`.
    """
    if "id" not in args:
        return []
    return await _get_detail("ipam/fhrp-groups/", args["id"], args)


# ipam/fhrp-group-assignments

@mcp.tool(
    annotations={
        "title": "Search FHRP Group Assignments",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_fhrp_group_assignments(args: Dict[str, Any]) -> Dict[str, Any]:
    """Search FHRP group assignments (ipam/fhrp-group-assignments/).

    Accepts: group_id, interface_type, interface_id, priority, device,
             virtual_machine, limit
        group_id: FHRP group ID
        interface_type: Content type of the interface (e.g. 'dcim.interface')
        interface_id: Interface ID
        priority: FHRP priority value
        device: Device name (matches device interfaces)
        virtual_machine: Virtual machine name (matches VM interfaces)
        limit: Maximum number of results to return (default 10)

    Returns `{count, results}` (NetBox total + page). Default `brief=true`
    for compact FHRP group assignment objects; pass `brief=false` for full objects. Use
    `offset` to paginate, `fields`/`exclude` to project, `limit` capped at 100.
    """
    mappings = {
        "group_id": "group_id",
        "interface_type": "interface_type",
        "interface_id": "interface_id",
        "priority": "priority",
        "device": "device",
        "virtual_machine": "virtual_machine",
    }
    return await _search("ipam/fhrp-group-assignments/", args, mappings)


@mcp.tool(
    annotations={
        "title": "Get FHRP Group Assignment Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_fhrp_group_assignment_details(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Get FHRP group assignment by ID (ipam/fhrp-group-assignments/{id}/).
    Accepts: id (required)
        id: Numeric ID of the FHRP group assignment to fetch. Returns `[obj]` or `[]`.
    """
    if "id" not in args:
        return []
    return await _get_detail("ipam/fhrp-group-assignments/", args["id"], args)


# ipam/asns

@mcp.tool(
    annotations={
        "title": "Search ASNs",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_asns(args: Dict[str, Any]) -> Dict[str, Any]:
    """Search ASNs (ipam/asns/).
    Accepts: asn, rir, site, tenant, provider, tag, q, limit
        asn: ASN number (exact match)
        rir: RIR ID or slug
        site: Site ID or slug
        tenant: Tenant ID or slug
        provider: Provider ID or slug
        tag: Tag slug (single)
        q: Free-text search across description and asn
        limit: Maximum number of results to return (default 10)

    Returns `{count, results}` (NetBox total + page). Default `brief=true`
    for compact ASN objects; pass `brief=false` for full objects. Use
    `offset` to paginate, `fields`/`exclude` to project, `limit` capped at 100.
    """
    mappings = {
        "asn": "asn",
        "rir": "rir",
        "site": "site",
        "tenant": "tenant",
        "provider": "provider",
        "tag": "tag",
        "q": "q",
    }
    return await _search("ipam/asns/", args, mappings)


@mcp.tool(
    annotations={
        "title": "Get ASN Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_asn_details(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Get ASN by ID (ipam/asns/{id}/).
    Accepts: id (required)
        id: Numeric ID of the ASN to fetch. Returns `[obj]` or `[]`.
    """
    if "id" not in args:
        return []
    return await _get_detail("ipam/asns/", args["id"], args)


# ipam/asn-ranges

@mcp.tool(
    annotations={
        "title": "Search ASN Ranges",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_asn_ranges(args: Dict[str, Any]) -> Dict[str, Any]:
    """Search ASN ranges (ipam/asn-ranges/).
    Accepts: name, rir, tenant, start, end, tag, q, limit
        name: ASN range name (case-insensitive contains match)
        rir: RIR ID or slug
        tenant: Tenant ID or slug
        start: Range start ASN
        end: Range end ASN
        tag: Tag slug (single)
        q: Free-text search across name and description
        limit: Maximum number of results to return (default 10)

    Returns `{count, results}` (NetBox total + page). Default `brief=true`
    for compact ASN range objects; pass `brief=false` for full objects. Use
    `offset` to paginate, `fields`/`exclude` to project, `limit` capped at 100.
    """
    mappings = {
        "name": "name__ic",
        "rir": "rir",
        "tenant": "tenant",
        "start": "start",
        "end": "end",
        "tag": "tag",
        "q": "q",
    }
    return await _search("ipam/asn-ranges/", args, mappings)


@mcp.tool(
    annotations={
        "title": "Get ASN Range Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_asn_range_details(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Get ASN range by ID (ipam/asn-ranges/{id}/).
    Accepts: id (required)
        id: Numeric ID of the ASN range to fetch. Returns `[obj]` or `[]`.
    """
    if "id" not in args:
        return []
    return await _get_detail("ipam/asn-ranges/", args["id"], args)


# ipam/asn-ranges/{id}/available-asns

@mcp.tool(
    annotations={
        "title": "Get Available ASNs in ASN Range",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_asn_range_available_asns(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """List free ASNs inside an ASN range
    (ipam/asn-ranges/{id}/available-asns/).

    Accepts: id (required), limit
        id: Numeric ID of the ASN range
        limit: Maximum number of ASNs to return (default 10)

    Returns a list of available ASN candidates, or `[]`.
    """
    if "id" not in args:
        return []
    return await _get_list(f"ipam/asn-ranges/{args['id']}/available-asns/", args)


# ipam/vlan-groups

@mcp.tool(
    annotations={
        "title": "Search VLAN Groups",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_vlan_groups(args: Dict[str, Any]) -> Dict[str, Any]:
    """Search VLAN groups (ipam/vlan-groups/).
    Accepts: name, scope_type, site, region, location, rack, cluster,
             cluster_group, contains_vid, tag, q, limit
        name: VLAN group name (case-insensitive contains match)
        scope_type: Content type of the group's scope (e.g. 'dcim.site')
        site: Site ID
        region: Region ID
        location: Location ID
        rack: Rack ID
        cluster: Cluster ID
        cluster_group: Cluster group ID
        contains_vid: VID that the group's vid_ranges must contain
        tag: Tag slug (single)
        q: Free-text search across name and description
        limit: Maximum number of results to return (default 10)

    Returns `{count, results}` (NetBox total + page). Default `brief=true`
    for compact VLAN group objects; pass `brief=false` for full objects. Use
    `offset` to paginate, `fields`/`exclude` to project, `limit` capped at 100.
    """
    mappings = {
        "name": "name__ic",
        "scope_type": "scope_type",
        "site": "site",
        "region": "region",
        "location": "location",
        "rack": "rack",
        "cluster": "cluster",
        "cluster_group": "cluster_group",
        "contains_vid": "contains_vid",
        "tag": "tag",
        "q": "q",
    }
    return await _search("ipam/vlan-groups/", args, mappings)


@mcp.tool(
    annotations={
        "title": "Get VLAN Group Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_vlan_group_details(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Get VLAN group by ID (ipam/vlan-groups/{id}/).
    Accepts: id (required)
        id: Numeric ID of the VLAN group to fetch. Returns `[obj]` or `[]`.
    """
    if "id" not in args:
        return []
    return await _get_detail("ipam/vlan-groups/", args["id"], args)


# ipam/vlan-groups/{id}/available-vlans

@mcp.tool(
    annotations={
        "title": "Get Available VLANs in VLAN Group",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_vlan_group_available_vlans(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """List free VLAN VIDs inside a VLAN group
    (ipam/vlan-groups/{id}/available-vlans/).

    Accepts: id (required), limit
        id: Numeric ID of the VLAN group
        limit: Maximum number of VLANs to return (default 10)

    Returns a list of available VLAN candidates, or `[]`.
    """
    if "id" not in args:
        return []
    return await _get_list(f"ipam/vlan-groups/{args['id']}/available-vlans/", args)


# ipam/vlans

@mcp.tool(
    annotations={
        "title": "Search VLANs",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_vlans(args: Dict[str, Any]) -> Dict[str, Any]:
    """Search VLANs (ipam/vlans/).

    Accepts: vid, name, group, site, region, role, tenant, status,
             available_on_device, available_on_virtualmachine, qinq_role,
             l2vpn, tag, q, limit
        vid: VLAN ID (1-4094)
        name: VLAN name (case-insensitive contains match)
        group: VLAN group ID or slug
        site: Site ID or slug
        region: Region ID or slug
        role: IPAM role slug or ID
        tenant: Tenant ID or slug
        status: Status (e.g. 'active', 'reserved', 'deprecated')
        available_on_device: Device ID - return VLANs available on the device
        available_on_virtualmachine: VM ID - return VLANs available on the VM
        qinq_role: Q-in-Q role (e.g. 'svlan', 'cvlan')
        l2vpn: L2VPN identifier
        tag: Tag slug (single)
        q: Free-text search across name, vid, and description
        limit: Maximum number of results to return (default 10)

    Returns `{count, results}` (NetBox total + page). Default `brief=true`
    for compact VLAN objects; pass `brief=false` for full objects. Use
    `offset` to paginate, `fields`/`exclude` to project, `limit` capped at 100.
    """
    mappings = {
        "vid": "vid",
        "name": "name__ic",
        "group": "group",
        "site": "site",
        "region": "region",
        "role": "role",
        "tenant": "tenant",
        "status": "status",
        "available_on_device": "available_on_device",
        "available_on_virtualmachine": "available_on_virtualmachine",
        "qinq_role": "qinq_role",
        "l2vpn": "l2vpn",
        "tag": "tag",
        "q": "q",
    }
    return await _search("ipam/vlans/", args, mappings)


@mcp.tool(
    annotations={
        "title": "Get VLAN Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_vlan_details(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Get VLAN by ID (ipam/vlans/{id}/).
    Accepts: id (required)
        id: Numeric ID of the VLAN to fetch. Returns `[obj]` or `[]`.
    """
    if "id" not in args:
        return []
    return await _get_detail("ipam/vlans/", args["id"], args)


# ipam/vlan-translation-policies

@mcp.tool(
    annotations={
        "title": "Search VLAN Translation Policies",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_vlan_translation_policies(args: Dict[str, Any]) -> Dict[str, Any]:
    """Search VLAN translation policies (ipam/vlan-translation-policies/).
    Accepts: name, tag, q, limit
        name: Policy name (case-insensitive contains match)
        tag: Tag slug (single)
        q: Free-text search across name and description
        limit: Maximum number of results to return (default 10)

    Returns `{count, results}` (NetBox total + page). Default `brief=true`
    for compact VLAN translation policy objects; pass `brief=false` for full objects. Use
    `offset` to paginate, `fields`/`exclude` to project, `limit` capped at 100.
    """
    mappings = {
        "name": "name__ic",
        "tag": "tag",
        "q": "q",
    }
    return await _search("ipam/vlan-translation-policies/", args, mappings)


@mcp.tool(
    annotations={
        "title": "Get VLAN Translation Policy Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_vlan_translation_policy_details(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Get VLAN translation policy by ID
    (ipam/vlan-translation-policies/{id}/).
    Accepts: id (required)
        id: Numeric ID of the VLAN translation policy. Returns `[obj]` or `[]`.
    """
    if "id" not in args:
        return []
    return await _get_detail("ipam/vlan-translation-policies/", args["id"], args)


# ipam/vlan-translation-rules

@mcp.tool(
    annotations={
        "title": "Search VLAN Translation Rules",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_vlan_translation_rules(args: Dict[str, Any]) -> Dict[str, Any]:
    """Search VLAN translation rules (ipam/vlan-translation-rules/).
    Accepts: policy, local_vid, remote_vid, q, limit
        policy: Policy name or ID
        local_vid: Local VLAN VID
        remote_vid: Remote VLAN VID
        q: Free-text search across policy and VIDs
        limit: Maximum number of results to return (default 10)

    Returns `{count, results}` (NetBox total + page). Default `brief=true`
    for compact VLAN translation rule objects; pass `brief=false` for full objects. Use
    `offset` to paginate, `fields`/`exclude` to project, `limit` capped at 100.
    """
    mappings = {
        "policy": "policy",
        "local_vid": "local_vid",
        "remote_vid": "remote_vid",
        "q": "q",
    }
    return await _search("ipam/vlan-translation-rules/", args, mappings)


@mcp.tool(
    annotations={
        "title": "Get VLAN Translation Rule Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_vlan_translation_rule_details(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Get VLAN translation rule by ID (ipam/vlan-translation-rules/{id}/).
    Accepts: id (required)
        id: Numeric ID of the VLAN translation rule. Returns `[obj]` or `[]`.
    """
    if "id" not in args:
        return []
    return await _get_detail("ipam/vlan-translation-rules/", args["id"], args)


# ipam/service-templates

@mcp.tool(
    annotations={
        "title": "Search Service Templates",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_service_templates(args: Dict[str, Any]) -> Dict[str, Any]:
    """Search service templates (ipam/service-templates/).
    Accepts: name, protocol, port, tag, q, limit
        name: Template name (case-insensitive contains match)
        protocol: 'tcp', 'udp', or 'sctp'
        port: Numeric port (must be inside the template's ports list)
        tag: Tag slug (single)
        q: Free-text search across name and description
        limit: Maximum number of results to return (default 10)

    Returns `{count, results}` (NetBox total + page). Default `brief=true`
    for compact service template objects; pass `brief=false` for full objects. Use
    `offset` to paginate, `fields`/`exclude` to project, `limit` capped at 100.
    """
    mappings = {
        "name": "name__ic",
        "protocol": "protocol",
        "port": "port",
        "tag": "tag",
        "q": "q",
    }
    return await _search("ipam/service-templates/", args, mappings)


@mcp.tool(
    annotations={
        "title": "Get Service Template Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_service_template_details(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Get service template by ID (ipam/service-templates/{id}/).
    Accepts: id (required)
        id: Numeric ID of the service template. Returns `[obj]` or `[]`.
    """
    if "id" not in args:
        return []
    return await _get_detail("ipam/service-templates/", args["id"], args)


# ipam/services

@mcp.tool(
    annotations={
        "title": "Search Services",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_services(args: Dict[str, Any]) -> Dict[str, Any]:
    """Search services (ipam/services/).

    Accepts: name, protocol, port, device, virtual_machine, fhrpgroup,
             ip_address, parent_object_type, tenant, tag, q, limit
        name: Service name (case-insensitive contains match)
        protocol: 'tcp', 'udp', or 'sctp'
        port: Numeric port (must be in the service's ports list)
        device: Device name
        virtual_machine: Virtual machine name
        fhrpgroup: FHRP group name
        ip_address: IP address ID
        parent_object_type: Content type of the parent (e.g. 'dcim.device')
        tenant: Tenant ID or slug
        tag: Tag slug (single)
        q: Free-text search across name and description
        limit: Maximum number of results to return (default 10)

    Returns `{count, results}` (NetBox total + page). Default `brief=true`
    for compact service objects; pass `brief=false` for full objects. Use
    `offset` to paginate, `fields`/`exclude` to project, `limit` capped at 100.
    """
    mappings = {
        "name": "name__ic",
        "protocol": "protocol",
        "port": "port",
        "device": "device",
        "virtual_machine": "virtual_machine",
        "fhrpgroup": "fhrpgroup",
        "ip_address": "ip_address",
        "parent_object_type": "parent_object_type",
        "tenant": "tenant",
        "tag": "tag",
        "q": "q",
    }
    return await _search("ipam/services/", args, mappings)


@mcp.tool(
    annotations={
        "title": "Get Service Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_service_details(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Get service by ID (ipam/services/{id}/).
    Accepts: id (required)
        id: Numeric ID of the service to fetch. Returns `[obj]` or `[]`.
    """
    if "id" not in args:
        return []
    return await _get_detail("ipam/services/", args["id"], args)




if __name__ == "__main__":
    host = os.getenv("MCP_HOST", "0.0.0.0")

    port_env = os.getenv("MCP_PORT")
