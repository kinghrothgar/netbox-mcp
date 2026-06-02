# COPILOT_INSTRUCTIONS — FastMCP NetBox tools

Purpose
------
This document describes the expected structure, conventions, and contributor guidance for the FastMCP-based NetBox tool collection in this repository. The core rule: every NetBox data element in the model must be represented by two explicit MCP tools:

- `search_<resource>(args)`: queries the API collection endpoint and supports a set of optional filters.
- `get_<resource>_details(args)`: fetches a single object by ID and returns the envelope `{"results": [obj]}` or `{"results": []}`.

This repository requires hand-written, descriptive docstrings for each tool (no programmatic/dynamic registrar for final production code). Tools must be grouped and ordered by NetBox API root.

Project structure
----------------
```
.
├── netbox_mcp/
│   ├── __init__.py
│   ├── __main__.py                 # `python -m netbox_mcp` entry point
│   ├── client.py                   # NetBoxClient + shared httpx client + env config
│   ├── helpers.py                  # _build_params, _search, _get_detail, _get_list, _get_action
│   ├── server.py                   # mcp = FastMCP(...) singleton
│   ├── version.py                  # supported NetBox versions + tool-gating decorator
│   └── tools/
│       ├── __init__.py             # side-effect imports of every tools.<app>
│       ├── circuits.py
│       ├── core.py
│       ├── dcim.py
│       ├── extras.py
│       ├── ipam.py
│       ├── tenancy.py
│       ├── virtualization.py
│       ├── vpn.py
│       └── wireless.py
├── tests/                          # pytest integration suite against demo.netbox.dev
├── Dockerfile                      # Container image build
├── Makefile                        # build-dev / run-dev / test-demo targets
├── .github/
│   └── copilot-instructions.md     # This file - Copilot coding guidelines
├── .gitignore                      # Git ignore patterns
├── AGENTS.md                       # Repo-wide guidance for coding agents
├── CONTRIBUTING.md                 # Contributor quick-start
└── README.md                       # User-facing documentation
```

Repository conventions
---------------------
- Tools live under `netbox_mcp/tools/<app>.py`, one module per NetBox app.
- Shared infrastructure: `netbox_mcp/client.py` (NetBoxClient wrapping `httpx.AsyncClient`), `netbox_mcp/helpers.py` (search/detail/list helpers), `netbox_mcp/server.py` (`mcp = FastMCP(...)` singleton).
- MCP registration: functions are decorated with `@mcp.tool` and are async functions taking `args: Dict[str, Any]`. Every tool returns a `Dict[str, Any]` envelope:
  - Search tools return `{"count": int, "results": [...]}`.
  - Detail and list-sub-resource tools return `{"results": [...]}` (one element on success, empty on missing/unknown id).
  - Action-endpoint tools (trace, rack elevation) return `{"result": <payload>}`; on error, `result` is `[]`.

  Tools register at import time; `netbox_mcp/tools/__init__.py` imports every submodule so all decorators fire before the server starts.

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
Each NetBox app gets its own module under `netbox_mcp/tools/`. Modules
currently present:

1. circuits
2. core
3. dcim
4. extras
5. ipam
6. tenancy
7. virtualization
8. vpn
9. wireless

`plugins`, `status`, and `users` are not currently exposed; add modules
for them following the same conventions if/when needed.

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
- Signatures: every tool is `async def <name>(args: Dict[str, Any]) -> Dict[str, Any]`. Do not annotate with `List[...]` — every tool returns the dict envelope described above.
- `search_` behavior: accept a limited set of optional filter args (documented
  in the docstring) plus the shared knobs `limit`, `offset`, `brief`, `fields`,
  `exclude` (handled by `helpers._build_params` / `helpers._search`). Return
  `{"count": int, "results": [...]}` where `count` is the NetBox total and
  `results` is the current page. Default `brief=true` for compact payloads.
- `get_` behavior: accept at minimum `id` in `args`; if present fetch the
  `.../{id}/` endpoint via `helpers._get_detail(endpoint, args["id"], args)`
  and return its envelope (`{"results": [obj]}` or `{"results": []}`). Pass
  `args` through so `fields`, `exclude`, and `raw` are honoured. By default
  a small set of noisy keys is stripped from the returned object; pass
  `raw=true` to disable.
- Action endpoints (`*/trace/`, `racks/{id}/elevation/`) use
  `helpers._get_action(endpoint, args)` and return `{"result": <payload>}`.
- List sub-resources (`available-ips`, `available-prefixes`,
  `available-asns`, `available-vlans`) use `helpers._get_list(endpoint, args)`
  and return `{"results": [...]}`.

Docstrings and content requirements
----------------------------------
Each tool must include a multi-line docstring that:
- Briefly describes the purpose and which NetBox endpoint it queries.
- Lists accepted args and their types/semantics. Be explicit about which args are required vs optional.
- Describes the return value envelope (search: `{count, results}`; detail/list: `{"results": [...]}`; action: `{"result": <payload>}`) and error behavior.
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
- Network or 4xx/5xx responses are caught inside the shared helpers and surfaced as the empty envelope (`{"results": []}` or `{"result": []}`), so a transport-level failure looks like "looked up, nothing there" rather than raising into the LLM.
- Validation errors (missing required arguments such as `id`) should return the matching empty envelope (`{"results": []}` for detail/list tools, `{"result": []}` for action tools) rather than raising.

Testing & verification
----------------------
When you add or reorder tools:

- Run a quick syntax check:

```bash
python3 -m py_compile netbox_mcp/__main__.py netbox_mcp/tools/*.py
```

- Run the integration suite against `demo.netbox.dev`:

```bash
make test-demo
```

  This builds the dev image plus the test image (`tests/Dockerfile`),
  bootstraps a demo NetBox account on first run (cached in
  `.netbox-demo-creds.json`), spins up the netbox-mcp container, and
  runs pytest against it. New tools should at minimum be covered by
  the shape assertions in `tests/test_schema.py`; tools backed by new
  helper classes should grow an envelope-shape assertion in
  `tests/test_smoke.py`.

- Verify imports (ensure `fastmcp`, `httpx`, and typing hints are present).
- Keep changes small and run the syntax check after reordering large blocks.

How to add a new resource (step-by-step)
----------------------------------------
1. Open the corresponding `netbox_mcp/tools/<app>.py` module. If the
   NetBox app doesn't have a module yet, create one and add a side-effect
   import for it to `netbox_mcp/tools/__init__.py`.
2. Use the existing helpers from `netbox_mcp/helpers.py`
   (`_search`, `_get_detail`, `_get_list`, `_get_action`) — they're
   imported at the top of each tools module.
3. Create `search_<resource>` function with:
   - A clear docstring (purpose, accepted args, returns).
   - A `mappings` dict from incoming arg name to NetBox query param name.
   - `return await _search("dcim/example/", args, mappings)`.
4. Create `get_<resource>_details` function with:
   - Docstring describing it accepts `id` and returns the envelope `{"results": [obj]}` or `{"results": []}`.
   - If `id` missing: `return {"results": []}`.
   - If `id` present: `return await _get_detail("dcim/example/", args["id"], args)`.
5. Run `python3 -m py_compile netbox_mcp/tools/<app>.py` and fix any syntax issues.
6. Run `make test-demo` to confirm the new tool round-trips against the demo NetBox.
7. Commit only the minimal relevant changes and include a short commit message describing the resource added.

Examples
--------
Example Search (sites):

- Function name: `search_sites`
- Endpoint: `dcim/sites/`
- Accepted args: `name` (partial/case-insensitive), `status`, `region`, `location`, plus the shared `limit` / `offset` / `brief` / `fields` / `exclude`
- Return: `{"count": int, "results": [site_dict, ...]}`

Example Get (site details):

- Function name: `get_site_details`
- Endpoint: `dcim/sites/{id}/`
- Accepted args: `id` (required)
- Return: `{"results": [site_dict]}` or `{"results": []}`
