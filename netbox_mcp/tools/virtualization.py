"""Tools for the NetBox virtualization app."""

from typing import Any, Dict

from ..helpers import _get_detail, _get_list, _search  # noqa: F401
from ..server import mcp
from ..version import is_at_least, version_gated_tool


# --- virtualization (clusters, virtual machines, etc.) ---

# virtualization/cluster-types

@mcp.tool(
    annotations={
        "title": "Search Cluster Types",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_cluster_types(args: Dict[str, Any]) -> Dict[str, Any]:
    """Search cluster types (virtualization/cluster-types/).
    Accepts: name, slug, q, tag, limit
        name: Name of the cluster type (case-insensitive contains match)
        slug: Cluster type slug (exact match)
        q: Free-text search across name and description
        tag: Tag slug (single)
        limit: Maximum number of results to return (default 10)

    Returns `{count, results}` (NetBox total + page). Default `brief=true`
    for compact cluster type objects; pass `brief=false` for full objects. Use
    `offset` to paginate, `fields`/`exclude` to project, `limit` capped at 100.
    """
    mappings = {
        "name": "name__ic",
        "slug": "slug",
        "q": "q",
        "tag": "tag",
    }
    return await _search("virtualization/cluster-types/", args, mappings)


@mcp.tool(
    annotations={
        "title": "Get Cluster Type Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_cluster_type_details(args: Dict[str, Any]) -> Dict[str, Any]:
    """Get cluster type by ID (virtualization/cluster-types/{id}/).
    Accepts: id (required)
        id: Numeric ID of the cluster type to fetch. Returns the envelope `{"results": [obj]}` or `{"results": []}`.
    """
    if "id" not in args:
        return {"results": []}
    return await _get_detail("virtualization/cluster-types/", args["id"], args)


# virtualization/cluster-groups

@mcp.tool(
    annotations={
        "title": "Search Cluster Groups",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_cluster_groups(args: Dict[str, Any]) -> Dict[str, Any]:
    """Search cluster groups (virtualization/cluster-groups/).
    Accepts: name, slug, contact, contact_group, q, tag, limit
        name: Name of the cluster group (case-insensitive contains match)
        slug: Cluster group slug (exact match)
        contact: Contact ID
        contact_group: Contact group ID or slug
        q: Free-text search across name and description
        tag: Tag slug (single)
        limit: Maximum number of results to return (default 10)

    Returns `{count, results}` (NetBox total + page). Default `brief=true`
    for compact cluster group objects; pass `brief=false` for full objects. Use
    `offset` to paginate, `fields`/`exclude` to project, `limit` capped at 100.
    """
    mappings = {
        "name": "name__ic",
        "slug": "slug",
        "contact": "contact",
        "contact_group": "contact_group",
        "q": "q",
        "tag": "tag",
    }
    return await _search("virtualization/cluster-groups/", args, mappings)


@mcp.tool(
    annotations={
        "title": "Get Cluster Group Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_cluster_group_details(args: Dict[str, Any]) -> Dict[str, Any]:
    """Get cluster group by ID (virtualization/cluster-groups/{id}/).
    Accepts: id (required)
        id: Numeric ID of the cluster group to fetch. Returns the envelope `{"results": [obj]}` or `{"results": []}`.
    """
    if "id" not in args:
        return {"results": []}
    return await _get_detail("virtualization/cluster-groups/", args["id"], args)


# virtualization/clusters

@mcp.tool(
    annotations={
        "title": "Search Clusters",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_clusters(args: Dict[str, Any]) -> Dict[str, Any]:
    """Search clusters (virtualization/clusters/).
    Accepts: name, group, type, status, site, region, site_group, location,
             tenant, tenant_group, q, tag, limit
        name: Name of the cluster (case-insensitive contains match)
        group: Cluster group ID or slug
        type: Cluster type ID or slug
        status: Status (e.g. 'active', 'planned', 'staging', 'decommissioning', 'offline')
        site: Site ID or slug
        region: Region ID or slug
        site_group: Site group ID or slug
        location: Location ID or slug
        tenant: Tenant ID or slug
        tenant_group: Tenant group ID or slug
        q: Free-text search across name and description
        tag: Tag slug (single)
        limit: Maximum number of results to return (default 10)

    Returns `{count, results}` (NetBox total + page). Default `brief=true`
    for compact cluster objects; pass `brief=false` for full objects. Use
    `offset` to paginate, `fields`/`exclude` to project, `limit` capped at 100.
    """
    mappings = {
        "name": "name__ic",
        "group": "group",
        "type": "type",
        "status": "status",
        "site": "site",
        "region": "region",
        "site_group": "site_group",
        "location": "location",
        "tenant": "tenant",
        "tenant_group": "tenant_group",
        "q": "q",
        "tag": "tag",
    }
    return await _search("virtualization/clusters/", args, mappings)


@mcp.tool(
    annotations={
        "title": "Get Cluster Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_cluster_details(args: Dict[str, Any]) -> Dict[str, Any]:
    """Get cluster by ID (virtualization/clusters/{id}/).
    Accepts: id (required)
        id: Numeric ID of the cluster to fetch. Returns the envelope `{"results": [obj]}` or `{"results": []}`.
    """
    if "id" not in args:
        return {"results": []}
    return await _get_detail("virtualization/clusters/", args["id"], args)


# virtualization/virtual-machine-types  (NetBox 4.6+)

@version_gated_tool(
    mcp,
    min_version=(4, 6),
    annotations={
        "title": "Search Virtual Machine Types",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_virtual_machine_types(args: Dict[str, Any]) -> Dict[str, Any]:
    """Search virtual machine types (virtualization/virtual-machine-types/).
    Accepts: name, slug, default_platform, q, tag, limit
        name: Name of the VM type (case-insensitive contains match)
        slug: VM type slug (exact match)
        default_platform: Platform ID or slug
        q: Free-text search across name and description
        tag: Tag slug (single)
        limit: Maximum number of results to return (default 10)

    Returns `{count, results}` (NetBox total + page). Default `brief=true`
    for compact virtual machine type objects; pass `brief=false` for full objects. Use
    `offset` to paginate, `fields`/`exclude` to project, `limit` capped at 100.
    """
    mappings = {
        "name": "name__ic",
        "slug": "slug",
        "default_platform": "default_platform",
        "q": "q",
        "tag": "tag",
    }
    return await _search("virtualization/virtual-machine-types/", args, mappings)


@version_gated_tool(
    mcp,
    min_version=(4, 6),
    annotations={
        "title": "Get Virtual Machine Type Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_virtual_machine_type_details(args: Dict[str, Any]) -> Dict[str, Any]:
    """Get virtual machine type by ID (virtualization/virtual-machine-types/{id}/).
    Accepts: id (required)
        id: Numeric ID of the virtual machine type to fetch. Returns the envelope `{"results": [obj]}` or `{"results": []}`.
    """
    if "id" not in args:
        return {"results": []}
    return await _get_detail("virtualization/virtual-machine-types/", args["id"], args)


# virtualization/virtual-machines

@mcp.tool(
    annotations={
        "title": "Search Virtual Machines",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_virtual_machines(args: Dict[str, Any]) -> Dict[str, Any]:
    """Search virtual machines (virtualization/virtual-machines/).
    Accepts: name, cluster, cluster_group, cluster_type, device, site, region,
             site_group, tenant, role, platform, status, mac_address,
             has_primary_ip, virtual_machine_type (NetBox 4.6+),
             config_template, q, tag, limit
        name: Name of the virtual machine (case-insensitive contains match)
        cluster: Cluster ID or name (optional on NetBox 4.6+: a VM may be
                 attached to a device without a cluster)
        cluster_group: Cluster group ID or slug
        cluster_type: Cluster type ID or slug
        device: Host device ID or name
        site: Site ID or slug
        region: Region ID or slug
        site_group: Site group ID or slug
        tenant: Tenant ID or slug
        role: Device role ID or slug
        platform: Platform ID or slug
        status: Status (e.g. 'active', 'planned', 'staged', 'offline',
                'failed', 'decommissioning')
        mac_address: MAC address (exact match)
        has_primary_ip: Boolean - whether the VM has a primary IP assigned
        virtual_machine_type: Virtual machine type ID or slug (NetBox 4.6+;
                              ignored on older releases)
        config_template: Config template ID
        q: Free-text search across name, comments, and description
        tag: Tag slug (single)
        limit: Maximum number of results to return (default 10)

    Returns `{count, results}` (NetBox total + page). Default `brief=true`
    for compact virtual machine objects; pass `brief=false` for full objects. Use
    `offset` to paginate, `fields`/`exclude` to project, `limit` capped at 100.
    """
    mappings = {
        "name": "name__ic",
        "cluster": "cluster",
        "cluster_group": "cluster_group",
        "cluster_type": "cluster_type",
        "device": "device",
        "site": "site",
        "region": "region",
        "site_group": "site_group",
        "tenant": "tenant",
        "role": "role",
        "platform": "platform",
        "status": "status",
        "mac_address": "mac_address",
        "has_primary_ip": "has_primary_ip",
        "config_template": "config_template",
        "q": "q",
        "tag": "tag",
    }
    # virtual_machine_type was introduced alongside the VirtualMachineType
    # model in NetBox 4.6. Forwarding it on 4.5 would either be silently
    # ignored or produce a confusing error; gate it explicitly.
    if is_at_least(4, 6):
        mappings["virtual_machine_type"] = "virtual_machine_type"
    return await _search("virtualization/virtual-machines/", args, mappings)


@mcp.tool(
    annotations={
        "title": "Get Virtual Machine Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_virtual_machine_details(args: Dict[str, Any]) -> Dict[str, Any]:
    """Get virtual machine by ID (virtualization/virtual-machines/{id}/).
    Accepts: id (required)
        id: Numeric ID of the virtual machine to fetch. Returns the envelope `{"results": [obj]}` or `{"results": []}`.
    """
    if "id" not in args:
        return {"results": []}
    return await _get_detail("virtualization/virtual-machines/", args["id"], args)


# virtualization/interfaces

@mcp.tool(
    annotations={
        "title": "Search VM Interfaces",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_vm_interfaces(args: Dict[str, Any]) -> Dict[str, Any]:
    """Search VM interfaces (virtualization/interfaces/).
    Accepts: name, virtual_machine, cluster, enabled, mtu, mode, parent,
             bridge, mac_address, vrf, q, tag, limit
        name: Interface name (case-insensitive contains match)
        virtual_machine: Virtual machine ID or name
        cluster: Cluster ID or name
        enabled: Boolean - whether the interface is enabled
        mtu: MTU value (exact match)
        mode: 'access', 'tagged', or 'tagged-all'
        parent: Parent interface ID
        bridge: Bridge interface ID
        mac_address: MAC address (exact match)
        vrf: VRF RD or ID
        q: Free-text search across name and description
        tag: Tag slug (single)
        limit: Maximum number of results to return (default 10)

    Returns `{count, results}` (NetBox total + page). Default `brief=true`
    for compact VM interface objects; pass `brief=false` for full objects. Use
    `offset` to paginate, `fields`/`exclude` to project, `limit` capped at 100.
    """
    mappings = {
        "name": "name__ic",
        "virtual_machine": "virtual_machine",
        "cluster": "cluster",
        "enabled": "enabled",
        "mtu": "mtu",
        "mode": "mode",
        "parent": "parent",
        "bridge": "bridge",
        "mac_address": "mac_address",
        "vrf": "vrf",
        "q": "q",
        "tag": "tag",
    }
    return await _search("virtualization/interfaces/", args, mappings)


@mcp.tool(
    annotations={
        "title": "Get VM Interface Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_vm_interface_details(args: Dict[str, Any]) -> Dict[str, Any]:
    """Get VM interface by ID (virtualization/interfaces/{id}/).
    Accepts: id (required)
        id: Numeric ID of the VM interface to fetch. Returns the envelope `{"results": [obj]}` or `{"results": []}`.
    """
    if "id" not in args:
        return {"results": []}
    return await _get_detail("virtualization/interfaces/", args["id"], args)


# virtualization/virtual-disks

@mcp.tool(
    annotations={
        "title": "Search Virtual Disks",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_virtual_disks(args: Dict[str, Any]) -> Dict[str, Any]:
    """Search virtual disks (virtualization/virtual-disks/).
    Accepts: name, virtual_machine, size, q, tag, limit
        name: Disk name (case-insensitive contains match)
        virtual_machine: Virtual machine ID or name
        size: Disk size in MB (exact match)
        q: Free-text search across name and description
        tag: Tag slug (single)
        limit: Maximum number of results to return (default 10)

    Returns `{count, results}` (NetBox total + page). Default `brief=true`
    for compact virtual disk objects; pass `brief=false` for full objects. Use
    `offset` to paginate, `fields`/`exclude` to project, `limit` capped at 100.
    """
    mappings = {
        "name": "name__ic",
        "virtual_machine": "virtual_machine",
        "size": "size",
        "q": "q",
        "tag": "tag",
    }
    return await _search("virtualization/virtual-disks/", args, mappings)


@mcp.tool(
    annotations={
        "title": "Get Virtual Disk Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_virtual_disk_details(args: Dict[str, Any]) -> Dict[str, Any]:
    """Get virtual disk by ID (virtualization/virtual-disks/{id}/).
    Accepts: id (required)
        id: Numeric ID of the virtual disk to fetch. Returns the envelope `{"results": [obj]}` or `{"results": []}`.
    """
    if "id" not in args:
        return {"results": []}
    return await _get_detail("virtualization/virtual-disks/", args["id"], args)
