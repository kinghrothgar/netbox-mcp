"""Tools for the NetBox vpn app."""

from typing import Any, Dict, List

from ..helpers import _get_detail, _get_list, _search  # noqa: F401
from ..server import mcp


# --- vpn (tunnels, IKE/IPsec, L2VPN) ---

# vpn/tunnel-groups

@mcp.tool(
    annotations={
        "title": "Search Tunnel Groups",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_tunnel_groups(args: Dict[str, Any]) -> Dict[str, Any]:
    """Search tunnel groups (vpn/tunnel-groups/).
    Accepts: name, slug, q, tag, limit
        name: Tunnel group name (case-insensitive contains match)
        slug: Tunnel group slug (exact match)
        q: Free-text search across name and description
        tag: Tag slug (single)
        limit: Maximum number of results to return (default 10)

    Returns `{count, results}` (NetBox total + page). Default `brief=true`
    for compact tunnel group objects; pass `brief=false` for full objects. Use
    `offset` to paginate, `fields`/`exclude` to project, `limit` capped at 100.
    """
    mappings = {
        "name": "name__ic",
        "slug": "slug",
        "q": "q",
        "tag": "tag",
    }
    return await _search("vpn/tunnel-groups/", args, mappings)


@mcp.tool(
    annotations={
        "title": "Get Tunnel Group Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_tunnel_group_details(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Get tunnel group by ID (vpn/tunnel-groups/{id}/).
    Accepts: id (required)
        id: Numeric ID of the tunnel group to fetch. Returns `[obj]` or `[]`.
    """
    if "id" not in args:
        return []
    return await _get_detail("vpn/tunnel-groups/", args["id"], args)


# vpn/tunnels

@mcp.tool(
    annotations={
        "title": "Search Tunnels",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_tunnels(args: Dict[str, Any]) -> Dict[str, Any]:
    """Search tunnels (vpn/tunnels/).
    Accepts: name, status, tunnel_id, group, encapsulation, ipsec_profile,
             tenant, q, tag, limit
        name: Tunnel name (case-insensitive contains match)
        status: Status (e.g. 'planned', 'active', 'disabled')
        tunnel_id: Numeric tunnel identifier
        group: Tunnel group ID or slug
        encapsulation: 'ipsec-transport', 'ipsec-tunnel', 'ip-ip', 'gre', etc.
        ipsec_profile: IPsec profile ID
        tenant: Tenant ID or slug
        q: Free-text search across name and description
        tag: Tag slug (single)
        limit: Maximum number of results to return (default 10)

    Returns `{count, results}` (NetBox total + page). Default `brief=true`
    for compact tunnel objects; pass `brief=false` for full objects. Use
    `offset` to paginate, `fields`/`exclude` to project, `limit` capped at 100.
    """
    mappings = {
        "name": "name__ic",
        "status": "status",
        "tunnel_id": "tunnel_id",
        "group": "group",
        "encapsulation": "encapsulation",
        "ipsec_profile": "ipsec_profile",
        "tenant": "tenant",
        "q": "q",
        "tag": "tag",
    }
    return await _search("vpn/tunnels/", args, mappings)


@mcp.tool(
    annotations={
        "title": "Get Tunnel Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_tunnel_details(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Get tunnel by ID (vpn/tunnels/{id}/).
    Accepts: id (required)
        id: Numeric ID of the tunnel to fetch. Returns `[obj]` or `[]`.
    """
    if "id" not in args:
        return []
    return await _get_detail("vpn/tunnels/", args["id"], args)


# vpn/tunnel-terminations

@mcp.tool(
    annotations={
        "title": "Search Tunnel Terminations",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_tunnel_terminations(args: Dict[str, Any]) -> Dict[str, Any]:
    """Search tunnel terminations (vpn/tunnel-terminations/).
    Accepts: tunnel, role, termination_type, interface, vminterface,
             outside_ip, q, tag, limit
        tunnel: Tunnel ID or name
        role: 'peer', 'hub', or 'spoke'
        termination_type: Content type of the termination
        interface: Device interface ID
        vminterface: VM interface ID
        outside_ip: Outside IP address ID
        q: Free-text search
        tag: Tag slug (single)
        limit: Maximum number of results to return (default 10)

    Returns `{count, results}` (NetBox total + page). Default `brief=true`
    for compact tunnel termination objects; pass `brief=false` for full objects. Use
    `offset` to paginate, `fields`/`exclude` to project, `limit` capped at 100.
    """
    mappings = {
        "tunnel": "tunnel",
        "role": "role",
        "termination_type": "termination_type",
        "interface": "interface_id",
        "vminterface": "vminterface_id",
        "outside_ip": "outside_ip_id",
        "q": "q",
        "tag": "tag",
    }
    return await _search("vpn/tunnel-terminations/", args, mappings)


@mcp.tool(
    annotations={
        "title": "Get Tunnel Termination Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_tunnel_termination_details(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Get tunnel termination by ID (vpn/tunnel-terminations/{id}/).
    Accepts: id (required)
        id: Numeric ID of the tunnel termination to fetch. Returns `[obj]` or `[]`.
    """
    if "id" not in args:
        return []
    return await _get_detail("vpn/tunnel-terminations/", args["id"], args)


# vpn/ike-proposals

@mcp.tool(
    annotations={
        "title": "Search IKE Proposals",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_ike_proposals(args: Dict[str, Any]) -> Dict[str, Any]:
    """Search IKE proposals (vpn/ike-proposals/).
    Accepts: name, authentication_method, encryption_algorithm,
             authentication_algorithm, group, sa_lifetime, q, tag, limit
        name: Proposal name (case-insensitive contains match)
        authentication_method: e.g. 'preshared-keys', 'certificates', 'rsa-signatures'
        encryption_algorithm: e.g. 'aes-128-cbc', 'aes-256-gcm'
        authentication_algorithm: e.g. 'hmac-sha1', 'hmac-sha256'
        group: Diffie-Hellman group number
        sa_lifetime: SA lifetime in seconds
        q: Free-text search
        tag: Tag slug (single)
        limit: Maximum number of results to return (default 10)

    Returns `{count, results}` (NetBox total + page). Default `brief=true`
    for compact IKE proposal objects; pass `brief=false` for full objects. Use
    `offset` to paginate, `fields`/`exclude` to project, `limit` capped at 100.
    """
    mappings = {
        "name": "name__ic",
        "authentication_method": "authentication_method",
        "encryption_algorithm": "encryption_algorithm",
        "authentication_algorithm": "authentication_algorithm",
        "group": "group",
        "sa_lifetime": "sa_lifetime",
        "q": "q",
        "tag": "tag",
    }
    return await _search("vpn/ike-proposals/", args, mappings)


@mcp.tool(
    annotations={
        "title": "Get IKE Proposal Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_ike_proposal_details(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Get IKE proposal by ID (vpn/ike-proposals/{id}/).
    Accepts: id (required)
        id: Numeric ID of the IKE proposal to fetch. Returns `[obj]` or `[]`.
    """
    if "id" not in args:
        return []
    return await _get_detail("vpn/ike-proposals/", args["id"], args)


# vpn/ike-policies

@mcp.tool(
    annotations={
        "title": "Search IKE Policies",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_ike_policies(args: Dict[str, Any]) -> Dict[str, Any]:
    """Search IKE policies (vpn/ike-policies/).
    Accepts: name, version, mode, proposal, q, tag, limit
        name: Policy name (case-insensitive contains match)
        version: 1 or 2
        mode: 'main' or 'aggressive'
        proposal: IKE proposal ID
        q: Free-text search
        tag: Tag slug (single)
        limit: Maximum number of results to return (default 10)

    Returns `{count, results}` (NetBox total + page). Default `brief=true`
    for compact IKE policy objects; pass `brief=false` for full objects. Use
    `offset` to paginate, `fields`/`exclude` to project, `limit` capped at 100.
    """
    mappings = {
        "name": "name__ic",
        "version": "version",
        "mode": "mode",
        "proposal": "proposal",
        "q": "q",
        "tag": "tag",
    }
    return await _search("vpn/ike-policies/", args, mappings)


@mcp.tool(
    annotations={
        "title": "Get IKE Policy Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_ike_policy_details(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Get IKE policy by ID (vpn/ike-policies/{id}/).
    Accepts: id (required)
        id: Numeric ID of the IKE policy to fetch. Returns `[obj]` or `[]`.
    """
    if "id" not in args:
        return []
    return await _get_detail("vpn/ike-policies/", args["id"], args)


# vpn/ipsec-proposals

@mcp.tool(
    annotations={
        "title": "Search IPsec Proposals",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_ipsec_proposals(args: Dict[str, Any]) -> Dict[str, Any]:
    """Search IPsec proposals (vpn/ipsec-proposals/).
    Accepts: name, encryption_algorithm, authentication_algorithm,
             sa_lifetime_seconds, sa_lifetime_data, q, tag, limit
        name: Proposal name (case-insensitive contains match)
        encryption_algorithm: e.g. 'aes-256-gcm'
        authentication_algorithm: e.g. 'hmac-sha256'
        sa_lifetime_seconds: SA lifetime in seconds
        sa_lifetime_data: SA lifetime in KB
        q: Free-text search
        tag: Tag slug (single)
        limit: Maximum number of results to return (default 10)

    Returns `{count, results}` (NetBox total + page). Default `brief=true`
    for compact IPsec proposal objects; pass `brief=false` for full objects. Use
    `offset` to paginate, `fields`/`exclude` to project, `limit` capped at 100.
    """
    mappings = {
        "name": "name__ic",
        "encryption_algorithm": "encryption_algorithm",
        "authentication_algorithm": "authentication_algorithm",
        "sa_lifetime_seconds": "sa_lifetime_seconds",
        "sa_lifetime_data": "sa_lifetime_data",
        "q": "q",
        "tag": "tag",
    }
    return await _search("vpn/ipsec-proposals/", args, mappings)


@mcp.tool(
    annotations={
        "title": "Get IPsec Proposal Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_ipsec_proposal_details(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Get IPsec proposal by ID (vpn/ipsec-proposals/{id}/).
    Accepts: id (required)
        id: Numeric ID of the IPsec proposal to fetch. Returns `[obj]` or `[]`.
    """
    if "id" not in args:
        return []
    return await _get_detail("vpn/ipsec-proposals/", args["id"], args)


# vpn/ipsec-policies

@mcp.tool(
    annotations={
        "title": "Search IPsec Policies",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_ipsec_policies(args: Dict[str, Any]) -> Dict[str, Any]:
    """Search IPsec policies (vpn/ipsec-policies/).
    Accepts: name, pfs_group, proposal, q, tag, limit
        name: Policy name (case-insensitive contains match)
        pfs_group: Perfect Forward Secrecy group number
        proposal: IPsec proposal ID
        q: Free-text search
        tag: Tag slug (single)
        limit: Maximum number of results to return (default 10)

    Returns `{count, results}` (NetBox total + page). Default `brief=true`
    for compact IPsec policy objects; pass `brief=false` for full objects. Use
    `offset` to paginate, `fields`/`exclude` to project, `limit` capped at 100.
    """
    mappings = {
        "name": "name__ic",
        "pfs_group": "pfs_group",
        "proposal": "proposal",
        "q": "q",
        "tag": "tag",
    }
    return await _search("vpn/ipsec-policies/", args, mappings)


@mcp.tool(
    annotations={
        "title": "Get IPsec Policy Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_ipsec_policy_details(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Get IPsec policy by ID (vpn/ipsec-policies/{id}/).
    Accepts: id (required)
        id: Numeric ID of the IPsec policy to fetch. Returns `[obj]` or `[]`.
    """
    if "id" not in args:
        return []
    return await _get_detail("vpn/ipsec-policies/", args["id"], args)


# vpn/ipsec-profiles

@mcp.tool(
    annotations={
        "title": "Search IPsec Profiles",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_ipsec_profiles(args: Dict[str, Any]) -> Dict[str, Any]:
    """Search IPsec profiles (vpn/ipsec-profiles/).
    Accepts: name, mode, ike_policy, ipsec_policy, q, tag, limit
        name: Profile name (case-insensitive contains match)
        mode: 'esp' or 'ah'
        ike_policy: IKE policy ID
        ipsec_policy: IPsec policy ID
        q: Free-text search
        tag: Tag slug (single)
        limit: Maximum number of results to return (default 10)

    Returns `{count, results}` (NetBox total + page). Default `brief=true`
    for compact IPsec profile objects; pass `brief=false` for full objects. Use
    `offset` to paginate, `fields`/`exclude` to project, `limit` capped at 100.
    """
    mappings = {
        "name": "name__ic",
        "mode": "mode",
        "ike_policy": "ike_policy",
        "ipsec_policy": "ipsec_policy",
        "q": "q",
        "tag": "tag",
    }
    return await _search("vpn/ipsec-profiles/", args, mappings)


@mcp.tool(
    annotations={
        "title": "Get IPsec Profile Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_ipsec_profile_details(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Get IPsec profile by ID (vpn/ipsec-profiles/{id}/).
    Accepts: id (required)
        id: Numeric ID of the IPsec profile to fetch. Returns `[obj]` or `[]`.
    """
    if "id" not in args:
        return []
    return await _get_detail("vpn/ipsec-profiles/", args["id"], args)


# vpn/l2vpns

@mcp.tool(
    annotations={
        "title": "Search L2VPNs",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_l2vpns(args: Dict[str, Any]) -> Dict[str, Any]:
    """Search L2VPNs (vpn/l2vpns/).
    Accepts: name, slug, identifier, type, status, import_target,
             export_target, tenant, q, tag, limit
        name: L2VPN name (case-insensitive contains match)
        slug: L2VPN slug (exact match)
        identifier: Numeric identifier (e.g. VNI for VXLAN)
        type: e.g. 'vpws', 'vpls', 'evpn', 'mpls-evpn', 'vxlan', 'vxlan-evpn'
        status: Status (e.g. 'active', 'planned')
        import_target: Route target name for import
        export_target: Route target name for export
        tenant: Tenant ID or slug
        q: Free-text search across name and description
        tag: Tag slug (single)
        limit: Maximum number of results to return (default 10)

    Returns `{count, results}` (NetBox total + page). Default `brief=true`
    for compact L2VPN objects; pass `brief=false` for full objects. Use
    `offset` to paginate, `fields`/`exclude` to project, `limit` capped at 100.
    """
    mappings = {
        "name": "name__ic",
        "slug": "slug",
        "identifier": "identifier",
        "type": "type",
        "status": "status",
        "import_target": "import_target",
        "export_target": "export_target",
        "tenant": "tenant",
        "q": "q",
        "tag": "tag",
    }
    return await _search("vpn/l2vpns/", args, mappings)


@mcp.tool(
    annotations={
        "title": "Get L2VPN Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_l2vpn_details(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Get L2VPN by ID (vpn/l2vpns/{id}/).
    Accepts: id (required)
        id: Numeric ID of the L2VPN to fetch. Returns `[obj]` or `[]`.
    """
    if "id" not in args:
        return []
    return await _get_detail("vpn/l2vpns/", args["id"], args)


# vpn/l2vpn-terminations

@mcp.tool(
    annotations={
        "title": "Search L2VPN Terminations",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_l2vpn_terminations(args: Dict[str, Any]) -> Dict[str, Any]:
    """Search L2VPN terminations (vpn/l2vpn-terminations/).
    Accepts: l2vpn, assigned_object_type, device, virtual_machine,
             interface, vminterface, vlan, vlan_vid, region, site,
             q, tag, limit
        l2vpn: L2VPN ID or slug
        assigned_object_type: Content type of the assigned object
        device: Device ID
        virtual_machine: Virtual machine ID
        interface: Interface ID
        vminterface: VM interface ID
        vlan: VLAN ID
        vlan_vid: VLAN VID
        region: Region ID or slug
        site: Site ID or slug
        q: Free-text search
        tag: Tag slug (single)
        limit: Maximum number of results to return (default 10)

    Returns `{count, results}` (NetBox total + page). Default `brief=true`
    for compact L2VPN termination objects; pass `brief=false` for full objects. Use
    `offset` to paginate, `fields`/`exclude` to project, `limit` capped at 100.
    """
    mappings = {
        "l2vpn": "l2vpn",
        "assigned_object_type": "assigned_object_type",
        "device": "device_id",
        "virtual_machine": "virtual_machine_id",
        "interface": "interface_id",
        "vminterface": "vminterface_id",
        "vlan": "vlan_id",
        "vlan_vid": "vlan_vid",
        "region": "region",
        "site": "site",
        "q": "q",
        "tag": "tag",
    }
    return await _search("vpn/l2vpn-terminations/", args, mappings)


@mcp.tool(
    annotations={
        "title": "Get L2VPN Termination Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_l2vpn_termination_details(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Get L2VPN termination by ID (vpn/l2vpn-terminations/{id}/).
    Accepts: id (required)
        id: Numeric ID of the L2VPN termination to fetch. Returns `[obj]` or `[]`.
    """
    if "id" not in args:
        return []
    return await _get_detail("vpn/l2vpn-terminations/", args["id"], args)
