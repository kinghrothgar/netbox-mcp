"""Tools for the NetBox extras app (selected read-useful resources)."""

from typing import Any, Dict

from ..helpers import _get_detail, _get_list, _search  # noqa: F401
from ..server import mcp


# --- extras (tags, journal entries, config contexts/templates, custom fields) ---

# extras/tags

@mcp.tool(
    annotations={
        "title": "Search Tags",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_tags(args: Dict[str, Any]) -> Dict[str, Any]:
    """Search tags (extras/tags/).
    Accepts: name, slug, content_type, q, limit
        name: Tag name (case-insensitive contains match)
        slug: Tag slug (exact match)
        content_type: Content type the tag is restricted to (e.g. 'dcim.device')
        q: Free-text search across name and description
        limit: Maximum number of results to return (default 10)

    Returns `{count, results}` (NetBox total + page). Default `brief=true`
    for compact tag objects; pass `brief=false` for full objects. Use
    `offset` to paginate, `fields`/`exclude` to project, `limit` capped at 100.
    """
    mappings = {
        "name": "name__ic",
        "slug": "slug",
        "content_type": "content_type",
        "q": "q",
    }
    return await _search("extras/tags/", args, mappings)


@mcp.tool(
    annotations={
        "title": "Get Tag Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_tag_details(args: Dict[str, Any]) -> Dict[str, Any]:
    """Get tag by ID (extras/tags/{id}/).
    Accepts: id (required)
        id: Numeric ID of the tag to fetch. Returns the envelope `{"results": [obj]}` or `{"results": []}`.
    """
    if "id" not in args:
        return {"results": []}
    return await _get_detail("extras/tags/", args["id"], args)


# extras/journal-entries

@mcp.tool(
    annotations={
        "title": "Search Journal Entries",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_journal_entries(args: Dict[str, Any]) -> Dict[str, Any]:
    """Search journal entries (extras/journal-entries/).
    Accepts: assigned_object_type, assigned_object_id, created_by, kind,
             created_after, created_before, q, tag, limit
        assigned_object_type: Content type of the assigned object (e.g. 'dcim.device')
        assigned_object_id: Numeric ID of the assigned object
        created_by: User ID
        kind: 'info', 'success', 'warning', or 'danger'
        created_after: ISO-8601 timestamp lower bound
        created_before: ISO-8601 timestamp upper bound
        q: Free-text search across comments
        tag: Tag slug (single)
        limit: Maximum number of results to return (default 10)

    Returns `{count, results}` (NetBox total + page). Default `brief=true`
    for compact journal entry objects; pass `brief=false` for full objects. Use
    `offset` to paginate, `fields`/`exclude` to project, `limit` capped at 100.
    """
    mappings = {
        "assigned_object_type": "assigned_object_type",
        "assigned_object_id": "assigned_object_id",
        "created_by": "created_by_id",
        "kind": "kind",
        "created_after": "created__gte",
        "created_before": "created__lte",
        "q": "q",
        "tag": "tag",
    }
    return await _search("extras/journal-entries/", args, mappings)


@mcp.tool(
    annotations={
        "title": "Get Journal Entry Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_journal_entry_details(args: Dict[str, Any]) -> Dict[str, Any]:
    """Get journal entry by ID (extras/journal-entries/{id}/).
    Accepts: id (required)
        id: Numeric ID of the journal entry to fetch. Returns the envelope `{"results": [obj]}` or `{"results": []}`.
    """
    if "id" not in args:
        return {"results": []}
    return await _get_detail("extras/journal-entries/", args["id"], args)


# extras/config-contexts

@mcp.tool(
    annotations={
        "title": "Search Config Contexts",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_config_contexts(args: Dict[str, Any]) -> Dict[str, Any]:
    """Search config contexts (extras/config-contexts/).
    Accepts: name, is_active, region, site_group, site, location, role,
             platform, cluster_type, cluster_group, cluster, tenant_group,
             tenant, tag, data_source, data_synced, q, limit
        name: Context name (case-insensitive contains match)
        is_active: Boolean
        region: Region ID or slug
        site_group: Site group ID or slug
        site: Site ID or slug
        location: Location ID or slug
        role: Device role ID or slug
        platform: Platform ID or slug
        cluster_type: Cluster type ID or slug
        cluster_group: Cluster group ID or slug
        cluster: Cluster ID
        tenant_group: Tenant group ID or slug
        tenant: Tenant ID or slug
        tag: Tag slug (single)
        data_source: Data source ID
        data_synced: Boolean
        q: Free-text search across name and description
        limit: Maximum number of results to return (default 10)

    Returns `{count, results}` (NetBox total + page). Default `brief=true`
    for compact config context objects; pass `brief=false` for full objects. Use
    `offset` to paginate, `fields`/`exclude` to project, `limit` capped at 100.
    """
    mappings = {
        "name": "name__ic",
        "is_active": "is_active",
        "region": "region",
        "site_group": "site_group",
        "site": "site",
        "location": "location",
        "role": "role",
        "platform": "platform",
        "cluster_type": "cluster_type",
        "cluster_group": "cluster_group",
        "cluster": "cluster_id",
        "tenant_group": "tenant_group",
        "tenant": "tenant",
        "tag": "tag",
        "data_source": "data_source",
        "data_synced": "data_synced",
        "q": "q",
    }
    return await _search("extras/config-contexts/", args, mappings)


@mcp.tool(
    annotations={
        "title": "Get Config Context Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_config_context_details(args: Dict[str, Any]) -> Dict[str, Any]:
    """Get config context by ID (extras/config-contexts/{id}/).
    Accepts: id (required)
        id: Numeric ID of the config context to fetch. Returns the envelope `{"results": [obj]}` or `{"results": []}`.
    """
    if "id" not in args:
        return {"results": []}
    return await _get_detail("extras/config-contexts/", args["id"], args)


# extras/config-templates

@mcp.tool(
    annotations={
        "title": "Search Config Templates",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_config_templates(args: Dict[str, Any]) -> Dict[str, Any]:
    """Search config templates (extras/config-templates/).
    Accepts: name, data_source, data_synced, q, tag, limit
        name: Template name (case-insensitive contains match)
        data_source: Data source ID
        data_synced: Boolean
        q: Free-text search across name and description
        tag: Tag slug (single)
        limit: Maximum number of results to return (default 10)

    Returns `{count, results}` (NetBox total + page). Default `brief=true`
    for compact config template objects; pass `brief=false` for full objects. Use
    `offset` to paginate, `fields`/`exclude` to project, `limit` capped at 100.
    """
    mappings = {
        "name": "name__ic",
        "data_source": "data_source",
        "data_synced": "data_synced",
        "q": "q",
        "tag": "tag",
    }
    return await _search("extras/config-templates/", args, mappings)


@mcp.tool(
    annotations={
        "title": "Get Config Template Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_config_template_details(args: Dict[str, Any]) -> Dict[str, Any]:
    """Get config template by ID (extras/config-templates/{id}/).
    Accepts: id (required)
        id: Numeric ID of the config template to fetch. Returns the envelope `{"results": [obj]}` or `{"results": []}`.
    """
    if "id" not in args:
        return {"results": []}
    return await _get_detail("extras/config-templates/", args["id"], args)


# extras/custom-fields

@mcp.tool(
    annotations={
        "title": "Search Custom Fields",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_custom_fields(args: Dict[str, Any]) -> Dict[str, Any]:
    """Search custom fields (extras/custom-fields/).
    Accepts: name, label, group_name, type, required, content_types,
             choice_set, q, limit
        name: Internal name (case-insensitive contains match)
        label: Display label (case-insensitive contains match)
        group_name: Group name (case-insensitive contains match)
        type: Field type (e.g. 'text', 'integer', 'boolean', 'select', 'multiselect',
              'object', 'multiobject', 'date', 'datetime', 'url', 'json')
        required: Boolean
        content_types: Content types the field applies to (e.g. 'dcim.device')
        choice_set: Choice set ID
        q: Free-text search across name, label, and description
        limit: Maximum number of results to return (default 10)

    Returns `{count, results}` (NetBox total + page). Default `brief=true`
    for compact custom field objects; pass `brief=false` for full objects. Use
    `offset` to paginate, `fields`/`exclude` to project, `limit` capped at 100.
    """
    mappings = {
        "name": "name__ic",
        "label": "label__ic",
        "group_name": "group_name__ic",
        "type": "type",
        "required": "required",
        "content_types": "content_types",
        "choice_set": "choice_set_id",
        "q": "q",
    }
    return await _search("extras/custom-fields/", args, mappings)


@mcp.tool(
    annotations={
        "title": "Get Custom Field Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_custom_field_details(args: Dict[str, Any]) -> Dict[str, Any]:
    """Get custom field by ID (extras/custom-fields/{id}/).
    Accepts: id (required)
        id: Numeric ID of the custom field to fetch. Returns the envelope `{"results": [obj]}` or `{"results": []}`.
    """
    if "id" not in args:
        return {"results": []}
    return await _get_detail("extras/custom-fields/", args["id"], args)


# extras/custom-field-choice-sets

@mcp.tool(
    annotations={
        "title": "Search Custom Field Choice Sets",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def search_custom_field_choice_sets(args: Dict[str, Any]) -> Dict[str, Any]:
    """Search custom field choice sets (extras/custom-field-choice-sets/).
    Accepts: name, base_choices, choice, q, limit
        name: Choice set name (case-insensitive contains match)
        base_choices: Base choice set name (NetBox built-in)
        choice: Specific choice value present in the set
        q: Free-text search across name and description
        limit: Maximum number of results to return (default 10)

    Returns `{count, results}` (NetBox total + page). Default `brief=true`
    for compact custom field choice set objects; pass `brief=false` for full objects. Use
    `offset` to paginate, `fields`/`exclude` to project, `limit` capped at 100.
    """
    mappings = {
        "name": "name__ic",
        "base_choices": "base_choices",
        "choice": "choice",
        "q": "q",
    }
    return await _search("extras/custom-field-choice-sets/", args, mappings)


@mcp.tool(
    annotations={
        "title": "Get Custom Field Choice Set Details",
        "readOnlyHint": True,
        "openWorldHint": True
    }
)
async def get_custom_field_choice_set_details(args: Dict[str, Any]) -> Dict[str, Any]:
    """Get custom field choice set by ID (extras/custom-field-choice-sets/{id}/).
    Accepts: id (required)
        id: Numeric ID of the choice set to fetch. Returns the envelope `{"results": [obj]}` or `{"results": []}`.
    """
    if "id" not in args:
        return {"results": []}
    return await _get_detail("extras/custom-field-choice-sets/", args["id"], args)
