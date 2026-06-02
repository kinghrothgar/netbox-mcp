"""Entry point: `python -m netbox_mcp`.

Importing `.tools` triggers each submodule's @mcp.tool decorators,
populating the shared registry before the server starts.
"""

import os

from . import tools  # noqa: F401  -- side-effect import for tool registration
from .server import mcp


def main() -> None:
    host = os.getenv("MCP_HOST", "0.0.0.0")

    port_env = os.getenv("MCP_PORT")
    if port_env is None:
        port = 8000
    else:
        try:
            port = int(port_env)
        except ValueError:
            raise SystemExit(f"Invalid MCP_PORT value: {port_env} - must be an integer")

    mcp.run(transport="http", host=host, port=port)


if __name__ == "__main__":
    main()
