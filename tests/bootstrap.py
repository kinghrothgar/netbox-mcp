"""Demo NetBox credential lifecycle for integration tests.

`demo.netbox.dev` runs the official upstream NetBox demo plugin which
lets anyone provision a self-service personal account at
``/plugins/demo/login/``. We sign up there, mint a read-only API token
via ``/api/users/tokens/provision/``, and cache the result so successive
test runs reuse the same credentials.

The cache file is written 0o600 and is gitignored. The demo NetBox is
wiped nightly at 04:00 UTC; when that happens our cached user no longer
exists, so we bootstrap a fresh one. The check is "does the cached
token still authenticate?" - cheap to do every test run.

This module is intentionally dependency-light: it only uses ``httpx``
(already a transitive dep of ``fastmcp``) and the stdlib. No HTML
parser; the demo login form has a single hidden ``csrfmiddlewaretoken``
input we extract with a regex.
"""

from __future__ import annotations

import json
import os
import re
import secrets
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional

import httpx


DEMO_URL = "https://demo.netbox.dev"
DEMO_LOGIN_URL = f"{DEMO_URL}/plugins/demo/login/"
DEMO_PROVISION_URL = f"{DEMO_URL}/api/users/tokens/provision/"
DEMO_STATUS_URL = f"{DEMO_URL}/api/status/"

# Repo-root cache file. The pytest entrypoint runs with the repo
# bind-mounted at /work, so this path resolves to the same file on the
# host and in the container.
CREDENTIALS_FILE = Path(".netbox-demo-creds.json")

# Extracted from the demo login page HTML.
_CSRF_INPUT_RE = re.compile(
    r'name="csrfmiddlewaretoken" value="([^"]+)"'
)

# How long to wait on any single demo HTTP request. The demo is public
# and sometimes slow; 15s gives it enough headroom without hanging the
# test session on a real outage.
_HTTP_TIMEOUT = 15.0


class DemoBootstrapError(RuntimeError):
    """Raised when we can't get a working token from the demo NetBox.

    The pytest session fixture converts this into ``pytest.UsageError``
    so the whole run aborts cleanly with a single readable message
    instead of every test failing individually.
    """


def load_or_create_credentials() -> Dict[str, Any]:
    """Return cached credentials if the token still works, else bootstrap fresh.

    Side effect: writes to :data:`CREDENTIALS_FILE` (0o600) when fresh
    credentials are minted.
    """
    cached = _load_cached()
    if cached and _token_works(cached.get("token", "")):
        return cached

    creds = _bootstrap_new_user_and_token()
    _save(creds)
    return creds


def _load_cached() -> Optional[Dict[str, Any]]:
    """Read and parse the cache file if it exists and is valid JSON."""
    if not CREDENTIALS_FILE.exists():
        return None
    try:
        return json.loads(CREDENTIALS_FILE.read_text())
    except (OSError, json.JSONDecodeError):
        return None


def _save(creds: Dict[str, Any]) -> None:
    """Persist credentials to :data:`CREDENTIALS_FILE` with mode 0o600."""
    payload = json.dumps(creds, indent=2, sort_keys=True) + "\n"
    # Write then chmod, to avoid a window where the file exists with
    # the default umask permissions.
    CREDENTIALS_FILE.write_text(payload)
    os.chmod(CREDENTIALS_FILE, 0o600)


def _token_works(token: str) -> bool:
    """GET /api/status/ to confirm the token authenticates.

    Returns ``True`` only on 200. Anything else - 401, 403, network
    error - is treated as "cached creds are stale, re-bootstrap".
    """
    if not token:
        return False
    headers = _auth_header(token)
    try:
        resp = httpx.get(
            DEMO_STATUS_URL,
            headers=headers,
            timeout=_HTTP_TIMEOUT,
            follow_redirects=True,
        )
    except httpx.RequestError:
        return False
    return resp.status_code == 200


def _auth_header(token: str) -> Dict[str, str]:
    """Build the ``Authorization`` header for either token format.

    Matches the logic in :mod:`netbox_mcp.client` so this module stays
    self-contained and we can validate the token before handing it to
    the server under test.
    """
    if token.startswith("nbt_"):
        return {"Authorization": f"Bearer {token}"}
    return {"Authorization": f"Token {token}"}


def _bootstrap_new_user_and_token() -> Dict[str, Any]:
    """Create a fresh demo user and mint a read-only API token.

    Two HTTP round trips against the demo plugin's signup form plus one
    against the NetBox token-provision API endpoint.
    """
    username = "mcp-test-" + secrets.token_hex(4)
    password = secrets.token_urlsafe(18)

    with httpx.Client(
        timeout=_HTTP_TIMEOUT, follow_redirects=True
    ) as session:
        csrf = _fetch_csrf_token(session)
        _signup(session, csrf, username, password)
        token = _provision_token(username, password)

    return {
        "demo_url": DEMO_URL,
        "username": username,
        "password": password,
        "token": token,
        "token_write_enabled": False,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }


def _fetch_csrf_token(session: httpx.Client) -> str:
    """GET the demo signup page and extract the hidden CSRF token."""
    try:
        resp = session.get(DEMO_LOGIN_URL)
    except httpx.RequestError as exc:
        raise DemoBootstrapError(
            f"Cannot reach demo NetBox at {DEMO_LOGIN_URL}: {exc}"
        ) from exc
    if resp.status_code != 200:
        raise DemoBootstrapError(
            f"Demo login page returned HTTP {resp.status_code}: "
            f"{resp.text[:200]}"
        )
    match = _CSRF_INPUT_RE.search(resp.text)
    if not match:
        raise DemoBootstrapError(
            "Could not find csrfmiddlewaretoken in demo login page; "
            "the demo plugin's form may have changed."
        )
    return match.group(1)


def _signup(
    session: httpx.Client, csrf: str, username: str, password: str
) -> None:
    """POST the demo signup form. Django requires a matching Referer."""
    try:
        resp = session.post(
            DEMO_LOGIN_URL,
            data={
                "csrfmiddlewaretoken": csrf,
                "username": username,
                "password": password,
            },
            headers={"Referer": DEMO_LOGIN_URL},
        )
    except httpx.RequestError as exc:
        raise DemoBootstrapError(f"Demo signup POST failed: {exc}") from exc
    # The demo plugin signs the user in and redirects to "/" on success.
    # With follow_redirects=True we end up on the homepage with a 200.
    if resp.status_code != 200:
        raise DemoBootstrapError(
            f"Demo signup returned HTTP {resp.status_code}: "
            f"{resp.text[:200]}"
        )


def _provision_token(username: str, password: str) -> str:
    """Mint a read-only API token via ``/api/users/tokens/provision/``.

    NetBox returns ``key`` and ``token`` separately; we assemble the
    full v2 auth value (``nbt_<key>.<token>``) so it drops directly
    into ``NETBOX_TOKEN`` without further glue.
    """
    body = {
        "username": username,
        "password": password,
        "description": "netbox-mcp integration tests (auto-provisioned)",
        "write_enabled": False,
    }
    try:
        resp = httpx.post(
            DEMO_PROVISION_URL,
            json=body,
            timeout=_HTTP_TIMEOUT,
            follow_redirects=True,
        )
    except httpx.RequestError as exc:
        raise DemoBootstrapError(
            f"Token provision request failed: {exc}"
        ) from exc
    if resp.status_code != 201:
        raise DemoBootstrapError(
            f"Token provision returned HTTP {resp.status_code}: "
            f"{resp.text[:300]}"
        )
    try:
        data = resp.json()
        key = data["key"]
        plaintext = data["token"]
    except (json.JSONDecodeError, KeyError) as exc:
        raise DemoBootstrapError(
            f"Token provision response missing expected fields: {resp.text[:300]}"
        ) from exc
    # v2 token wire format: nbt_<key>.<plaintext>. See netbox_mcp.client.
    return f"nbt_{key}.{plaintext}"
