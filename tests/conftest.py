"""Pytest fixtures for netbox-mcp integration tests against demo.netbox.dev.

The fixtures are intentionally session-scoped so we do one credential
bootstrap and one container spin-up per ``pytest`` invocation.

The ``netbox_mcp_url`` fixture picks the target NetBox version from
whatever the demo NetBox reports via ``/api/status/``, clamped to the
highest version this package supports. So a single ``make test-demo``
exercises the version the demo is currently running, no parametrisation
needed.
"""

from __future__ import annotations

import os
import socket
import subprocess
import time
from typing import Any, Dict, Iterator, Tuple

import httpx
import pytest
import pytest_asyncio
from fastmcp import Client

from tests.bootstrap import (
    DEMO_STATUS_URL,
    DemoBootstrapError,
    _auth_header,
    load_or_create_credentials,
)


# Image tag the prod Dockerfile is built under (see Makefile).
NETBOX_MCP_IMAGE = os.getenv("NETBOX_MCP_IMAGE", "netbox-mcp:dev")

# Versions of NetBox this package can target. Mirrors
# netbox_mcp.version.SUPPORTED_NETBOX_VERSIONS but duplicated here so
# the test harness doesn't import production modules - the production
# code may refuse to import without credentials configured.
_SUPPORTED_VERSIONS: Tuple[Tuple[int, int], ...] = ((4, 5), (4, 6))


@pytest.fixture(scope="session")
def creds() -> Dict[str, Any]:
    """Bootstrapped (or cached) demo NetBox credentials."""
    try:
        return load_or_create_credentials()
    except DemoBootstrapError as exc:
        raise pytest.UsageError(str(exc))


@pytest.fixture(scope="session")
def demo_netbox_version(creds: Dict[str, Any]) -> Tuple[int, int]:
    """Probe the demo's reported NetBox version once per session.

    Returns ``(major, minor)``. Used by ``netbox_mcp_url`` to pick a
    matching target version and by version-gating tests to decide
    which gated tools should function.
    """
    try:
        resp = httpx.get(
            DEMO_STATUS_URL,
            headers=_auth_header(creds["token"]),
            timeout=15,
            follow_redirects=True,
        )
    except httpx.RequestError as exc:
        raise pytest.UsageError(
            f"Cannot reach demo NetBox /api/status/: {exc}"
        )
    if resp.status_code != 200:
        raise pytest.UsageError(
            f"demo NetBox /api/status/ returned HTTP {resp.status_code}: "
            f"{resp.text[:200]}"
        )
    raw = resp.json().get("netbox-version", "")
    parts = raw.split(".")
    if len(parts) < 2:
        raise pytest.UsageError(
            f"Cannot parse netbox-version from /api/status/: {raw!r}"
        )
    try:
        return (int(parts[0]), int(parts[1]))
    except ValueError:
        raise pytest.UsageError(
            f"Non-integer netbox-version components: {raw!r}"
        )


@pytest.fixture(scope="session")
def target_version(
    demo_netbox_version: Tuple[int, int],
) -> Tuple[int, int]:
    """Highest supported netbox-mcp target <= demo's reported version.

    If the demo runs a version newer than anything we support (e.g. 4.7
    while we still only know 4.5 / 4.6), we clamp down to our highest
    supported version. If the demo runs *older* than our oldest, we
    refuse to test.
    """
    chosen = None
    for v in _SUPPORTED_VERSIONS:
        if v <= demo_netbox_version and (chosen is None or v > chosen):
            chosen = v
    if chosen is None:
        raise pytest.UsageError(
            f"demo NetBox is {demo_netbox_version[0]}.{demo_netbox_version[1]}, "
            f"older than this package's oldest supported target "
            f"({_SUPPORTED_VERSIONS[0][0]}.{_SUPPORTED_VERSIONS[0][1]})."
        )
    return chosen


def _free_port() -> int:
    """Reserve an ephemeral TCP port on 127.0.0.1.

    There's a small race between releasing the socket and ``docker
    run`` binding it, but it's good enough for local-dev test runs.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]
    finally:
        s.close()


def _wait_for_port(host: str, port: int, timeout: float = 15.0) -> None:
    """Poll TCP connect until the port accepts or timeout."""
    deadline = time.monotonic() + timeout
    last_exc: Exception | None = None
    while time.monotonic() < deadline:
        try:
            with socket.create_connection((host, port), timeout=1.0):
                return
        except OSError as exc:
            last_exc = exc
            time.sleep(0.3)
    raise pytest.UsageError(
        f"netbox-mcp container at {host}:{port} did not accept TCP "
        f"connections within {timeout}s: {last_exc}"
    )


@pytest.fixture(scope="session")
def netbox_mcp_url(
    creds: Dict[str, Any],
    target_version: Tuple[int, int],
) -> Iterator[str]:
    """Spin up a netbox-mcp container pointed at the demo NetBox.

    Yields the FastMCP HTTP transport URL. Tears down the container on
    session exit.
    """
    port = _free_port()
    container = f"netbox-mcp-test-{os.getpid()}-{port}"
    version_str = f"{target_version[0]}.{target_version[1]}"
    env_args = [
        "-e", f"NETBOX_URL={creds['demo_url']}",
        "-e", f"NETBOX_TOKEN={creds['token']}",
        "-e", f"NETBOX_VERSION={version_str}",
        "-e", "MCP_HOST=127.0.0.1",
        "-e", f"MCP_PORT={port}",
    ]
    cmd = [
        "docker", "run",
        "-d", "--rm",
        "--name", container,
        "--network", "host",
        "--stop-timeout", "2",
        *env_args,
        NETBOX_MCP_IMAGE,
    ]
    result = subprocess.run(
        cmd, capture_output=True, text=True, check=False,
    )
    if result.returncode != 0:
        raise pytest.UsageError(
            f"Failed to start netbox-mcp container: {result.stderr.strip()}"
        )
    try:
        _wait_for_port("127.0.0.1", port)
        yield f"http://127.0.0.1:{port}/mcp/"
    finally:
        subprocess.run(
            ["docker", "stop", container],
            capture_output=True, text=True, check=False,
        )


@pytest_asyncio.fixture
async def mcp_client(netbox_mcp_url: str) -> Client:
    """Connected FastMCP client, function-scoped.

    Each test gets a fresh client on a fresh asyncio event loop. The
    netbox_mcp_url fixture is session-scoped so the underlying
    container is reused across the run.
    """
    async with Client(netbox_mcp_url) as c:
        yield c



