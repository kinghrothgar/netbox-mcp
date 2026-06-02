"""Shared NetBox HTTP client and credential configuration.

NetBox URL and API token are owned by this module but populated by the
entry point (:mod:`netbox_mcp.__main__`) via :func:`set_netbox_credentials`
after CLI args / environment variables have been resolved. Helpers
retrieve them per-call via :func:`get_netbox_credentials`, which raises
loudly if the entry point hasn't run. This avoids snapshotting env vars
at import time, which would make ``--netbox-url`` / ``--netbox-token``
ineffective.
"""

import asyncio
from typing import Any, Dict, Optional, Tuple
from urllib.parse import urljoin

import httpx


# NetBox credentials. Populated by :func:`set_netbox_credentials` from
# :mod:`netbox_mcp.__main__` before tool modules are imported.
_netbox_url: Optional[str] = None
_netbox_token: Optional[str] = None


def set_netbox_credentials(url: str, token: str) -> None:
    """Store the NetBox base URL and API token for use by helpers.

    Must be called before any tool runs. The entry point invokes this
    after argparse resolution (CLI flag > env var > default). ``token``
    may be the empty string for unauthenticated read access; ``url``
    must be a non-empty string.
    """
    global _netbox_url, _netbox_token
    if not isinstance(url, str) or not url:
        raise ValueError("NetBox URL must be a non-empty string")
    if not isinstance(token, str):
        raise ValueError("NetBox token must be a string (may be empty)")
    _netbox_url = url
    _netbox_token = token


def get_netbox_credentials() -> Tuple[str, str]:
    """Return ``(url, token)`` previously stored by :func:`set_netbox_credentials`.

    Raises :class:`RuntimeError` if credentials have not been set. The
    package's entry point is responsible for calling
    :func:`set_netbox_credentials`; importing tool modules without
    going through it (e.g. ``python -c "from netbox_mcp.tools import dcim"``)
    will fail here rather than silently using stale or missing env vars.
    """
    if _netbox_url is None or _netbox_token is None:
        raise RuntimeError(
            "NetBox credentials are not configured. Run the server via "
            "`python -m netbox_mcp` (which resolves --netbox-url / "
            "--netbox-token or the NETBOX_URL / NETBOX_TOKEN env vars), "
            "or call netbox_mcp.client.set_netbox_credentials(url, token) "
            "directly before invoking any tool."
        )
    return _netbox_url, _netbox_token


# Shared HTTP client to avoid creating multiple clients concurrently
# This prevents "unhandled errors in a TaskGroup" when multiple tools run simultaneously
_shared_http_client: Optional[httpx.AsyncClient] = None
_init_lock = None


async def _get_shared_client() -> httpx.AsyncClient:
    """Get or create the shared HTTP client (thread-safe).

    Uses asyncio.Lock for proper synchronization during concurrent initialization.
    This function must be called from an async context (which is guaranteed since
    it's an async function called by async tool functions).
    """
    global _shared_http_client, _init_lock

    # Fast path: if client already exists, return it
    if _shared_http_client is not None:
        return _shared_http_client

    # Ensure we have a lock (create it if needed in async context)
    if _init_lock is None:
        try:
            _init_lock = asyncio.Lock()
        except RuntimeError as e:
            # This should never happen since we're in an async context
            raise RuntimeError(
                "No event loop available. This function must be called from an async context."
            ) from e

    # Slow path: create client with lock to ensure only one instance
    async with _init_lock:
        # Double-check after acquiring lock (another coroutine might have created it)
        if _shared_http_client is None:
            _shared_http_client = httpx.AsyncClient(timeout=30.0)
        return _shared_http_client


async def _close_shared_client() -> None:
    """Close the shared HTTP client on application shutdown.

    Note: FastMCP doesn't provide shutdown hooks by default. If running this
    as a standalone service, you may want to register this function with your
    application framework's shutdown handler (e.g., atexit, signal handlers).
    For now, the client will be cleaned up when the Python process exits.
    """
    global _shared_http_client
    if _shared_http_client is not None:
        await _shared_http_client.aclose()
        _shared_http_client = None


class NetBoxClient:
    """Async NetBox API client"""

    def __init__(self, base_url: str, token: str):
        self.base_url = base_url.rstrip('/')
        self.token = token
        self.headers = {
            "Authorization": f"Token {token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    async def get(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Make GET request to NetBox API"""
        url = urljoin(f"{self.base_url}/api/", endpoint.lstrip('/'))

        # Use shared client to avoid concurrent client creation issues
        client = await _get_shared_client()
        try:
            response = await client.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            # Re-raise HTTP errors with more context
            raise Exception(f"NetBox API HTTP {e.response.status_code}: {e}") from e
        except httpx.RequestError as e:
            # Handle connection, timeout, and request errors
            raise Exception(f"NetBox API request error: {e}") from e
        except Exception as e:
            # Handle all other errors (JSON decode, etc.)
            raise Exception(f"NetBox API error: {e}") from e
