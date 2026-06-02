"""Shared NetBox HTTP client and environment configuration."""

import asyncio
import os
from typing import Any, Dict, Optional
from urllib.parse import urljoin

import httpx


# Configuration for NetBox API client

NETBOX_URL = os.getenv("NETBOX_URL", "https://netbox.example.com")
NETBOX_TOKEN = os.getenv("NETBOX_TOKEN", "")

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
