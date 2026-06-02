# COPILOT_INSTRUCTIONS — FastMCP NetBox tools

Purpose
------
This document describes the expected structure, conventions, and contributor guidance for the FastMCP-based NetBox tool collection in this repository. The core rule: every NetBox data element in the model must be represented by two explicit MCP tools:

- `search_<resource>(args)`: queries the API collection endpoint and supports a set of optional filters.
- `get_<resource>_details(args)`: fetches a single object by ID and returns a single-element list or an empty list.

This repository requires hand-written, descriptive docstrings for each tool (no programmatic/dynamic registrar for final production code). Tools must be grouped and ordered by NetBox API root.

Project structure
----------------
```
.
├── netbox_mcp/
│   ├── __init__.py
│   ├── __main__.py                 # `python -m netbox_mcp` entry point
│   ├── client.py                   # NetBoxClient + shared httpx client + env config
│   ├── helpers.py                  # _build_params, _search, _get_detail, _get_list
│   ├── server.py                   # mcp = FastMCP(...) singleton
│   └── tools/
│       ├── __init__.py             # side-effect imports of every tools.<app>
│       ├── circuits.py
│       ├── dcim.py
│       ├── tenancy.py
│       └── ipam.py
├── Dockerfile                      # Container image build
├── Makefile                        # build-dev / run-dev targets
├── .github/
│   └── copilot-instructions.md     # This file - Copilot coding guidelines
├── .gitignore                      # Git ignore patterns
└── README.md                       # User-facing documentation
```

Repository conventions
---------------------
- Tools live under `netbox_mcp/tools/<app>.py`, one module per NetBox app.
- Shared infrastructure: `netbox_mcp/client.py` (NetBoxClient wrapping `httpx.AsyncClient`), `netbox_mcp/helpers.py` (search/detail/list helpers), `netbox_mcp/server.py` (`mcp = FastMCP(...)` singleton).
- MCP registration: functions are decorated with `@mcp.tool` and are async functions with signature `async def func(args: Dict[str, Any]) -> List[Dict[str, Any]]`. Tools register at import time; `netbox_mcp/tools/__init__.py` imports every submodule so all decorators fire before the server starts.

Dependencies and setup
---------------------
This project requires Python 3.7+ and the following dependencies:
- `fastmcp` — FastMCP framework for building MCP servers
- `httpx` — Async HTTP client for making requests to the NetBox API

To set up the development environment:
1. Ensure Python 3.7+ is installed
2. Install dependencies: `pip install fastmcp httpx`
3. Set environment variables (see README.md):
   - `NETBOX_URL` — Base URL to your NetBox instance
   - `NETBOX_TOKEN` — NetBox API token with read permissions
   - `MCP_HOST` — Bind address for the FastMCP HTTP transport (default: 0.0.0.0)
   - `MCP_PORT` — Port for the FastMCP HTTP transport (default: 8000)
4. Run the server: `python3 -m netbox_mcp`

API grouping and ordering
-------------------------
Each NetBox app gets its own module under `netbox_mcp/tools/`. The recommended file ordering is:

1. circuits
2. core
3. dcim
4. extras
5. ipam
6. plugins
7. status
8. tenancy
9. users
10. virtualization
11. vpn
12. wireless

Inside each `netbox_mcp/tools/<app>.py` module, use hierarchical
API-path comments for individual resources to mirror the NetBox API
path structure and make tools easy to find by endpoint:

# dcim/sites

# dcim/cables

The module docstring at the top of the file plays the role of the
previous group-level separator. Use simple `# <api-root>/<resource>`
comment lines above each resource's tools within the module.

Naming and signatures
---------------------
- Search tool naming: `search_<resource>` where `<resource>` is a concise, snake_case name matching the API resource (examples: `search_sites`, `search_devices`, `search_vlans`).
- Get tool naming: `get_<resource>_details` (examples: `get_site_details`, `get_device_details`).
- All tools: `async def name(args: Dict[str, Any]) -> List[Dict[str, Any]]`.
- `search_` behavior: accept a limited set of optional filter args (documented in the docstring) and return the NetBox `results` list or an empty list.
- `get_` behavior: accept at minimum `id` in `args`; if present fetch the `.../{id}/` endpoint and return `[object]` or `[]`.

Docstrings and content requirements
----------------------------------
Each tool must include a multi-line docstring that:
- Briefly describes the purpose and which NetBox endpoint it queries.
- Lists accepted args and their types/semantics. Be explicit about which args are required vs optional.
- Describes the return value (list of NetBox objects or single-element list) and error behavior.
- Notes any edge-cases or special semantics (e.g., when name lookup is supported, how multiple matches are handled).

Do not include long human chatter in the return value: return structured JSON objects (NetBox dicts) so downstream tools can consume them reliably.

Parameter mapping guidance
--------------------------
Map incoming `args` to NetBox query parameters in a consistent way:
- Partial/case-insensitive string matches: use `name__ic` where appropriate.
- Exact ID filters: pass numeric ids as-is (e.g., `site`, `device`).
- Defaults: set a reasonable `limit` default (typically 10 or 100 depending on the endpoint). Always read `args.get("limit", <default>)`.

Errors and exceptions
---------------------
- Network or server errors should raise exceptions so the MCP server can surface them.
- Validation errors (missing required arguments) should return an empty list rather than raising, following existing repo behavior.

Testing & verification
----------------------
When you add or reorder tools:

- Run a quick syntax check:

```bash
python3 -m py_compile netbox_mcp/__main__.py netbox_mcp/tools/*.py
```

- Verify imports (ensure `fastmcp`, `httpx`, and typing hints are present).
- Keep changes small and run the syntax check after reordering large blocks.

How to add a new resource (step-by-step)
----------------------------------------
1. Open the corresponding `netbox_mcp/tools/<app>.py` module. If the
   NetBox app doesn't have a module yet, create one and add a side-effect
   import for it to `netbox_mcp/tools/__init__.py`.
2. Use the existing helpers from `netbox_mcp/helpers.py`
   (`_search`, `_get_detail`, `_get_list`) — they're imported at the top
   of each tools module.
3. Create `search_<resource>` function with:
   - A clear docstring (purpose, accepted args, returns).
   - A `mappings` dict from incoming arg name to NetBox query param name.
   - `return await _search("dcim/example/", args, mappings)`.
4. Create `get_<resource>_details` function with:
   - Docstring describing it accepts `id`.
   - If `id` present: `return await _get_detail("dcim/example/", args["id"])`.
5. Run `python3 -m py_compile netbox_mcp/tools/<app>.py` and fix any syntax issues.
6. Commit only the minimal relevant changes and include a short commit message describing the resource added.

Examples
--------
Example Search (sites):

- Function name: `search_sites`
- Endpoint: `dcim/sites/`
- Accepted args: `site_id` (exact), `site_name` (partial)
- Return: list of site dicts

Example Get (site details):

- Function name: `get_site_details`
- Endpoint: `dcim/sites/{id}/`
- Accepted args: `id` (required)
- Return: `[site_dict]` or `[]`
