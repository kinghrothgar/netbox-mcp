"""Tools for the NetBox tenancy app."""

from typing import Any, Dict, List

from ..helpers import _get_detail, _get_list, _search
from ..server import mcp


# --- tenancy (tenants, contacts, etc.) ---

# tenancy

# tenancy/tenants

@mcp.tool(
    annotations={
        "title": "Search Tenants",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_tenants(args: Dict[str, Any]) -> Dict[str, Any]:
    """Search tenants (tenancy/tenants/).
    Accepts: name, group, limit
        name: Name of the tenant (case-insensitive contains match)
        group: Tenant group id or name (optional)
        limit: maximum number of results to return (default 10)

    Returns `{count, results}` (NetBox total + page). Default `brief=true`
    for compact tenant objects; pass `brief=false` for full objects. Use
    `offset` to paginate, `fields`/`exclude` to project, `limit` capped at 100.
    """
    mappings = {"name": "name__ic", "group": "tenant_group"}
    return await _search("tenancy/tenants/", args, mappings)


@mcp.tool(
    annotations={
        "title": "Get Tenant Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_tenant_details(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Get tenant details by ID (tenancy/tenants/{id}/).
    Accepts: id (required)
        id: Numeric ID of the tenant to fetch. Returns `[obj]` or `[]`.
    """
    if "id" not in args:
        return []
    return await _get_detail("tenancy/tenants/", args["id"], args)


# tenancy/tenant-groups

@mcp.tool(
    annotations={
        "title": "Search Tenant Groups",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_tenant_groups(args: Dict[str, Any]) -> Dict[str, Any]:
    """Search tenant groups (tenancy/tenant-groups/).
    Accepts: name, limit
        name: Name of the tenant group (case-insensitive contains match)
        limit: maximum number of results to return (default 10)

    Returns `{count, results}` (NetBox total + page). Default `brief=true`
    for compact tenant group objects; pass `brief=false` for full objects. Use
    `offset` to paginate, `fields`/`exclude` to project, `limit` capped at 100.
    """
    mappings = {"name": "name__ic"}
    return await _search("tenancy/tenant-groups/", args, mappings)


@mcp.tool(
    annotations={
        "title": "Get Tenant Group Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_tenant_group_details(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Get tenant group details by ID (tenancy/tenant-groups/{id}/).
    Accepts: id (required)
        id: Numeric ID of the tenant group to fetch. Returns `[obj]` or `[]`.
    """
    if "id" not in args:
        return []
    return await _get_detail("tenancy/tenant-groups/", args["id"], args)


# tenancy/contacts

@mcp.tool(
    annotations={
        "title": "Search Contacts",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_contacts(args: Dict[str, Any]) -> Dict[str, Any]:
    """Search contacts (tenancy/contacts/).
    Accepts: name, title, phone, email, address, limit
        name: Name of the contact (case-insensitive contains match)
        title: Contact's title or role (case-insensitive contains match)
        phone: Contact phone number (partial match)
        email: Contact email (case-insensitive contains match)
        address: Contact address (case-insensitive contains match)
        limit: maximum number of results to return (default 10)

    Returns `{count, results}` (NetBox total + page). Default `brief=true`
    for compact contact objects; pass `brief=false` for full objects. Use
    `offset` to paginate, `fields`/`exclude` to project, `limit` capped at 100.
    """
    mappings = {
        "name": "name__ic",
        "title": "title__ic",
        "phone": "phone__ic",
        "email": "email__ic",
        "address": "address__ic",
    }
    return await _search("tenancy/contacts/", args, mappings)


@mcp.tool(
    annotations={
        "title": "Get Contact Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_contact_details(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Get contact details by ID (tenancy/contacts/{id}/).
    Accepts: id (required)
        id: Numeric ID of the contact to fetch. Returns `[obj]` or `[]`.
    """
    if "id" not in args:
        return []
    return await _get_detail("tenancy/contacts/", args["id"], args)


# tenancy/contact-groups

@mcp.tool(
    annotations={
        "title": "Search Contact Groups",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_contact_groups(args: Dict[str, Any]) -> Dict[str, Any]:
    """Search contact groups (tenancy/contact-groups/).
    Accepts: name, limit
        name: Name of the contact group (case-insensitive contains match)
        limit: maximum number of results to return (default 10)

    Returns `{count, results}` (NetBox total + page). Default `brief=true`
    for compact contact group objects; pass `brief=false` for full objects. Use
    `offset` to paginate, `fields`/`exclude` to project, `limit` capped at 100.
    """
    mappings = {"name": "name__ic"}
    return await _search("tenancy/contact-groups/", args, mappings)


@mcp.tool(
    annotations={
        "title": "Get Contact Group Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_contact_group_details(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Get contact group details by ID (tenancy/contact-groups/{id}/).
    Accepts: id (required)
        id: Numeric ID of the contact group to fetch. Returns `[obj]` or `[]`.
    """
    if "id" not in args:
        return []
    return await _get_detail("tenancy/contact-groups/", args["id"], args)


# tenancy/contact-roles

@mcp.tool(
    annotations={
        "title": "Search Contact Roles",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_contact_roles(args: Dict[str, Any]) -> Dict[str, Any]:
    """Search contact roles (tenancy/contact-roles/).
    Accepts: name, limit
        name: Name of the contact role (case-insensitive contains match)
        limit: maximum number of results to return (default 10)

    Returns `{count, results}` (NetBox total + page). Default `brief=true`
    for compact contact role objects; pass `brief=false` for full objects. Use
    `offset` to paginate, `fields`/`exclude` to project, `limit` capped at 100.
    """
    mappings = {"name": "name__ic"}
    return await _search("tenancy/contact-roles/", args, mappings)


@mcp.tool(
    annotations={
        "title": "Get Contact Role Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_contact_role_details(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Get contact role details by ID (tenancy/contact-roles/{id}/).
    Accepts: id (required)
        id: Numeric ID of the contact role to fetch. Returns `[obj]` or `[]`.
    """
    if "id" not in args:
        return []
    return await _get_detail("tenancy/contact-roles/", args["id"], args)


# tenancy/contact-assignments

@mcp.tool(
    annotations={
        "title": "Search Contact Assignments",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_contact_assignments(args: Dict[str, Any]) -> Dict[str, Any]:
    """Search contact assignments (tenancy/contact-assignments/).
    Accepts: object_type, object_id, contact, group, role, priority, q, tag, limit
        object_type: Content type of the assigned object (e.g. 'dcim.device')
        object_id: Numeric ID of the assigned object
        contact: Contact ID
        group: Contact group ID or slug
        role: Contact role ID or slug
        priority: Priority value (e.g. 'primary', 'secondary', 'tertiary', 'inactive')
        q: Free-text search
        tag: Tag slug (single)
        limit: Maximum number of results to return (default 10)

    Returns `{count, results}` (NetBox total + page). Default `brief=true`
    for compact contact assignment objects; pass `brief=false` for full objects. Use
    `offset` to paginate, `fields`/`exclude` to project, `limit` capped at 100.
    """
    mappings = {
        "object_type": "object_type",
        "object_id": "object_id",
        "contact": "contact",
        "group": "group",
        "role": "role",
        "priority": "priority",
        "q": "q",
        "tag": "tag",
    }
    return await _search("tenancy/contact-assignments/", args, mappings)


@mcp.tool(
    annotations={
        "title": "Get Contact Assignment Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_contact_assignment_details(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Get contact assignment by ID (tenancy/contact-assignments/{id}/).
    Accepts: id (required)
        id: Numeric ID of the contact assignment to fetch. Returns `[obj]` or `[]`.
    """
    if "id" not in args:
        return []
    return await _get_detail("tenancy/contact-assignments/", args["id"], args)










