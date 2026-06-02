# NetBox MCP Server

A small Model Context Protocol (MCP) server built with FastMCP that provides an interface to a NetBox instance.

This repository exposes NetBox resources (sites, site-groups, devices, etc.) as MCP tools and runs a streaming HTTP transport so clients can connect and receive streamed responses from the MCP server.

## Architecture (FastMCP + streaming HTTP)

- FastMCP: The MCP tool registry and runtime. Tools are defined under
  `netbox_mcp/tools/` (one module per NetBox app) and decorated with
  `@mcp.tool` on the shared `mcp` singleton from `netbox_mcp/server.py`.
- NetBoxClient: a tiny async helper in `netbox_mcp/client.py` that wraps
  `httpx.AsyncClient` to call the NetBox API.
- Streaming HTTP transport: the MCP server is started with
  `mcp.run(transport="http", ...)` which runs an HTTP server that supports
  a streaming/chunked response transport. This is useful for clients that
  want to consume events or long-running responses incrementally rather
  than waiting for the entire result.

Conceptually the flow is:

1. Client connects to the FastMCP streaming HTTP endpoint.
2. Client requests a tool (for example, `search_sites` or `get_site_group_details`).
3. FastMCP calls the associated Python function in the relevant
   `netbox_mcp/tools/<app>.py` module, which may in turn call NetBox via
   `NetBoxClient`.
4. The result is streamed back over the HTTP transport as it becomes available.

> Note: The low-level HTTP path/shape is provided by the FastMCP runtime. Clients that wish to connect should use a compatible MCP client or an HTTP client that supports reading chunked / streaming responses.

## Supported NetBox versions

This server targets a specific NetBox minor release. Tools that map to
endpoints introduced in a newer release are only registered when that
release is selected; tools that map to endpoints removed in a newer
release are not registered when that release is selected. Currently
supported targets:

- `4.5`
- `4.6` (default)

The selected version is logged to stderr at startup.

Notable version-gated additions on 4.6:

- `search_rack_groups` / `get_rack_group_details` (`dcim/rack-groups/`)
- `search_cable_bundles` / `get_cable_bundle_details` (`dcim/cable-bundles/`)
- `search_virtual_machine_types` / `get_virtual_machine_type_details`
  (`virtualization/virtual-machine-types/`)
- `virtual_machine_type` filter on `search_virtual_machines`
- `role` filter on `search_asns`

## Configuration

Every runtime knob can be set via either a CLI flag or an environment
variable. Precedence is **CLI flag > env var > built-in default**.

| CLI flag            | Env var          | Default                       | Description                                                                |
| ------------------- | ---------------- | ----------------------------- | -------------------------------------------------------------------------- |
| `--netbox-version`  | `NETBOX_VERSION` | `4.6`                         | Target NetBox minor version (`4.5` or `4.6`).                              |
| `--netbox-url`      | `NETBOX_URL`     | `https://netbox.example.com`  | Base URL of the NetBox instance.                                           |
| `--netbox-token`    | `NETBOX_TOKEN`   | *(empty)*                     | NetBox API token with read permissions. See security note below.           |
| `--mcp-host`        | `MCP_HOST`       | `0.0.0.0`                     | Address the FastMCP HTTP transport binds to.                               |
| `--mcp-port`        | `MCP_PORT`       | `8000`                        | Port for the FastMCP HTTP transport. Must be an integer.                   |

Run `python3 -m netbox_mcp --help` to see the resolved defaults at
invocation time (env vars already in scope appear as the default).

### Security note on `--netbox-token`

The CLI flag exists for ad-hoc and debugging use. Command-line
arguments are visible in `ps`, `/proc/<pid>/cmdline`, shell history, and
container runtime metadata. For real deployments prefer `NETBOX_TOKEN`
via `docker run --env-file`, a Kubernetes Secret, systemd
`EnvironmentFile=`, or an equivalent mechanism.

## Run the server

```bash
# Env-var style (recommended for deployments)
export NETBOX_URL="https://netbox.example.com"
export NETBOX_TOKEN="0123456789abcdef0123456789abcdef01234567"
export NETBOX_VERSION=4.6
export MCP_HOST=0.0.0.0
export MCP_PORT=8000
python3 -m netbox_mcp

# CLI-flag style (handy for one-off runs)
python3 -m netbox_mcp \
    --netbox-url https://netbox.example.com \
    --netbox-token 0123456789abcdef0123456789abcdef01234567 \
    --netbox-version 4.5 \
    --mcp-host 0.0.0.0 \
    --mcp-port 8000
```

The server binds to the resolved `--mcp-host` / `--mcp-port` and serves
the FastMCP HTTP transport.

For local development, `make build-dev` builds the container image and
`make run-dev` runs it with `--network host` so the container inherits
the host's DNS resolver. See `.env.sample` for the expected env vars.

## Tools included

`netbox_mcp/tools/` registers MCP tools for NetBox resources, organized
one module per NetBox app (`circuits`, `dcim`, `tenancy`, `ipam`, ...).
Examples:

- `search_sites` — search of `dcim/sites/` (supports partial/case-insensitive name queries)
- `get_site_details` — site lookup
- `search_site_groups` — search of `dcim/site-groups/` (supports `name__ic`)
- `get_site_group_details` — single site-group lookup by `id`
- `search_prefixes` — search of `ipam/prefixes/` with CIDR containment filters
- `get_prefix_available_ips` — list free IPs inside a prefix

You can add more tools following the repository conventions: each NetBox resource has a `search_<resource>` and `get_<resource>_details` tool.

## Verifying / testing

- Quick syntax check:

```bash
python3 -m py_compile netbox_mcp/__main__.py netbox_mcp/tools/*.py
```

- Start the server and use an HTTP client that supports streaming (for example, `curl --no-buffer` or a custom MCP client) to connect to the FastMCP HTTP transport and invoke tools.

Because the exact HTTP request shape (paths, headers and payload) is defined by the FastMCP runtime and clients, prefer using an existing MCP client library where available. If you're building a custom client, make sure it supports reading chunked responses so streamed results can be consumed incrementally.

## Contributing

If you add tools, follow the repo conventions documented in `.github/copilot-instructions.md`: each resource should have a `search_` and a `get_` tool with descriptive docstrings and consistent parameter mapping.

## License

This project is provided as-is.
