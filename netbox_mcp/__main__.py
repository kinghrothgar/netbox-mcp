"""Entry point: `python -m netbox_mcp`.

All runtime knobs are settable via either a CLI flag or an environment
variable. Precedence for every setting is **CLI flag > env var > built-in
default**, implemented uniformly by giving each argparse option a default
of ``os.getenv("NAME", builtin_default)``.

Tool registration happens as a side effect of importing
``netbox_mcp.tools``. That import is deferred until *after* the target
NetBox version is set, so version-gated decorators see the right value
at decoration time.
"""

import argparse
import asyncio
import os
import sys
from typing import List, Optional

from .client import _close_shared_client, set_netbox_credentials
from .server import mcp
from .version import (
    DEFAULT_NETBOX_VERSION,
    SUPPORTED_NETBOX_VERSIONS,
    parse_version,
    set_netbox_version,
)


_DEFAULT_NETBOX_URL = "https://netbox.example.com"
_DEFAULT_NETBOX_TOKEN = ""
_DEFAULT_MCP_HOST = "0.0.0.0"
_DEFAULT_MCP_PORT = "8000"


def _shutdown_shared_client() -> None:
    """Best-effort close of the shared httpx client on process exit."""
    try:
        asyncio.run(_close_shared_client())
    except Exception:
        # Shutdown is best-effort; never raise from the exit path.
        pass


def _build_parser() -> argparse.ArgumentParser:
    """Build the CLI argument parser.

    Every flag falls back to a matching environment variable when not
    supplied on the command line, and to a hard-coded default when
    neither is set. ``argparse``'s help text shows the resolved default
    at invocation time.
    """
    supported = ", ".join(f"{m}.{n}" for m, n in SUPPORTED_NETBOX_VERSIONS)
    default_version = f"{DEFAULT_NETBOX_VERSION[0]}.{DEFAULT_NETBOX_VERSION[1]}"

    parser = argparse.ArgumentParser(
        prog="python -m netbox_mcp",
        description=(
            "FastMCP server exposing read-only NetBox API tools. Every "
            "option below can also be supplied via an environment "
            "variable; CLI flags take precedence over env vars, which "
            "take precedence over built-in defaults."
        ),
    )
    parser.add_argument(
        "--netbox-version",
        dest="netbox_version",
        metavar="MAJOR.MINOR",
        default=os.getenv("NETBOX_VERSION", default_version),
        help=(
            f"Target NetBox minor version. Supported: {supported}. "
            f"Env: NETBOX_VERSION. Default: {default_version}."
        ),
    )
    parser.add_argument(
        "--netbox-url",
        dest="netbox_url",
        metavar="URL",
        default=os.getenv("NETBOX_URL", _DEFAULT_NETBOX_URL),
        help=(
            "Base URL of the NetBox instance. "
            f"Env: NETBOX_URL. Default: {_DEFAULT_NETBOX_URL}."
        ),
    )
    parser.add_argument(
        "--netbox-token",
        dest="netbox_token",
        metavar="TOKEN",
        default=os.getenv("NETBOX_TOKEN", _DEFAULT_NETBOX_TOKEN),
        help=(
            "NetBox API token with read permissions. "
            "Env: NETBOX_TOKEN. Default: empty. "
            "WARNING: passing a secret on the command line exposes it via "
            "`ps`, /proc/<pid>/cmdline, shell history, and container "
            "runtime metadata. Prefer NETBOX_TOKEN (e.g. via --env-file, "
            "a Kubernetes Secret, or systemd EnvironmentFile=) for "
            "anything beyond ad-hoc debugging."
        ),
    )
    parser.add_argument(
        "--mcp-host",
        dest="mcp_host",
        metavar="HOST",
        default=os.getenv("MCP_HOST", _DEFAULT_MCP_HOST),
        help=(
            "Address the FastMCP HTTP transport binds to. "
            f"Env: MCP_HOST. Default: {_DEFAULT_MCP_HOST}."
        ),
    )
    parser.add_argument(
        "--mcp-port",
        dest="mcp_port",
        metavar="PORT",
        # Kept as a string so the validation error path is identical for
        # both `--mcp-port abc` and `MCP_PORT=abc`.
        default=os.getenv("MCP_PORT", _DEFAULT_MCP_PORT),
        help=(
            "Port for the FastMCP HTTP transport. Must be an integer. "
            f"Env: MCP_PORT. Default: {_DEFAULT_MCP_PORT}."
        ),
    )
    return parser


def _parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = _build_parser()
    return parser.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> None:
    args = _parse_args(argv)

    try:
        port = int(args.mcp_port)
    except (TypeError, ValueError):
        raise SystemExit(
            f"Invalid MCP_PORT value: {args.mcp_port} - must be an integer"
        )

    try:
        version = parse_version(args.netbox_version)
        set_netbox_version(version)
    except ValueError as exc:
        raise SystemExit(f"netbox-mcp: {exc}")

    try:
        set_netbox_credentials(args.netbox_url, args.netbox_token)
    except ValueError as exc:
        raise SystemExit(f"netbox-mcp: {exc}")

    # Tool registration is a side effect of importing the tools package.
    # Do this *after* the target version has been set so version-gated
    # tools see the correct value at decoration time.
    from . import tools  # noqa: F401

    print(
        f"netbox-mcp: targeting NetBox {version[0]}.{version[1]}",
        file=sys.stderr,
    )

    try:
        mcp.run(transport="http", host=args.mcp_host, port=port)
    except KeyboardInterrupt:
        # Ctrl+C / SIGINT: anyio's asyncio runner re-raises KeyboardInterrupt
        # after the event loop unwinds. Swallow it so we exit 0 with a clean
        # message instead of dumping a CancelledError/KeyboardInterrupt trace.
        print("netbox-mcp: received interrupt, shutting down")
    finally:
        _shutdown_shared_client()


if __name__ == "__main__":
    main()
