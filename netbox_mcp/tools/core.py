"""Tools for the NetBox core app (selected read-useful resources)."""

from typing import Any, Dict

from ..helpers import _get_detail, _get_list, _search  # noqa: F401
from ..server import mcp


# --- core (object types and change log) ---

# core/object-types

@mcp.tool(
    annotations={
        "title": "Search Object Types",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_object_types(args: Dict[str, Any]) -> Dict[str, Any]:
    """Search object types / content types (core/object-types/).
    Accepts: app_label, model, q, limit
        app_label: NetBox app label (e.g. 'dcim', 'ipam', 'virtualization')
        model: Model name (e.g. 'device', 'interface', 'virtualmachine')
        q: Free-text search
        limit: Maximum number of results to return (default 10)

    Returns `{count, results}` (NetBox total + page). Default `brief=true`
    for compact object type objects; pass `brief=false` for full objects. Use
    `offset` to paginate, `fields`/`exclude` to project, `limit` capped at 100.

    Use this to resolve `app_label.model` strings to/from numeric content-type
    IDs when other tools return generic relations like `assigned_object_type`.
    """
    mappings = {
        "app_label": "app_label",
        "model": "model",
        "q": "q",
    }
    return await _search("core/object-types/", args, mappings)


@mcp.tool(
    annotations={
        "title": "Get Object Type Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_object_type_details(args: Dict[str, Any]) -> Dict[str, Any]:
    """Get object type by ID (core/object-types/{id}/).
    Accepts: id (required)
        id: Numeric ID of the object type to fetch. Returns the envelope `{"results": [obj]}` or `{"results": []}`.
    """
    if "id" not in args:
        return {"results": []}
    return await _get_detail("core/object-types/", args["id"], args)


# core/object-changes

@mcp.tool(
    annotations={
        "title": "Search Object Changes",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_object_changes(args: Dict[str, Any]) -> Dict[str, Any]:
    """Search object change log entries (core/object-changes/).
    Accepts: user, user_name, action, changed_object_type, changed_object_id,
             related_object_type, related_object_id, time_after, time_before,
             request_id, q, limit
        user: User ID
        user_name: Username (case-insensitive contains match)
        action: 'create', 'update', or 'delete'
        changed_object_type: Content type of the changed object (e.g. 'dcim.device')
        changed_object_id: Numeric ID of the changed object
        related_object_type: Content type of a related object
        related_object_id: Numeric ID of a related object
        time_after: ISO-8601 timestamp lower bound
        time_before: ISO-8601 timestamp upper bound
        request_id: UUID of the request that produced the change
        q: Free-text search
        limit: Maximum number of results to return (default 10)

    Returns `{count, results}` (NetBox total + page). Default `brief=true`
    for compact object change objects; pass `brief=false` for full objects. Use
    `offset` to paginate, `fields`/`exclude` to project, `limit` capped at 100.
    """
    mappings = {
        "user": "user_id",
        "user_name": "user_name__ic",
        "action": "action",
        "changed_object_type": "changed_object_type",
        "changed_object_id": "changed_object_id",
        "related_object_type": "related_object_type",
        "related_object_id": "related_object_id",
        "time_after": "time__gte",
        "time_before": "time__lte",
        "request_id": "request_id",
        "q": "q",
    }
    return await _search("core/object-changes/", args, mappings)


@mcp.tool(
    annotations={
        "title": "Get Object Change Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_object_change_details(args: Dict[str, Any]) -> Dict[str, Any]:
    """Get object change by ID (core/object-changes/{id}/).
    Accepts: id (required)
        id: Numeric ID of the object change to fetch. Returns the envelope `{"results": [obj]}` or `{"results": []}`.
    """
    if "id" not in args:
        return {"results": []}
    return await _get_detail("core/object-changes/", args["id"], args)
