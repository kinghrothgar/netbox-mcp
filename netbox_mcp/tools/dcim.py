"""Tools for the NetBox dcim app."""

from typing import Any, Dict, List

from ..helpers import _get_action, _get_detail, _get_list, _search
from ..server import mcp


# --- dcim (sites, site-groups, devices, etc.) ---

# dcim

# dcim/sites

@mcp.tool(
    annotations={
        "title": "Search Sites",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_sites(args: Dict[str, Any]) -> Dict[str, Any]:
    """Search sites (dcim/sites/).
    Accepts: name, status, location, region, limit
        name: Name of the site (case-insensitive search contains)
        status: Status of the site (exact match), e.g., 'active', 'planned', 'retired'
        location: Location name (case-insensitive search contains)
        region: Name of the region (case-insensitive search contains)
        limit: Maximum number of results to return (default 10)
    
    Returns `{count, results}` (NetBox total + page). Default `brief=true`
    for compact site objects; pass `brief=false` for full objects. Use
    `offset` to paginate, `fields`/`exclude` to project, `limit` capped at 100.
    """
    mappings = {"name": "name__ic", "status": "status", "location": "location__ic", "region": "region__ic"}
    return await _search("dcim/sites/", args, mappings)

@mcp.tool(
    annotations={
        "title": "Get Site Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_site_details(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Get site by ID (dcim/sites/).
    Accepts: id
        id: ID of the site - can be obtained from search_sites
    """
    if "id" not in args:
        return []
    return await _get_detail("dcim/sites/", args["id"], args)


@mcp.tool(
    annotations={
        "title": "Search Site Groups",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_site_groups(args: Dict[str, Any]) -> Dict[str, Any]:
    """Search site groups (dcim/site-groups/).
    Accepts: name, limit
        name: Name of the site group (case-insensitive contains match)
        limit: maximum number of results to return (default 10)

    Returns `{count, results}` (NetBox total + page). Default `brief=true`
    for compact site group objects; pass `brief=false` for full objects. Use
    `offset` to paginate, `fields`/`exclude` to project, `limit` capped at 100.
    """
    mappings = {"name": "name__ic"}
    return await _search("dcim/site-groups/", args, mappings)


@mcp.tool(
    annotations={
        "title": "Get Site Group Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_site_group_details(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Get site group details by ID (dcim/site-groups/{id}/).
    Accepts: id (required)
        id: Numeric ID of the site group to fetch. When provided, the tool will call
            the single-object endpoint and return a single-element list `[obj]` or `[]` if
            not found.
    """
    if "id" not in args:
        return []
    return await _get_detail("dcim/site-groups/", args["id"], args)


# dcim/cables

@mcp.tool(
    annotations={
        "title": "Search Cables",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_cables(args: Dict[str, Any]) -> Dict[str, Any]:
    """Search cables (dcim/cables/).
    Accepts: status, type, label, device, location, limit
        status: Status of the cable (exact match), e.g., 'connected', 'planned', 'decommissioning'
        type: Cable type (case-insensitive contains match), e.g., 'cat5e', 'cat6', 'fiber'
        label: Cable label (case-insensitive contains match)
        device: Device ID (numeric)
        location: Location ID (numeric)
        limit: Maximum number of results to return (default 10)
    
    Returns `{count, results}` (NetBox total + page). Default `brief=true`
    for compact cable objects; pass `brief=false` for full objects. Use
    `offset` to paginate, `fields`/`exclude` to project, `limit` capped at 100.
    """
    mappings = {
        "status": "status",
        "type": "type__ic",
        "label": "label__ic",
        "device": "device_id",
        "location": "location_id"
    }
    return await _search("dcim/cables/", args, mappings)


@mcp.tool(
    annotations={
        "title": "Get Cable Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_cable_details(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Get cable by ID (dcim/cables/{id}/).
    Accepts: id (required)
        id: Numeric ID of the cable to fetch. Returns `[obj]` or `[]`.
    """
    if "id" not in args:
        return []
    return await _get_detail("dcim/cables/", args["id"], args)


# dcim/console-ports

@mcp.tool(
    annotations={
        "title": "Search Console Ports",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_console_ports(args: Dict[str, Any]) -> Dict[str, Any]:
    """Search console ports (dcim/console-ports/).
    Accepts: name, device, type, label, limit
        name: Name of the console port (case-insensitive contains match)
        device: Device ID (numeric)
        type: Console port type (case-insensitive contains match)
        label: Console port label (case-insensitive contains match)
        limit: Maximum number of results to return (default 10)
    
    Returns `{count, results}` (NetBox total + page). Default `brief=true`
    for compact console port objects; pass `brief=false` for full objects. Use
    `offset` to paginate, `fields`/`exclude` to project, `limit` capped at 100.
    """
    mappings = {
        "name": "name__ic",
        "device": "device_id",
        "type": "type__ic",
        "label": "label__ic"
    }
    return await _search("dcim/console-ports/", args, mappings)


@mcp.tool(
    annotations={
        "title": "Get Console Port Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_console_port_details(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Get console port by ID (dcim/console-ports/{id}/).
    Accepts: id (required)
        id: Numeric ID of the console port to fetch. Returns `[obj]` or `[]`.
    """
    if "id" not in args:
        return []
    return await _get_detail("dcim/console-ports/", args["id"], args)


# dcim/console-port-templates

@mcp.tool(
    annotations={
        "title": "Search Console Port Templates",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_console_port_templates(args: Dict[str, Any]) -> Dict[str, Any]:
    """Search console port templates (dcim/console-port-templates/).
    Accepts: name, device_type, type, label, limit
        name: Name of the console port template (case-insensitive contains match)
        device_type: Device type ID (numeric)
        type: Console port type (case-insensitive contains match)
        label: Console port template label (case-insensitive contains match)
        limit: Maximum number of results to return (default 10)
    
    Returns `{count, results}` (NetBox total + page). Default `brief=true`
    for compact console port template objects; pass `brief=false` for full objects. Use
    `offset` to paginate, `fields`/`exclude` to project, `limit` capped at 100.
    """
    mappings = {
        "name": "name__ic",
        "device_type": "device_type_id",
        "type": "type__ic",
        "label": "label__ic"
    }
    return await _search("dcim/console-port-templates/", args, mappings)


@mcp.tool(
    annotations={
        "title": "Get Console Port Template Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_console_port_template_details(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Get console port template by ID (dcim/console-port-templates/{id}/).
    Accepts: id (required)
        id: Numeric ID of the console port template to fetch. Returns `[obj]` or `[]`.
    """
    if "id" not in args:
        return []
    return await _get_detail("dcim/console-port-templates/", args["id"], args)


# dcim/console-server-ports

@mcp.tool(
    annotations={
        "title": "Search Console Server Ports",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_console_server_ports(args: Dict[str, Any]) -> Dict[str, Any]:
    """Search console server ports (dcim/console-server-ports/).
    Accepts: name, device, type, label, limit
        name: Name of the console server port (case-insensitive contains match)
        device: Device ID (numeric)
        type: Console server port type (case-insensitive contains match)
        label: Console server port label (case-insensitive contains match)
        limit: Maximum number of results to return (default 10)
    
    Returns `{count, results}` (NetBox total + page). Default `brief=true`
    for compact console server port objects; pass `brief=false` for full objects. Use
    `offset` to paginate, `fields`/`exclude` to project, `limit` capped at 100.
    """
    mappings = {
        "name": "name__ic",
        "device": "device_id",
        "type": "type__ic",
        "label": "label__ic"
    }
    return await _search("dcim/console-server-ports/", args, mappings)


@mcp.tool(
    annotations={
        "title": "Get Console Server Port Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_console_server_port_details(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Get console server port by ID (dcim/console-server-ports/{id}/).
    Accepts: id (required)
        id: Numeric ID of the console server port to fetch. Returns `[obj]` or `[]`.
    """
    if "id" not in args:
        return []
    return await _get_detail("dcim/console-server-ports/", args["id"], args)


# dcim/console-server-port-templates

@mcp.tool(
    annotations={
        "title": "Search Console Server Port Templates",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_console_server_port_templates(args: Dict[str, Any]) -> Dict[str, Any]:
    """Search console server port templates (dcim/console-server-port-templates/).
    Accepts: name, device_type, type, label, limit
        name: Name of the console server port template (case-insensitive contains match)
        device_type: Device type ID (numeric)
        type: Console server port type (case-insensitive contains match)
        label: Console server port template label (case-insensitive contains match)
        limit: Maximum number of results to return (default 10)
    
    Returns `{count, results}` (NetBox total + page). Default `brief=true`
    for compact console server port template objects; pass `brief=false` for full objects. Use
    `offset` to paginate, `fields`/`exclude` to project, `limit` capped at 100.
    """
    mappings = {
        "name": "name__ic",
        "device_type": "device_type_id",
        "type": "type__ic",
        "label": "label__ic"
    }
    return await _search("dcim/console-server-port-templates/", args, mappings)


@mcp.tool(
    annotations={
        "title": "Get Console Server Port Template Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_console_server_port_template_details(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Get console server port template by ID (dcim/console-server-port-templates/{id}/).
    Accepts: id (required)
        id: Numeric ID of the console server port template to fetch. Returns `[obj]` or `[]`.
    """
    if "id" not in args:
        return []
    return await _get_detail("dcim/console-server-port-templates/", args["id"], args)


# dcim/devices

@mcp.tool(
    annotations={
        "title": "Search Devices",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_devices(args: Dict[str, Any]) -> Dict[str, Any]:
    """Search devices (dcim/devices/).
    Accepts: name, role, device_type, serial, asset_tag, rack, status, location, limit
        name: Name of the device (case-insensitive contains match)
        role: Device role ID or slug (NetBox API accepts numeric ID or slug)
        device_type: Device type ID or slug (NetBox API accepts numeric ID or slug)
        serial: Serial number (case-insensitive contains match)
        asset_tag: Asset tag (case-insensitive contains match)
        rack: Rack ID (numeric ID)
        status: Status of the device (exact match), e.g., 'active', 'planned', 'offline'
        location: Location ID (numeric)
        limit: maximum number of results to return (default 10)

    Returns `{count, results}` (NetBox total + page). Default `brief=true`
    for compact device objects; pass `brief=false` for full objects. Use
    `offset` to paginate, `fields`/`exclude` to project, `limit` capped at 100.
    """
    mappings = {
        "name": "name__ic",
        "role": "role",
        "device_type": "device_type",
        "serial": "serial__ic",
        "asset_tag": "asset_tag__ic",
        "rack": "rack_id",
        "status": "status",
        "location": "location_id"
    }
    return await _search("dcim/devices/", args, mappings)


@mcp.tool(
    annotations={
        "title": "Get Device Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_device_details(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Get device details by ID (dcim/devices/{id}/).
    Accepts: id (required)
        id: Numeric ID of the device to fetch. Returns `[obj]` or `[]`.
    """
    if "id" not in args:
        return []
    return await _get_detail("dcim/devices/", args["id"], args)


# dcim/device-bays

@mcp.tool(
    annotations={
        "title": "Search Device Bays",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_device_bays(args: Dict[str, Any]) -> Dict[str, Any]:
    """Search device bays (dcim/device-bays/).
    Accepts: name, device, label, limit
        name: Name of the device bay (case-insensitive contains match)
        device: Device ID (numeric)
        label: Device bay label (case-insensitive contains match)
        limit: Maximum number of results to return (default 10)
    
    Returns `{count, results}` (NetBox total + page). Default `brief=true`
    for compact device bay objects; pass `brief=false` for full objects. Use
    `offset` to paginate, `fields`/`exclude` to project, `limit` capped at 100.
    """
    mappings = {
        "name": "name__ic",
        "device": "device_id",
        "label": "label__ic"
    }
    return await _search("dcim/device-bays/", args, mappings)


@mcp.tool(
    annotations={
        "title": "Get Device Bay Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_device_bay_details(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Get device bay by ID (dcim/device-bays/{id}/).
    Accepts: id (required)
        id: Numeric ID of the device bay to fetch. Returns `[obj]` or `[]`.
    """
    if "id" not in args:
        return []
    return await _get_detail("dcim/device-bays/", args["id"], args)


# dcim/device-bay-templates

@mcp.tool(
    annotations={
        "title": "Search Device Bay Templates",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_device_bay_templates(args: Dict[str, Any]) -> Dict[str, Any]:
    """Search device bay templates (dcim/device-bay-templates/).
    Accepts: name, device_type, label, limit
        name: Name of the device bay template (case-insensitive contains match)
        device_type: Device type ID (numeric)
        label: Device bay template label (case-insensitive contains match)
        limit: Maximum number of results to return (default 10)
    
    Returns `{count, results}` (NetBox total + page). Default `brief=true`
    for compact device bay template objects; pass `brief=false` for full objects. Use
    `offset` to paginate, `fields`/`exclude` to project, `limit` capped at 100.
    """
    mappings = {
        "name": "name__ic",
        "device_type": "device_type_id",
        "label": "label__ic"
    }
    return await _search("dcim/device-bay-templates/", args, mappings)


@mcp.tool(
    annotations={
        "title": "Get Device Bay Template Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_device_bay_template_details(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Get device bay template by ID (dcim/device-bay-templates/{id}/).
    Accepts: id (required)
        id: Numeric ID of the device bay template to fetch. Returns `[obj]` or `[]`.
    """
    if "id" not in args:
        return []
    return await _get_detail("dcim/device-bay-templates/", args["id"], args)


# dcim/device-roles

@mcp.tool(
    annotations={
        "title": "Search Device Roles",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_device_roles(args: Dict[str, Any]) -> Dict[str, Any]:
    """Search device roles (dcim/device-roles/).
    Accepts: name, limit
        name: Name of the device role (case-insensitive contains match)
        limit: Maximum number of results to return (default 10)
    
    Returns `{count, results}` (NetBox total + page). Default `brief=true`
    for compact device role objects; pass `brief=false` for full objects. Use
    `offset` to paginate, `fields`/`exclude` to project, `limit` capped at 100.
    """
    mappings = {
        "name": "name__ic"
    }
    return await _search("dcim/device-roles/", args, mappings)


@mcp.tool(
    annotations={
        "title": "Get Device Role Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_device_role_details(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Get device role by ID (dcim/device-roles/{id}/).
    Accepts: id (required)
        id: Numeric ID of the device role to fetch. Returns `[obj]` or `[]`.
    """
    if "id" not in args:
        return []
    return await _get_detail("dcim/device-roles/", args["id"], args)


# dcim/device-types

@mcp.tool(
    annotations={
        "title": "Search Device Types",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_device_types(args: Dict[str, Any]) -> Dict[str, Any]:
    """Search device types (dcim/device-types/).
    Accepts: name, manufacturer, limit
        name: Name of the device type (case-insensitive contains match)
        manufacturer: Manufacturer ID (numeric)
        limit: Maximum number of results to return (default 10)
    
    Returns `{count, results}` (NetBox total + page). Default `brief=true`
    for compact device type objects; pass `brief=false` for full objects. Use
    `offset` to paginate, `fields`/`exclude` to project, `limit` capped at 100.
    """
    mappings = {
        "name": "name__ic",
        "manufacturer": "manufacturer_id"
    }
    return await _search("dcim/device-types/", args, mappings)


@mcp.tool(
    annotations={
        "title": "Get Device Type Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_device_type_details(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Get device type by ID (dcim/device-types/{id}/).
    Accepts: id (required)
        id: Numeric ID of the device type to fetch. Returns `[obj]` or `[]`.
    """
    if "id" not in args:
        return []
    return await _get_detail("dcim/device-types/", args["id"], args)


# dcim/front-ports

@mcp.tool(
    annotations={
        "title": "Search Front Ports",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_front_ports(args: Dict[str, Any]) -> Dict[str, Any]:
    """Search front ports (dcim/front-ports/).
    Accepts: name, device, type, label, limit
        name: Name of the front port (case-insensitive contains match)
        device: Device ID (numeric)
        type: Front port type (case-insensitive contains match)
        label: Front port label (case-insensitive contains match)
        limit: Maximum number of results to return (default 10)
    
    Returns `{count, results}` (NetBox total + page). Default `brief=true`
    for compact front port objects; pass `brief=false` for full objects. Use
    `offset` to paginate, `fields`/`exclude` to project, `limit` capped at 100.
    """
    mappings = {
        "name": "name__ic",
        "device": "device_id",
        "type": "type__ic",
        "label": "label__ic"
    }
    return await _search("dcim/front-ports/", args, mappings)


@mcp.tool(
    annotations={
        "title": "Get Front Port Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_front_port_details(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Get front port by ID (dcim/front-ports/{id}/).
    Accepts: id (required)
        id: Numeric ID of the front port to fetch. Returns `[obj]` or `[]`.
    """
    if "id" not in args:
        return []
    return await _get_detail("dcim/front-ports/", args["id"], args)


# dcim/front-port-templates

@mcp.tool(
    annotations={
        "title": "Search Front Port Templates",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_front_port_templates(args: Dict[str, Any]) -> Dict[str, Any]:
    """Search front port templates (dcim/front-port-templates/).
    Accepts: name, device_type, type, label, limit
        name: Name of the front port template (case-insensitive contains match)
        device_type: Device type ID (numeric)
        type: Front port type (case-insensitive contains match)
        label: Front port template label (case-insensitive contains match)
        limit: Maximum number of results to return (default 10)
    
    Returns `{count, results}` (NetBox total + page). Default `brief=true`
    for compact front port template objects; pass `brief=false` for full objects. Use
    `offset` to paginate, `fields`/`exclude` to project, `limit` capped at 100.
    """
    mappings = {
        "name": "name__ic",
        "device_type": "device_type_id",
        "type": "type__ic",
        "label": "label__ic"
    }
    return await _search("dcim/front-port-templates/", args, mappings)


@mcp.tool(
    annotations={
        "title": "Get Front Port Template Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_front_port_template_details(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Get front port template by ID (dcim/front-port-templates/{id}/).
    Accepts: id (required)
        id: Numeric ID of the front port template to fetch. Returns `[obj]` or `[]`.
    """
    if "id" not in args:
        return []
    return await _get_detail("dcim/front-port-templates/", args["id"], args)


# dcim/interfaces

@mcp.tool(
    annotations={
        "title": "Search Interfaces",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_interfaces(args: Dict[str, Any]) -> Dict[str, Any]:
    """Search interfaces (dcim/interfaces/).
    Accepts: name, device, type, label, limit
        name: Name of the interface (case-insensitive contains match)
        device: Device ID (numeric)
        type: Interface type (case-insensitive contains match)
        label: Interface label (case-insensitive contains match)
        limit: Maximum number of results to return (default 10)
    
    Returns `{count, results}` (NetBox total + page). Default `brief=true`
    for compact interface objects; pass `brief=false` for full objects. Use
    `offset` to paginate, `fields`/`exclude` to project, `limit` capped at 100.
    """
    mappings = {
        "name": "name__ic",
        "device": "device_id",
        "type": "type__ic",
        "label": "label__ic"
    }
    return await _search("dcim/interfaces/", args, mappings)


@mcp.tool(
    annotations={
        "title": "Get Interface Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_interface_details(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Get interface by ID (dcim/interfaces/{id}/).
    Accepts: id (required)
        id: Numeric ID of the interface to fetch. Returns `[obj]` or `[]`.
    """
    if "id" not in args:
        return []
    return await _get_detail("dcim/interfaces/", args["id"], args)


# dcim/interface-templates

@mcp.tool(
    annotations={
        "title": "Search Interface Templates",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_interface_templates(args: Dict[str, Any]) -> Dict[str, Any]:
    """Search interface templates (dcim/interface-templates/).
    Accepts: name, device_type, type, label, limit
        name: Name of the interface template (case-insensitive contains match)
        device_type: Device type ID (numeric)
        type: Interface type (case-insensitive contains match)
        label: Interface template label (case-insensitive contains match)
        limit: Maximum number of results to return (default 10)
    
    Returns `{count, results}` (NetBox total + page). Default `brief=true`
    for compact interface template objects; pass `brief=false` for full objects. Use
    `offset` to paginate, `fields`/`exclude` to project, `limit` capped at 100.
    """
    mappings = {
        "name": "name__ic",
        "device_type": "device_type_id",
        "type": "type__ic",
        "label": "label__ic"
    }
    return await _search("dcim/interface-templates/", args, mappings)


@mcp.tool(
    annotations={
        "title": "Get Interface Template Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_interface_template_details(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Get interface template by ID (dcim/interface-templates/{id}/).
    Accepts: id (required)
        id: Numeric ID of the interface template to fetch. Returns `[obj]` or `[]`.
    """
    if "id" not in args:
        return []
    return await _get_detail("dcim/interface-templates/", args["id"], args)


# dcim/inventory-items

@mcp.tool(
    annotations={
        "title": "Search Inventory Items",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_inventory_items(args: Dict[str, Any]) -> Dict[str, Any]:
    """Search inventory items (dcim/inventory-items/).
    Accepts: name, device, label, limit
        name: Name of the inventory item (case-insensitive contains match)
        device: Device ID (numeric)
        label: Inventory item label (case-insensitive contains match)
        limit: Maximum number of results to return (default 10)
    
    Returns `{count, results}` (NetBox total + page). Default `brief=true`
    for compact inventory item objects; pass `brief=false` for full objects. Use
    `offset` to paginate, `fields`/`exclude` to project, `limit` capped at 100.
    """
    mappings = {
        "name": "name__ic",
        "device": "device_id",
        "label": "label__ic"
    }
    return await _search("dcim/inventory-items/", args, mappings)


@mcp.tool(
    annotations={
        "title": "Get Inventory Item Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_inventory_item_details(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Get inventory item by ID (dcim/inventory-items/{id}/).
    Accepts: id (required)
        id: Numeric ID of the inventory item to fetch. Returns `[obj]` or `[]`.
    """
    if "id" not in args:
        return []
    return await _get_detail("dcim/inventory-items/", args["id"], args)


# dcim/inventory-item-roles

@mcp.tool(
    annotations={
        "title": "Search Inventory Item Roles",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_inventory_item_roles(args: Dict[str, Any]) -> Dict[str, Any]:
    """Search inventory item roles (dcim/inventory-item-roles/).
    Accepts: name, limit
        name: Name of the inventory item role (case-insensitive contains match)
        limit: Maximum number of results to return (default 10)
    
    Returns `{count, results}` (NetBox total + page). Default `brief=true`
    for compact inventory item role objects; pass `brief=false` for full objects. Use
    `offset` to paginate, `fields`/`exclude` to project, `limit` capped at 100.
    """
    mappings = {
        "name": "name__ic"
    }
    return await _search("dcim/inventory-item-roles/", args, mappings)


@mcp.tool(
    annotations={
        "title": "Get Inventory Item Role Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_inventory_item_role_details(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Get inventory item role by ID (dcim/inventory-item-roles/{id}/).
    Accepts: id (required)
        id: Numeric ID of the inventory item role to fetch. Returns `[obj]` or `[]`.
    """
    if "id" not in args:
        return []
    return await _get_detail("dcim/inventory-item-roles/", args["id"], args)


# dcim/inventory-item-templates

@mcp.tool(
    annotations={
        "title": "Search Inventory Item Templates",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_inventory_item_templates(args: Dict[str, Any]) -> Dict[str, Any]:
    """Search inventory item templates (dcim/inventory-item-templates/).
    Accepts: name, device_type, label, limit
        name: Name of the inventory item template (case-insensitive contains match)
        device_type: Device type ID (numeric)
        label: Inventory item template label (case-insensitive contains match)
        limit: Maximum number of results to return (default 10)
    
    Returns `{count, results}` (NetBox total + page). Default `brief=true`
    for compact inventory item template objects; pass `brief=false` for full objects. Use
    `offset` to paginate, `fields`/`exclude` to project, `limit` capped at 100.
    """
    mappings = {
        "name": "name__ic",
        "device_type": "device_type_id",
        "label": "label__ic"
    }
    return await _search("dcim/inventory-item-templates/", args, mappings)


@mcp.tool(
    annotations={
        "title": "Get Inventory Item Template Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_inventory_item_template_details(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Get inventory item template by ID (dcim/inventory-item-templates/{id}/).
    Accepts: id (required)
        id: Numeric ID of the inventory item template to fetch. Returns `[obj]` or `[]`.
    """
    if "id" not in args:
        return []
    return await _get_detail("dcim/inventory-item-templates/", args["id"], args)


# dcim/locations

@mcp.tool(
    annotations={
        "title": "Search Locations",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_locations(args: Dict[str, Any]) -> Dict[str, Any]:
    """Search locations (dcim/locations/).
    Accepts: name, status, limit
        name: Name of the location (case-insensitive contains match)
        status: Status of the location (exact match), e.g., 'active', 'planned', 'retired'
        limit: Maximum number of results to return (default 10)
    
    Returns `{count, results}` (NetBox total + page). Default `brief=true`
    for compact location objects; pass `brief=false` for full objects. Use
    `offset` to paginate, `fields`/`exclude` to project, `limit` capped at 100.
    """
    mappings = {
        "name": "name__ic",
        "status": "status"
    }
    return await _search("dcim/locations/", args, mappings)


@mcp.tool(
    annotations={
        "title": "Get Location Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_location_details(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Get location by ID (dcim/locations/{id}/).
    Accepts: id (required)
        id: Numeric ID of the location to fetch. Returns `[obj]` or `[]`.
    """
    if "id" not in args:
        return []
    return await _get_detail("dcim/locations/", args["id"], args)


# dcim/mac-addresses

@mcp.tool(
    annotations={
        "title": "Search Mac Addresses",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_mac_addresses(args: Dict[str, Any]) -> Dict[str, Any]:
    """Search MAC addresses (dcim/mac-addresses/).
    Accepts: mac_address, device, limit
        mac_address: MAC address (case-insensitive contains match)
        device: Device ID (numeric)
        limit: Maximum number of results to return (default 10)
    
    Returns `{count, results}` (NetBox total + page). Default `brief=true`
    for compact MAC address objects; pass `brief=false` for full objects. Use
    `offset` to paginate, `fields`/`exclude` to project, `limit` capped at 100.
    """
    mappings = {
        "mac_address": "mac_address__ic",
        "device": "device_id"
    }
    return await _search("dcim/mac-addresses/", args, mappings)


@mcp.tool(
    annotations={
        "title": "Get Mac Address Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_mac_address_details(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Get MAC address by ID (dcim/mac-addresses/{id}/).
    Accepts: id (required)
        id: Numeric ID of the MAC address to fetch. Returns `[obj]` or `[]`.
    """
    if "id" not in args:
        return []
    return await _get_detail("dcim/mac-addresses/", args["id"], args)


# dcim/manufacturers

@mcp.tool(
    annotations={
        "title": "Search Manufacturers",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_manufacturers(args: Dict[str, Any]) -> Dict[str, Any]:
    """Search manufacturers (dcim/manufacturers/).
    Accepts: name, limit
        name: Name of the manufacturer (case-insensitive contains match)
        limit: Maximum number of results to return (default 10)
    
    Returns `{count, results}` (NetBox total + page). Default `brief=true`
    for compact manufacturer objects; pass `brief=false` for full objects. Use
    `offset` to paginate, `fields`/`exclude` to project, `limit` capped at 100.
    """
    mappings = {
        "name": "name__ic"
    }
    return await _search("dcim/manufacturers/", args, mappings)


@mcp.tool(
    annotations={
        "title": "Get Manufacturer Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_manufacturer_details(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Get manufacturer by ID (dcim/manufacturers/{id}/).
    Accepts: id (required)
        id: Numeric ID of the manufacturer to fetch. Returns `[obj]` or `[]`.
    """
    if "id" not in args:
        return []
    return await _get_detail("dcim/manufacturers/", args["id"], args)


# dcim/modules

@mcp.tool(
    annotations={
        "title": "Search Modules",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_modules(args: Dict[str, Any]) -> Dict[str, Any]:
    """Search modules (dcim/modules/).
    Accepts: device, status, limit
        device: Device ID (numeric)
        status: Status of the module (exact match), e.g., 'active', 'planned', 'offline'
        limit: Maximum number of results to return (default 10)
    
    Returns `{count, results}` (NetBox total + page). Default `brief=true`
    for compact module objects; pass `brief=false` for full objects. Use
    `offset` to paginate, `fields`/`exclude` to project, `limit` capped at 100.
    """
    mappings = {
        "device": "device_id",
        "status": "status"
    }
    return await _search("dcim/modules/", args, mappings)


@mcp.tool(
    annotations={
        "title": "Get Module Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_module_details(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Get module by ID (dcim/modules/{id}/).
    Accepts: id (required)
        id: Numeric ID of the module to fetch. Returns `[obj]` or `[]`.
    """
    if "id" not in args:
        return []
    return await _get_detail("dcim/modules/", args["id"], args)


# dcim/module-bays

@mcp.tool(
    annotations={
        "title": "Search Module Bays",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_module_bays(args: Dict[str, Any]) -> Dict[str, Any]:
    """Search module bays (dcim/module-bays/).
    Accepts: name, device, label, limit
        name: Name of the module bay (case-insensitive contains match)
        device: Device ID (numeric)
        label: Module bay label (case-insensitive contains match)
        limit: Maximum number of results to return (default 10)
    
    Returns `{count, results}` (NetBox total + page). Default `brief=true`
    for compact module bay objects; pass `brief=false` for full objects. Use
    `offset` to paginate, `fields`/`exclude` to project, `limit` capped at 100.
    """
    mappings = {
        "name": "name__ic",
        "device": "device_id",
        "label": "label__ic"
    }
    return await _search("dcim/module-bays/", args, mappings)


@mcp.tool(
    annotations={
        "title": "Get Module Bay Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_module_bay_details(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Get module bay by ID (dcim/module-bays/{id}/).
    Accepts: id (required)
        id: Numeric ID of the module bay to fetch. Returns `[obj]` or `[]`.
    """
    if "id" not in args:
        return []
    return await _get_detail("dcim/module-bays/", args["id"], args)


# dcim/module-bay-templates

@mcp.tool(
    annotations={
        "title": "Search Module Bay Templates",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_module_bay_templates(args: Dict[str, Any]) -> Dict[str, Any]:
    """Search module bay templates (dcim/module-bay-templates/).
    Accepts: name, device_type, label, limit
        name: Name of the module bay template (case-insensitive contains match)
        device_type: Device type ID (numeric)
        label: Module bay template label (case-insensitive contains match)
        limit: Maximum number of results to return (default 10)
    
    Returns `{count, results}` (NetBox total + page). Default `brief=true`
    for compact module bay template objects; pass `brief=false` for full objects. Use
    `offset` to paginate, `fields`/`exclude` to project, `limit` capped at 100.
    """
    mappings = {
        "name": "name__ic",
        "device_type": "device_type_id",
        "label": "label__ic"
    }
    return await _search("dcim/module-bay-templates/", args, mappings)


@mcp.tool(
    annotations={
        "title": "Get Module Bay Template Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_module_bay_template_details(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Get module bay template by ID (dcim/module-bay-templates/{id}/).
    Accepts: id (required)
        id: Numeric ID of the module bay template to fetch. Returns `[obj]` or `[]`.
    """
    if "id" not in args:
        return []
    return await _get_detail("dcim/module-bay-templates/", args["id"], args)


# dcim/module-types

@mcp.tool(
    annotations={
        "title": "Search Module Types",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_module_types(args: Dict[str, Any]) -> Dict[str, Any]:
    """Search module types (dcim/module-types/).
    Accepts: name, manufacturer, limit
        name: Name of the module type (case-insensitive contains match)
        manufacturer: Manufacturer ID (numeric)
        limit: Maximum number of results to return (default 10)
    
    Returns `{count, results}` (NetBox total + page). Default `brief=true`
    for compact module type objects; pass `brief=false` for full objects. Use
    `offset` to paginate, `fields`/`exclude` to project, `limit` capped at 100.
    """
    mappings = {
        "name": "name__ic",
        "manufacturer": "manufacturer_id"
    }
    return await _search("dcim/module-types/", args, mappings)


@mcp.tool(
    annotations={
        "title": "Get Module Type Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_module_type_details(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Get module type by ID (dcim/module-types/{id}/).
    Accepts: id (required)
        id: Numeric ID of the module type to fetch. Returns `[obj]` or `[]`.
    """
    if "id" not in args:
        return []
    return await _get_detail("dcim/module-types/", args["id"], args)


# dcim/module-type-profiles

@mcp.tool(
    annotations={
        "title": "Search Module Type Profiles",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_module_type_profiles(args: Dict[str, Any]) -> Dict[str, Any]:
    """Search module type profiles (dcim/module-type-profiles/).
    Accepts: name, limit
        name: Name of the module type profile (case-insensitive contains match)
        limit: Maximum number of results to return (default 10)
    
    Returns `{count, results}` (NetBox total + page). Default `brief=true`
    for compact module type profile objects; pass `brief=false` for full objects. Use
    `offset` to paginate, `fields`/`exclude` to project, `limit` capped at 100.
    """
    mappings = {
        "name": "name__ic"
    }
    return await _search("dcim/module-type-profiles/", args, mappings)


@mcp.tool(
    annotations={
        "title": "Get Module Type Profile Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_module_type_profile_details(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Get module type profile by ID (dcim/module-type-profiles/{id}/).
    Accepts: id (required)
        id: Numeric ID of the module type profile to fetch. Returns `[obj]` or `[]`.
    """
    if "id" not in args:
        return []
    return await _get_detail("dcim/module-type-profiles/", args["id"], args)


# dcim/platforms

@mcp.tool(
    annotations={
        "title": "Search Platforms",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_platforms(args: Dict[str, Any]) -> Dict[str, Any]:
    """Search platforms (dcim/platforms/).
    Accepts: name, manufacturer, limit
        name: Name of the platform (case-insensitive contains match)
        manufacturer: Manufacturer ID (numeric)
        limit: Maximum number of results to return (default 10)
    
    Returns `{count, results}` (NetBox total + page). Default `brief=true`
    for compact platform objects; pass `brief=false` for full objects. Use
    `offset` to paginate, `fields`/`exclude` to project, `limit` capped at 100.
    """
    mappings = {
        "name": "name__ic",
        "manufacturer": "manufacturer_id"
    }
    return await _search("dcim/platforms/", args, mappings)


@mcp.tool(
    annotations={
        "title": "Get Platform Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_platform_details(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Get platform by ID (dcim/platforms/{id}/).
    Accepts: id (required)
        id: Numeric ID of the platform to fetch. Returns `[obj]` or `[]`.
    """
    if "id" not in args:
        return []
    return await _get_detail("dcim/platforms/", args["id"], args)


# dcim/power-feeds

@mcp.tool(
    annotations={
        "title": "Search Power Feeds",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_power_feeds(args: Dict[str, Any]) -> Dict[str, Any]:
    """Search power feeds (dcim/power-feeds/).
    Accepts: name, status, type, limit
        name: Name of the power feed (case-insensitive contains match)
        status: Status of the power feed (exact match), e.g., 'active', 'planned', 'offline'
        type: Power feed type (case-insensitive contains match)
        limit: Maximum number of results to return (default 10)
    
    Returns `{count, results}` (NetBox total + page). Default `brief=true`
    for compact power feed objects; pass `brief=false` for full objects. Use
    `offset` to paginate, `fields`/`exclude` to project, `limit` capped at 100.
    """
    mappings = {
        "name": "name__ic",
        "status": "status",
        "type": "type__ic"
    }
    return await _search("dcim/power-feeds/", args, mappings)


@mcp.tool(
    annotations={
        "title": "Get Power Feed Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_power_feed_details(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Get power feed by ID (dcim/power-feeds/{id}/).
    Accepts: id (required)
        id: Numeric ID of the power feed to fetch. Returns `[obj]` or `[]`.
    """
    if "id" not in args:
        return []
    return await _get_detail("dcim/power-feeds/", args["id"], args)


# dcim/power-outlets

@mcp.tool(
    annotations={
        "title": "Search Power Outlets",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_power_outlets(args: Dict[str, Any]) -> Dict[str, Any]:
    """Search power outlets (dcim/power-outlets/).
    Accepts: name, device, type, label, limit
        name: Name of the power outlet (case-insensitive contains match)
        device: Device ID (numeric)
        type: Power outlet type (case-insensitive contains match)
        label: Power outlet label (case-insensitive contains match)
        limit: Maximum number of results to return (default 10)
    
    Returns `{count, results}` (NetBox total + page). Default `brief=true`
    for compact power outlet objects; pass `brief=false` for full objects. Use
    `offset` to paginate, `fields`/`exclude` to project, `limit` capped at 100.
    """
    mappings = {
        "name": "name__ic",
        "device": "device_id",
        "type": "type__ic",
        "label": "label__ic"
    }
    return await _search("dcim/power-outlets/", args, mappings)


@mcp.tool(
    annotations={
        "title": "Get Power Outlet Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_power_outlet_details(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Get power outlet by ID (dcim/power-outlets/{id}/).
    Accepts: id (required)
        id: Numeric ID of the power outlet to fetch. Returns `[obj]` or `[]`.
    """
    if "id" not in args:
        return []
    return await _get_detail("dcim/power-outlets/", args["id"], args)


# dcim/power-outlet-templates

@mcp.tool(
    annotations={
        "title": "Search Power Outlet Templates",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_power_outlet_templates(args: Dict[str, Any]) -> Dict[str, Any]:
    """Search power outlet templates (dcim/power-outlet-templates/).
    Accepts: name, device_type, type, label, limit
        name: Name of the power outlet template (case-insensitive contains match)
        device_type: Device type ID (numeric)
        type: Power outlet type (case-insensitive contains match)
        label: Power outlet template label (case-insensitive contains match)
        limit: Maximum number of results to return (default 10)
    
    Returns `{count, results}` (NetBox total + page). Default `brief=true`
    for compact power outlet template objects; pass `brief=false` for full objects. Use
    `offset` to paginate, `fields`/`exclude` to project, `limit` capped at 100.
    """
    mappings = {
        "name": "name__ic",
        "device_type": "device_type_id",
        "type": "type__ic",
        "label": "label__ic"
    }
    return await _search("dcim/power-outlet-templates/", args, mappings)


@mcp.tool(
    annotations={
        "title": "Get Power Outlet Template Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_power_outlet_template_details(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Get power outlet template by ID (dcim/power-outlet-templates/{id}/).
    Accepts: id (required)
        id: Numeric ID of the power outlet template to fetch. Returns `[obj]` or `[]`.
    """
    if "id" not in args:
        return []
    return await _get_detail("dcim/power-outlet-templates/", args["id"], args)


# dcim/power-panels

@mcp.tool(
    annotations={
        "title": "Search Power Panels",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_power_panels(args: Dict[str, Any]) -> Dict[str, Any]:
    """Search power panels (dcim/power-panels/).
    Accepts: name, location, limit
        name: Name of the power panel (case-insensitive contains match)
        location: Location ID (numeric)
        limit: Maximum number of results to return (default 10)
    
    Returns `{count, results}` (NetBox total + page). Default `brief=true`
    for compact power panel objects; pass `brief=false` for full objects. Use
    `offset` to paginate, `fields`/`exclude` to project, `limit` capped at 100.
    """
    mappings = {
        "name": "name__ic",
        "location": "location_id"
    }
    return await _search("dcim/power-panels/", args, mappings)


@mcp.tool(
    annotations={
        "title": "Get Power Panel Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_power_panel_details(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Get power panel by ID (dcim/power-panels/{id}/).
    Accepts: id (required)
        id: Numeric ID of the power panel to fetch. Returns `[obj]` or `[]`.
    """
    if "id" not in args:
        return []
    return await _get_detail("dcim/power-panels/", args["id"], args)


# dcim/power-ports

@mcp.tool(
    annotations={
        "title": "Search Power Ports",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_power_ports(args: Dict[str, Any]) -> Dict[str, Any]:
    """Search power ports (dcim/power-ports/).
    Accepts: name, device, type, label, limit
        name: Name of the power port (case-insensitive contains match)
        device: Device ID (numeric)
        type: Power port type (case-insensitive contains match)
        label: Power port label (case-insensitive contains match)
        limit: Maximum number of results to return (default 10)
    
    Returns `{count, results}` (NetBox total + page). Default `brief=true`
    for compact power port objects; pass `brief=false` for full objects. Use
    `offset` to paginate, `fields`/`exclude` to project, `limit` capped at 100.
    """
    mappings = {
        "name": "name__ic",
        "device": "device_id",
        "type": "type__ic",
        "label": "label__ic"
    }
    return await _search("dcim/power-ports/", args, mappings)


@mcp.tool(
    annotations={
        "title": "Get Power Port Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_power_port_details(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Get power port by ID (dcim/power-ports/{id}/).
    Accepts: id (required)
        id: Numeric ID of the power port to fetch. Returns `[obj]` or `[]`.
    """
    if "id" not in args:
        return []
    return await _get_detail("dcim/power-ports/", args["id"], args)


# dcim/power-port-templates

@mcp.tool(
    annotations={
        "title": "Search Power Port Templates",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_power_port_templates(args: Dict[str, Any]) -> Dict[str, Any]:
    """Search power port templates (dcim/power-port-templates/).
    Accepts: name, device_type, type, label, limit
        name: Name of the power port template (case-insensitive contains match)
        device_type: Device type ID (numeric)
        type: Power port type (case-insensitive contains match)
        label: Power port template label (case-insensitive contains match)
        limit: Maximum number of results to return (default 10)
    
    Returns `{count, results}` (NetBox total + page). Default `brief=true`
    for compact power port template objects; pass `brief=false` for full objects. Use
    `offset` to paginate, `fields`/`exclude` to project, `limit` capped at 100.
    """
    mappings = {
        "name": "name__ic",
        "device_type": "device_type_id",
        "type": "type__ic",
        "label": "label__ic"
    }
    return await _search("dcim/power-port-templates/", args, mappings)


@mcp.tool(
    annotations={
        "title": "Get Power Port Template Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_power_port_template_details(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Get power port template by ID (dcim/power-port-templates/{id}/).
    Accepts: id (required)
        id: Numeric ID of the power port template to fetch. Returns `[obj]` or `[]`.
    """
    if "id" not in args:
        return []
    return await _get_detail("dcim/power-port-templates/", args["id"], args)


# dcim/racks

@mcp.tool(
    annotations={
        "title": "Search Racks",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_racks(args: Dict[str, Any]) -> Dict[str, Any]:
    """Search racks (dcim/racks/).
    Accepts: name, status, location, limit
        name: Name of the rack (case-insensitive contains match)
        status: Status of the rack (exact match), e.g., 'active', 'planned', 'reserved'
        location: Location ID (numeric)
        limit: Maximum number of results to return (default 10)
    
    Returns `{count, results}` (NetBox total + page). Default `brief=true`
    for compact rack objects; pass `brief=false` for full objects. Use
    `offset` to paginate, `fields`/`exclude` to project, `limit` capped at 100.
    """
    mappings = {
        "name": "name__ic",
        "status": "status",
        "location": "location_id"
    }
    return await _search("dcim/racks/", args, mappings)


@mcp.tool(
    annotations={
        "title": "Get Rack Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_rack_details(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Get rack by ID (dcim/racks/{id}/).
    Accepts: id (required)
        id: Numeric ID of the rack to fetch. Returns `[obj]` or `[]`.
    """
    if "id" not in args:
        return []
    return await _get_detail("dcim/racks/", args["id"], args)


# dcim/rack-reservations

@mcp.tool(
    annotations={
        "title": "Search Rack Reservations",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_rack_reservations(args: Dict[str, Any]) -> Dict[str, Any]:
    """Search rack reservations (dcim/rack-reservations/).
    Accepts: rack, limit
        rack: Rack ID (numeric)
        limit: Maximum number of results to return (default 10)
    
    Returns `{count, results}` (NetBox total + page). Default `brief=true`
    for compact rack reservation objects; pass `brief=false` for full objects. Use
    `offset` to paginate, `fields`/`exclude` to project, `limit` capped at 100.
    """
    mappings = {
        "rack": "rack_id"
    }
    return await _search("dcim/rack-reservations/", args, mappings)


@mcp.tool(
    annotations={
        "title": "Get Rack Reservation Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_rack_reservation_details(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Get rack reservation by ID (dcim/rack-reservations/{id}/).
    Accepts: id (required)
        id: Numeric ID of the rack reservation to fetch. Returns `[obj]` or `[]`.
    """
    if "id" not in args:
        return []
    return await _get_detail("dcim/rack-reservations/", args["id"], args)


# dcim/rack-roles

@mcp.tool(
    annotations={
        "title": "Search Rack Roles",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_rack_roles(args: Dict[str, Any]) -> Dict[str, Any]:
    """Search rack roles (dcim/rack-roles/).
    Accepts: name, limit
        name: Name of the rack role (case-insensitive contains match)
        limit: Maximum number of results to return (default 10)
    
    Returns `{count, results}` (NetBox total + page). Default `brief=true`
    for compact rack role objects; pass `brief=false` for full objects. Use
    `offset` to paginate, `fields`/`exclude` to project, `limit` capped at 100.
    """
    mappings = {
        "name": "name__ic"
    }
    return await _search("dcim/rack-roles/", args, mappings)


@mcp.tool(
    annotations={
        "title": "Get Rack Role Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_rack_role_details(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Get rack role by ID (dcim/rack-roles/{id}/).
    Accepts: id (required)
        id: Numeric ID of the rack role to fetch. Returns `[obj]` or `[]`.
    """
    if "id" not in args:
        return []
    return await _get_detail("dcim/rack-roles/", args["id"], args)


# dcim/rack-types

@mcp.tool(
    annotations={
        "title": "Search Rack Types",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_rack_types(args: Dict[str, Any]) -> Dict[str, Any]:
    """Search rack types (dcim/rack-types/).
    Accepts: name, manufacturer, limit
        name: Name of the rack type (case-insensitive contains match)
        manufacturer: Manufacturer ID (numeric)
        limit: Maximum number of results to return (default 10)
    
    Returns `{count, results}` (NetBox total + page). Default `brief=true`
    for compact rack type objects; pass `brief=false` for full objects. Use
    `offset` to paginate, `fields`/`exclude` to project, `limit` capped at 100.
    """
    mappings = {
        "name": "name__ic",
        "manufacturer": "manufacturer_id"
    }
    return await _search("dcim/rack-types/", args, mappings)


@mcp.tool(
    annotations={
        "title": "Get Rack Type Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_rack_type_details(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Get rack type by ID (dcim/rack-types/{id}/).
    Accepts: id (required)
        id: Numeric ID of the rack type to fetch. Returns `[obj]` or `[]`.
    """
    if "id" not in args:
        return []
    return await _get_detail("dcim/rack-types/", args["id"], args)


# dcim/rear-ports

@mcp.tool(
    annotations={
        "title": "Search Rear Ports",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_rear_ports(args: Dict[str, Any]) -> Dict[str, Any]:
    """Search rear ports (dcim/rear-ports/).
    Accepts: name, device, type, label, limit
        name: Name of the rear port (case-insensitive contains match)
        device: Device ID (numeric)
        type: Rear port type (case-insensitive contains match)
        label: Rear port label (case-insensitive contains match)
        limit: Maximum number of results to return (default 10)
    
    Returns `{count, results}` (NetBox total + page). Default `brief=true`
    for compact rear port objects; pass `brief=false` for full objects. Use
    `offset` to paginate, `fields`/`exclude` to project, `limit` capped at 100.
    """
    mappings = {
        "name": "name__ic",
        "device": "device_id",
        "type": "type__ic",
        "label": "label__ic"
    }
    return await _search("dcim/rear-ports/", args, mappings)


@mcp.tool(
    annotations={
        "title": "Get Rear Port Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_rear_port_details(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Get rear port by ID (dcim/rear-ports/{id}/).
    Accepts: id (required)
        id: Numeric ID of the rear port to fetch. Returns `[obj]` or `[]`.
    """
    if "id" not in args:
        return []
    return await _get_detail("dcim/rear-ports/", args["id"], args)


# dcim/rear-port-templates

@mcp.tool(
    annotations={
        "title": "Search Rear Port Templates",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_rear_port_templates(args: Dict[str, Any]) -> Dict[str, Any]:
    """Search rear port templates (dcim/rear-port-templates/).
    Accepts: name, device_type, type, label, limit
        name: Name of the rear port template (case-insensitive contains match)
        device_type: Device type ID (numeric)
        type: Rear port type (case-insensitive contains match)
        label: Rear port template label (case-insensitive contains match)
        limit: Maximum number of results to return (default 10)
    
    Returns `{count, results}` (NetBox total + page). Default `brief=true`
    for compact rear port template objects; pass `brief=false` for full objects. Use
    `offset` to paginate, `fields`/`exclude` to project, `limit` capped at 100.
    """
    mappings = {
        "name": "name__ic",
        "device_type": "device_type_id",
        "type": "type__ic",
        "label": "label__ic"
    }
    return await _search("dcim/rear-port-templates/", args, mappings)


@mcp.tool(
    annotations={
        "title": "Get Rear Port Template Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_rear_port_template_details(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Get rear port template by ID (dcim/rear-port-templates/{id}/).
    Accepts: id (required)
        id: Numeric ID of the rear port template to fetch. Returns `[obj]` or `[]`.
    """
    if "id" not in args:
        return []
    return await _get_detail("dcim/rear-port-templates/", args["id"], args)


# dcim/regions

@mcp.tool(
    annotations={
        "title": "Search Regions",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_regions(args: Dict[str, Any]) -> Dict[str, Any]:
    """Search regions (dcim/regions/).
    Accepts: name, limit
        name: Name of the region (case-insensitive contains match)
        limit: Maximum number of results to return (default 10)
    
    Returns `{count, results}` (NetBox total + page). Default `brief=true`
    for compact region objects; pass `brief=false` for full objects. Use
    `offset` to paginate, `fields`/`exclude` to project, `limit` capped at 100.
    """
    mappings = {
        "name": "name__ic"
    }
    return await _search("dcim/regions/", args, mappings)


@mcp.tool(
    annotations={
        "title": "Get Region Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_region_details(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Get region by ID (dcim/regions/{id}/).
    Accepts: id (required)
        id: Numeric ID of the region to fetch. Returns `[obj]` or `[]`.
    """
    if "id" not in args:
        return []
    return await _get_detail("dcim/regions/", args["id"], args)


# dcim/virtual-chassis

@mcp.tool(
    annotations={
        "title": "Search Virtual Chassis",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_virtual_chassis(args: Dict[str, Any]) -> Dict[str, Any]:
    """Search virtual chassis (dcim/virtual-chassis/).
    Accepts: name, limit
        name: Name of the virtual chassis (case-insensitive contains match)
        limit: Maximum number of results to return (default 10)
    
    Returns `{count, results}` (NetBox total + page). Default `brief=true`
    for compact virtual chassis objects; pass `brief=false` for full objects. Use
    `offset` to paginate, `fields`/`exclude` to project, `limit` capped at 100.
    """
    mappings = {
        "name": "name__ic"
    }
    return await _search("dcim/virtual-chassis/", args, mappings)


@mcp.tool(
    annotations={
        "title": "Get Virtual Chassis Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_virtual_chassis_details(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Get virtual chassis by ID (dcim/virtual-chassis/{id}/).
    Accepts: id (required)
        id: Numeric ID of the virtual chassis to fetch. Returns `[obj]` or `[]`.
    """
    if "id" not in args:
        return []
    return await _get_detail("dcim/virtual-chassis/", args["id"], args)


# dcim/virtual-device-contexts

@mcp.tool(
    annotations={
        "title": "Search Virtual Device Contexts",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_virtual_device_contexts(args: Dict[str, Any]) -> Dict[str, Any]:
    """Search virtual device contexts (dcim/virtual-device-contexts/).
    Accepts: name, device, status, limit
        name: Name of the virtual device context (case-insensitive contains match)
        device: Device ID (numeric)
        status: Status of the virtual device context (exact match), e.g., 'active', 'planned', 'offline'
        limit: Maximum number of results to return (default 10)
    
    Returns `{count, results}` (NetBox total + page). Default `brief=true`
    for compact virtual device context objects; pass `brief=false` for full objects. Use
    `offset` to paginate, `fields`/`exclude` to project, `limit` capped at 100.
    """
    mappings = {
        "name": "name__ic",
        "device": "device_id",
        "status": "status"
    }
    return await _search("dcim/virtual-device-contexts/", args, mappings)


@mcp.tool(
    annotations={
        "title": "Get Virtual Device Context Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_virtual_device_context_details(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Get virtual device context by ID (dcim/virtual-device-contexts/{id}/).
    Accepts: id (required)
        id: Numeric ID of the virtual device context to fetch. Returns `[obj]` or `[]`.
    """
    if "id" not in args:
        return []
    return await _get_detail("dcim/virtual-device-contexts/", args["id"], args)


# dcim/rack-groups

@mcp.tool(
    annotations={
        "title": "Search Rack Groups",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_rack_groups(args: Dict[str, Any]) -> Dict[str, Any]:
    """Search rack groups (dcim/rack-groups/).
    Accepts: name, slug, parent, ancestor, q, tag, limit
        name: Name of the rack group (case-insensitive contains match)
        slug: Rack group slug (exact match)
        parent: Parent rack group ID
        ancestor: Ancestor rack group ID (any depth)
        q: Free-text search across name and description
        tag: Tag slug (single)
        limit: Maximum number of results to return (default 10)

    Returns `{count, results}` (NetBox total + page). Default `brief=true`
    for compact rack group objects; pass `brief=false` for full objects. Use
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
    return await _search("dcim/rack-groups/", args, mappings)


@mcp.tool(
    annotations={
        "title": "Get Rack Group Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_rack_group_details(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Get rack group by ID (dcim/rack-groups/{id}/).
    Accepts: id (required)
        id: Numeric ID of the rack group to fetch. Returns `[obj]` or `[]`.
    """
    if "id" not in args:
        return []
    return await _get_detail("dcim/rack-groups/", args["id"], args)


# dcim/cable-terminations

@mcp.tool(
    annotations={
        "title": "Search Cable Terminations",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_cable_terminations(args: Dict[str, Any]) -> Dict[str, Any]:
    """Search cable terminations (dcim/cable-terminations/).
    Accepts: cable, termination_type, termination_id, cable_end, q, limit
        cable: Cable ID
        termination_type: Content type of the termination (e.g. 'dcim.interface')
        termination_id: ID of the termination object
        cable_end: 'A' or 'B'
        q: Free-text search
        limit: Maximum number of results to return (default 10)

    Returns `{count, results}` (NetBox total + page). Default `brief=true`
    for compact cable termination objects; pass `brief=false` for full objects. Use
    `offset` to paginate, `fields`/`exclude` to project, `limit` capped at 100.
    """
    mappings = {
        "cable": "cable_id",
        "termination_type": "termination_type",
        "termination_id": "termination_id",
        "cable_end": "cable_end",
        "q": "q",
    }
    return await _search("dcim/cable-terminations/", args, mappings)


@mcp.tool(
    annotations={
        "title": "Get Cable Termination Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_cable_termination_details(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Get cable termination by ID (dcim/cable-terminations/{id}/).
    Accepts: id (required)
        id: Numeric ID of the cable termination to fetch. Returns `[obj]` or `[]`.
    """
    if "id" not in args:
        return []
    return await _get_detail("dcim/cable-terminations/", args["id"], args)


# dcim/cable-bundles (NetBox v4.6+)

@mcp.tool(
    annotations={
        "title": "Search Cable Bundles",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_cable_bundles(args: Dict[str, Any]) -> Dict[str, Any]:
    """Search cable bundles (dcim/cable-bundles/).
    Accepts: name, q, tag, limit
        name: Name of the cable bundle (case-insensitive contains match)
        q: Free-text search across name and description
        tag: Tag slug (single)
        limit: Maximum number of results to return (default 10)

    Returns `{count, results}` (NetBox total + page). Default `brief=true`
    for compact cable bundle objects; pass `brief=false` for full objects. Use
    `offset` to paginate, `fields`/`exclude` to project, `limit` capped at 100.
    """
    mappings = {
        "name": "name__ic",
        "q": "q",
        "tag": "tag",
    }
    return await _search("dcim/cable-bundles/", args, mappings)


@mcp.tool(
    annotations={
        "title": "Get Cable Bundle Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_cable_bundle_details(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Get cable bundle by ID (dcim/cable-bundles/{id}/).
    Accepts: id (required)
        id: Numeric ID of the cable bundle to fetch. Returns `[obj]` or `[]`.
    """
    if "id" not in args:
        return []
    return await _get_detail("dcim/cable-bundles/", args["id"], args)


# --- dcim action endpoints (cable trace, rack elevation, rendered config) ---

# dcim/console-ports/{id}/trace

@mcp.tool(
    annotations={
        "title": "Trace Console Port Cable Path",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_console_port_trace(args: Dict[str, Any]) -> Any:
    """Trace the cable path from a console port (dcim/console-ports/{id}/trace/).
    Accepts: id (required)
        id: Numeric ID of the console port.

    Returns the full cable path as a list of `[near_termination, cable, far_termination]`
    segments, traversing any patch panels in between. Returns `[]` on error.
    """
    if "id" not in args:
        return []
    return await _get_action(f"dcim/console-ports/{args['id']}/trace/", args)


# dcim/console-server-ports/{id}/trace

@mcp.tool(
    annotations={
        "title": "Trace Console Server Port Cable Path",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_console_server_port_trace(args: Dict[str, Any]) -> Any:
    """Trace the cable path from a console server port (dcim/console-server-ports/{id}/trace/).
    Accepts: id (required)
        id: Numeric ID of the console server port.

    Returns the full cable path as a list of `[near_termination, cable, far_termination]`
    segments, traversing any patch panels in between. Returns `[]` on error.
    """
    if "id" not in args:
        return []
    return await _get_action(f"dcim/console-server-ports/{args['id']}/trace/", args)


# dcim/power-ports/{id}/trace

@mcp.tool(
    annotations={
        "title": "Trace Power Port Cable Path",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_power_port_trace(args: Dict[str, Any]) -> Any:
    """Trace the cable path from a power port (dcim/power-ports/{id}/trace/).
    Accepts: id (required)
        id: Numeric ID of the power port.

    Returns the full cable path as a list of `[near_termination, cable, far_termination]`
    segments, traversing any patch panels in between. Returns `[]` on error.
    """
    if "id" not in args:
        return []
    return await _get_action(f"dcim/power-ports/{args['id']}/trace/", args)


# dcim/power-outlets/{id}/trace

@mcp.tool(
    annotations={
        "title": "Trace Power Outlet Cable Path",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_power_outlet_trace(args: Dict[str, Any]) -> Any:
    """Trace the cable path from a power outlet (dcim/power-outlets/{id}/trace/).
    Accepts: id (required)
        id: Numeric ID of the power outlet.

    Returns the full cable path as a list of `[near_termination, cable, far_termination]`
    segments, traversing any patch panels in between. Returns `[]` on error.
    """
    if "id" not in args:
        return []
    return await _get_action(f"dcim/power-outlets/{args['id']}/trace/", args)


# dcim/interfaces/{id}/trace

@mcp.tool(
    annotations={
        "title": "Trace Interface Cable Path",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_interface_trace(args: Dict[str, Any]) -> Any:
    """Trace the cable path from an interface (dcim/interfaces/{id}/trace/).
    Accepts: id (required)
        id: Numeric ID of the interface.

    Returns the full cable path as a list of `[near_termination, cable, far_termination]`
    segments, traversing any patch panels in between. Returns `[]` on error.
    """
    if "id" not in args:
        return []
    return await _get_action(f"dcim/interfaces/{args['id']}/trace/", args)


# dcim/power-feeds/{id}/trace

@mcp.tool(
    annotations={
        "title": "Trace Power Feed Cable Path",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_power_feed_trace(args: Dict[str, Any]) -> Any:
    """Trace the cable path from a power feed (dcim/power-feeds/{id}/trace/).
    Accepts: id (required)
        id: Numeric ID of the power feed.

    Returns the full cable path as a list of `[near_termination, cable, far_termination]`
    segments, traversing any patch panels in between. Returns `[]` on error.
    """
    if "id" not in args:
        return []
    return await _get_action(f"dcim/power-feeds/{args['id']}/trace/", args)


# dcim/racks/{id}/elevation

@mcp.tool(
    annotations={
        "title": "Get Rack Elevation",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_rack_elevation(args: Dict[str, Any]) -> Any:
    """Get rack elevation (dcim/racks/{id}/elevation/).
    Accepts: id (required), face, render, unit_width, unit_height,
             legend_width, exclude, expand_devices, include_images
        id: Numeric ID of the rack.
        face: 'front' or 'rear' (default: front)
        render: 'json' (default) or 'svg'

    Returns the rack's unit-by-unit elevation listing installed devices,
    or `[]` on error. Use this to answer "what's mounted in rack X".
    """
    if "id" not in args:
        return []
    return await _get_action(f"dcim/racks/{args['id']}/elevation/", args)


# dcim/devices/{id}/render-config

@mcp.tool(
    annotations={
        "title": "Get Device Rendered Config",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_device_rendered_config(args: Dict[str, Any]) -> Any:
    """Render a device's assigned config template (dcim/devices/{id}/render-config/).
    Accepts: id (required), format
        id: Numeric ID of the device.
        format: 'json' or 'txt' (NetBox default depends on Accept header)

    Returns the rendered configuration text/JSON, or `[]` on error.
    Only works for devices with an assigned `config_template`.
    """
    if "id" not in args:
        return []
    return await _get_action(f"dcim/devices/{args['id']}/render-config/", args)

