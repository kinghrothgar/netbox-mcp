# Contributing to NetBox MCP Server

Thank you for your interest in contributing to the NetBox MCP Server project!

## Getting Started

The development workflow is fully containerised. You need `git`,
`docker` (with `buildx`), and `make` on the host — nothing else. Do
not `pip install` anything locally; the toolchain lives in the dev
image.

1. **Clone the repository**
   ```bash
   git clone https://github.com/kinghrothgar/netbox-mcp.git
   cd netbox-mcp
   ```

2. **Configure environment variables**
   Copy `.env.sample` to `.env` and fill in your NetBox URL and token.
   The `Makefile` reads `.env` and passes it to the dev container via
   `--env-file`:

   ```bash
   cp .env.sample .env
   # edit .env: NETBOX_URL, NETBOX_TOKEN, optionally NETBOX_VERSION,
   # MCP_HOST, MCP_PORT
   ```

3. **Build and run the dev image**
   ```bash
   make build-dev   # build netbox-mcp:dev
   make run-dev     # run it with --network host and your .env
   ```

## Development Guidelines

This repository follows specific conventions for adding NetBox MCP tools. **Please read the detailed guidelines in [`.github/copilot-instructions.md`](.github/copilot-instructions.md)** before contributing.

### Quick Summary

- Each NetBox resource must have two tools: `search_<resource>` and `get_<resource>_details`
- Tools are organized one module per NetBox app under `netbox_mcp/tools/` (`circuits.py`, `core.py`, `dcim.py`, `extras.py`, `ipam.py`, `tenancy.py`, `virtualization.py`, `vpn.py`, `wireless.py`)
- All tools require descriptive docstrings with clear parameter documentation
- Use the helper functions `_search()`, `_get_detail()`, `_get_list()`, and `_get_action()` (defined in `netbox_mcp/helpers.py`) to reduce code duplication
- Return structured JSON objects (no human-readable messages in responses). Every helper returns a dict envelope (`{"count", "results"}`, `{"results": [...]}`, or `{"result": ...}`) rather than a bare list so FastMCP emits `structured_content` even on empty results

### Adding a New Resource

1. Identify the NetBox API endpoint and open the corresponding module in `netbox_mcp/tools/<app>.py` (create one if the app doesn't have a module yet, and import it from `netbox_mcp/tools/__init__.py`)
2. Create `search_<resource>` function with proper docstring and parameter mapping
3. Create `get_<resource>_details` function for single object lookup
4. Verify your changes by running `make test-demo` (see [Testing](#testing) below). This spins up the dev image inside a throwaway test container and runs pytest against `demo.netbox.dev`; any syntax error or broken tool surfaces there.
5. Commit with a clear message describing what was added

For detailed step-by-step instructions, see the "How to add a new resource (step-by-step)" section in [`.github/copilot-instructions.md`](.github/copilot-instructions.md).

## Code Style

- Follow Python conventions (PEP 8)
- Use type hints: `async def func(args: Dict[str, Any]) -> Dict[str, Any]` (every tool returns an envelope dict, not a bare list)
- Keep functions focused and single-purpose
- Include comprehensive docstrings for all tools

## Testing

All testing happens inside Docker via the `Makefile`. Do not invoke
`pytest`, `python3`, or `pip` on the host directly.

Before submitting a PR:

1. Run the integration suite against `demo.netbox.dev`:
   ```bash
   make test-demo
   ```
   This builds the dev image (`make build-dev`) and the test image
   (`tests/Dockerfile`), bootstraps a demo NetBox account on first run
   (cached in `.netbox-demo-creds.json`, mode 0600), spins up the
   netbox-mcp container, and runs the pytest suite against it. The
   harness picks the highest supported target version that the demo's
   `/api/status/` reports.
2. (Optional) Smoke-test the running server against your own NetBox by
   pointing `.env` at it and running `make run-dev`, then connecting
   with any MCP client over the FastMCP HTTP transport.
3. Verify parameter mapping matches NetBox API expectations by
   inspecting the relevant NetBox API reference and matching the
   `mappings` dict in your `search_*` tool.

## Questions or Issues?

If you have questions or encounter issues:
- Check the [`.github/copilot-instructions.md`](.github/copilot-instructions.md) for detailed guidance
- Review existing tools under `netbox_mcp/tools/` for examples
- Open an issue on GitHub for discussion

## License

By contributing to this project, you agree that your contributions will be licensed under the same license as the project.
