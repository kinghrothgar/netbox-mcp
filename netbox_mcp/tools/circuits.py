"""Tools for the NetBox circuits app."""

from typing import Any, Dict, List

from ..helpers import _get_detail, _get_list, _search
from ..server import mcp


# --- circuits (circuits, circuit groups, providers, etc.) ---

# circuits

# circuits/circuits

@mcp.tool(
    annotations={
        "title": "Search Circuits",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_circuits(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Search circuits (circuits/circuits/).
    Accepts: provider, circuit_id, circuit_type, status, limit
        provider: Provider ID or name (case-insensitive contains match for name)
        circuit_id: Circuit ID (case-insensitive contains match)
        circuit_type: Circuit Type ID or name
        status: Status of the circuit (exact match), e.g., 'active', 'planned', 'decommissioning'
        limit: Maximum number of results to return (default 10)
    
    Returns a list of NetBox circuit objects (the `results` list) or an empty list.
    """
    mappings = {
        "provider": "provider",
        "circuit_id": "cid__ic",
        "circuit_type": "type",
        "status": "status"
    }
    return await _search("circuits/circuits/", args, mappings)


@mcp.tool(
    annotations={
        "title": "Get Circuit Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_circuit_details(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Get circuit by ID (circuits/circuits/{id}/).
    Accepts: id (required)
        id: Numeric ID of the circuit to fetch. Returns `[obj]` or `[]`.
    """
    if "id" not in args:
        return []
    return await _get_detail("circuits/circuits/", args["id"])


# circuits/circuit-groups

@mcp.tool(
    annotations={
        "title": "Search Circuit Groups",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_circuit_groups(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Search circuit groups (circuits/circuit-groups/).
    Accepts: name, limit
        name: Name of the circuit group (case-insensitive contains match)
        limit: Maximum number of results to return (default 10)
    
    Returns a list of NetBox circuit group objects (the `results` list) or an empty list.
    """
    mappings = {"name": "name__ic"}
    return await _search("circuits/circuit-groups/", args, mappings)


@mcp.tool(
    annotations={
        "title": "Get Circuit Group Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_circuit_group_details(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Get circuit group by ID (circuits/circuit-groups/{id}/).
    Accepts: id (required)
        id: Numeric ID of the circuit group to fetch. Returns `[obj]` or `[]`.
    """
    if "id" not in args:
        return []
    return await _get_detail("circuits/circuit-groups/", args["id"])


# circuits/circuit-group-assignments

@mcp.tool(
    annotations={
        "title": "Search Circuit Group Assignments",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_circuit_group_assignments(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Search circuit group assignments (circuits/circuit-group-assignments/).
    Accepts: priority, group, limit
        priority: Priority value (exact match)
        group: Circuit group ID (numeric)
        limit: Maximum number of results to return (default 10)
    
    Returns a list of NetBox circuit group assignment objects (the `results` list) or an empty list.
    """
    mappings = {
        "priority": "priority",
        "group": "group_id"
    }
    return await _search("circuits/circuit-group-assignments/", args, mappings)


@mcp.tool(
    annotations={
        "title": "Get Circuit Group Assignment Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_circuit_group_assignment_details(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Get circuit group assignment by ID (circuits/circuit-group-assignments/{id}/).
    Accepts: id (required)
        id: Numeric ID of the circuit group assignment to fetch. Returns `[obj]` or `[]`.
    """
    if "id" not in args:
        return []
    return await _get_detail("circuits/circuit-group-assignments/", args["id"])


# circuits/circuit-terminations

@mcp.tool(
    annotations={
        "title": "Search Circuit Terminations",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_circuit_terminations(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Search circuit terminations (circuits/circuit-terminations/).
    Accepts: circuit, termination, limit
        circuit: Circuit ID (numeric)
        termination: Termination side, typically 'A' or 'Z'
        limit: Maximum number of results to return (default 10)
    
    Returns a list of NetBox circuit termination objects (the `results` list) or an empty list.
    """
    mappings = {
        "circuit": "circuit_id",
        "termination": "term_side"
    }
    return await _search("circuits/circuit-terminations/", args, mappings)


@mcp.tool(
    annotations={
        "title": "Get Circuit Termination Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_circuit_termination_details(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Get circuit termination by ID (circuits/circuit-terminations/{id}/).
    Accepts: id (required)
        id: Numeric ID of the circuit termination to fetch. Returns `[obj]` or `[]`.
    """
    if "id" not in args:
        return []
    return await _get_detail("circuits/circuit-terminations/", args["id"])


# circuits/circuit-types

@mcp.tool(
    annotations={
        "title": "Search Circuit Types",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_circuit_types(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Search circuit types (circuits/circuit-types/).
    Accepts: name, limit
        name: Name of the circuit type (case-insensitive contains match)
        limit: Maximum number of results to return (default 10)
    
    Returns a list of NetBox circuit type objects (the `results` list) or an empty list.
    """
    mappings = {"name": "name__ic"}
    return await _search("circuits/circuit-types/", args, mappings)


@mcp.tool(
    annotations={
        "title": "Get Circuit Type Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_circuit_type_details(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Get circuit type by ID (circuits/circuit-types/{id}/).
    Accepts: id (required)
        id: Numeric ID of the circuit type to fetch. Returns `[obj]` or `[]`.
    """
    if "id" not in args:
        return []
    return await _get_detail("circuits/circuit-types/", args["id"])


# circuits/providers

@mcp.tool(
    annotations={
        "title": "Search Providers",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_providers(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Search providers (circuits/providers/).
    Accepts: name, limit
        name: Name of the provider (case-insensitive contains match)
        limit: Maximum number of results to return (default 10)
    
    Returns a list of NetBox provider objects (the `results` list) or an empty list.
    """
    mappings = {"name": "name__ic"}
    return await _search("circuits/providers/", args, mappings)


@mcp.tool(
    annotations={
        "title": "Get Provider Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_provider_details(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Get provider by ID (circuits/providers/{id}/).
    Accepts: id (required)
        id: Numeric ID of the provider to fetch. Returns `[obj]` or `[]`.
    """
    if "id" not in args:
        return []
    return await _get_detail("circuits/providers/", args["id"])


# circuits/provider-accounts

@mcp.tool(
    annotations={
        "title": "Search Provider Accounts",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_provider_accounts(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Search provider accounts (circuits/provider-accounts/).
    Accepts: name, account_number, limit
        name: Name of the provider account (case-insensitive contains match)
        account_number: Account number (case-insensitive contains match)
        limit: Maximum number of results to return (default 10)
    
    Returns a list of NetBox provider account objects (the `results` list) or an empty list.
    """
    mappings = {
        "name": "name__ic",
        "account_number": "account__ic"
    }
    return await _search("circuits/provider-accounts/", args, mappings)


@mcp.tool(
    annotations={
        "title": "Get Provider Account Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_provider_account_details(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Get provider account by ID (circuits/provider-accounts/{id}/).
    Accepts: id (required)
        id: Numeric ID of the provider account to fetch. Returns `[obj]` or `[]`.
    """
    if "id" not in args:
        return []
    return await _get_detail("circuits/provider-accounts/", args["id"])


# circuits/provider-networks

@mcp.tool(
    annotations={
        "title": "Search Provider Networks",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_provider_networks(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Search provider networks (circuits/provider-networks/).
    Accepts: name, limit
        name: Name of the provider network (case-insensitive contains match)
        limit: Maximum number of results to return (default 10)
    
    Returns a list of NetBox provider network objects (the `results` list) or an empty list.
    """
    mappings = {"name": "name__ic"}
    return await _search("circuits/provider-networks/", args, mappings)


@mcp.tool(
    annotations={
        "title": "Get Provider Network Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_provider_network_details(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Get provider network by ID (circuits/provider-networks/{id}/).
    Accepts: id (required)
        id: Numeric ID of the provider network to fetch. Returns `[obj]` or `[]`.
    """
    if "id" not in args:
        return []
    return await _get_detail("circuits/provider-networks/", args["id"])


# circuits/virtual-circuits

@mcp.tool(
    annotations={
        "title": "Search Virtual Circuits",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_virtual_circuits(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Search virtual circuits (circuits/virtual-circuits/).
    Accepts: provider_network, provider_account, circuit_id, status, limit
        provider_network: Provider network ID (numeric)
        provider_account: Provider account ID (numeric)
        circuit_id: Virtual circuit ID (case-insensitive contains match)
        status: Status of the virtual circuit (exact match), e.g., 'active', 'planned', 'offline'
        limit: Maximum number of results to return (default 10)
    
    Returns a list of NetBox virtual circuit objects (the `results` list) or an empty list.
    """
    mappings = {
        "provider_network": "provider_network_id",
        "provider_account": "provider_account_id",
        "circuit_id": "cid__ic",
        "status": "status"
    }
    return await _search("circuits/virtual-circuits/", args, mappings)


@mcp.tool(
    annotations={
        "title": "Get Virtual Circuit Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_virtual_circuit_details(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Get virtual circuit by ID (circuits/virtual-circuits/{id}/).
    Accepts: id (required)
        id: Numeric ID of the virtual circuit to fetch. Returns `[obj]` or `[]`.
    """
    if "id" not in args:
        return []
    return await _get_detail("circuits/virtual-circuits/", args["id"])


# circuits/virtual-circuit-terminations

@mcp.tool(
    annotations={
        "title": "Search Virtual Circuit Terminations",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_virtual_circuit_terminations(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Search virtual circuit terminations (circuits/virtual-circuit-terminations/).
    Accepts: virtual_circuit, interface, limit
        virtual_circuit: Virtual circuit ID (numeric)
        interface: Interface ID (numeric)
        limit: Maximum number of results to return (default 10)
    
    Returns a list of NetBox virtual circuit termination objects (the `results` list) or an empty list.
    """
    mappings = {
        "virtual_circuit": "virtual_circuit_id",
        "interface": "interface_id"
    }
    return await _search("circuits/virtual-circuit-terminations/", args, mappings)


@mcp.tool(
    annotations={
        "title": "Get Virtual Circuit Termination Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_virtual_circuit_termination_details(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Get virtual circuit termination by ID (circuits/virtual-circuit-terminations/{id}/).
    Accepts: id (required)
        id: Numeric ID of the virtual circuit termination to fetch. Returns `[obj]` or `[]`.
    """
    if "id" not in args:
        return []
    return await _get_detail("circuits/virtual-circuit-terminations/", args["id"])


# circuits/virtual-circuit-types

@mcp.tool(
    annotations={
        "title": "Search Virtual Circuit Types",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_virtual_circuit_types(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Search virtual circuit types (circuits/virtual-circuit-types/).
    Accepts: name, limit
        name: Name of the virtual circuit type (case-insensitive contains match)
        limit: Maximum number of results to return (default 10)
    
    Returns a list of NetBox virtual circuit type objects (the `results` list) or an empty list.
    """
    mappings = {"name": "name__ic"}
    return await _search("circuits/virtual-circuit-types/", args, mappings)


@mcp.tool(
    annotations={
        "title": "Get Virtual Circuit Type Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_virtual_circuit_type_details(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Get virtual circuit type by ID (circuits/virtual-circuit-types/{id}/).
    Accepts: id (required)
        id: Numeric ID of the virtual circuit type to fetch. Returns `[obj]` or `[]`.
    """
    if "id" not in args:
        return []
    return await _get_detail("circuits/virtual-circuit-types/", args["id"])


