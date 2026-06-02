# Contributing to NetBox MCP Server

Thank you for your interest in contributing to the NetBox MCP Server project!

## Getting Started

1. **Clone the repository**
   ```bash
   git clone https://github.com/kinghrothgar/netbox-mcp.git
   cd netbox-mcp
   ```

2. **Install dependencies**
   ```bash
   pip install fastmcp httpx
   ```

3. **Set up environment variables**
   ```bash
   export NETBOX_URL="https://netbox.example.com"
   export NETBOX_TOKEN="your-api-token"
   export NETBOX_VERSION=4.6
   export MCP_HOST=0.0.0.0
   export MCP_PORT=8000
   ```

4. **Test your setup**
   ```bash
   python3 -m py_compile netbox_mcp/__main__.py netbox_mcp/tools/*.py
   python3 -m netbox_mcp
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
4. Run syntax check: `python3 -m py_compile netbox_mcp/tools/<app>.py`
5. Test your changes with a running NetBox instance
6. Commit with a clear message describing what was added

For detailed step-by-step instructions, see the "How to add a new resource (step-by-step)" section in [`.github/copilot-instructions.md`](.github/copilot-instructions.md).

## Code Style

- Follow Python conventions (PEP 8)
- Use type hints: `async def func(args: Dict[str, Any]) -> Dict[str, Any]` (every tool returns an envelope dict, not a bare list)
- Keep functions focused and single-purpose
- Include comprehensive docstrings for all tools

## Testing

Before submitting a PR:

1. Run syntax check: `python3 -m py_compile netbox_mcp/__main__.py netbox_mcp/tools/*.py`
2. Run the integration suite against `demo.netbox.dev`: `make test-demo`
3. Test with your NetBox instance to verify tools work correctly
4. Verify parameter mapping matches NetBox API expectations

## Questions or Issues?

If you have questions or encounter issues:
- Check the [`.github/copilot-instructions.md`](.github/copilot-instructions.md) for detailed guidance
- Review existing tools under `netbox_mcp/tools/` for examples
- Open an issue on GitHub for discussion

## License

By contributing to this project, you agree that your contributions will be licensed under the same license as the project.
