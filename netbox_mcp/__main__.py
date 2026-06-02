"""Entry point: `python -m netbox_mcp`.

Importing `.tools` triggers each submodule's @mcp.tool decorators,
populating the shared registry before the server starts.
"""

import asyncio
import os

from . import tools  # noqa: F401  -- side-effect import for tool registration
from .client import _close_shared_client
from .server import mcp


def _shutdown_shared_client() -> None:
    """Best-effort close of the shared httpx client on process exit."""
    try:
        asyncio.run(_close_shared_client())
    except Exception:
        # Shutdown is best-effort; never raise from the exit path.
        pass


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

    try:
        mcp.run(transport="http", host=host, port=port)
    except KeyboardInterrupt:
        # Ctrl+C / SIGINT: anyio's asyncio runner re-raises KeyboardInterrupt
        # after the event loop unwinds. Swallow it so we exit 0 with a clean
        # message instead of dumping a CancelledError/KeyboardInterrupt trace.
        print("netbox-mcp: received interrupt, shutting down")
    finally:
        _shutdown_shared_client()


if __name__ == "__main__":
    main()
