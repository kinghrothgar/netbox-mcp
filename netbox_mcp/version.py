"""NetBox target version selection and feature gating.

Tools are registered at import time via ``@mcp.tool`` decorators on the
shared registry from :mod:`netbox_mcp.server`. Some tools correspond to
NetBox API endpoints that only exist (or only accept certain filters) on
a particular NetBox minor release. To support multiple NetBox versions
from a single image, the entry point (:mod:`netbox_mcp.__main__`) sets
the target version *before* the tool modules are imported. Tool modules
then use :func:`version_gated_tool` to register version-specific tools
only when the target version is high enough.

Currently supported target versions: ``4.5`` and ``4.6``. The default is
the newest supported version (``4.6``). To run against an older NetBox,
pass ``--netbox-version 4.5`` or set ``NETBOX_VERSION=4.5``.
"""

from typing import Any, Callable, Tuple

# Default to the newest supported NetBox minor release. The entry point
# overrides this via :func:`set_netbox_version` after parsing CLI args /
# environment variables, before the tool submodules are imported.
DEFAULT_NETBOX_VERSION: Tuple[int, int] = (4, 6)

# Versions this package knows how to target. Used to validate user input.
SUPPORTED_NETBOX_VERSIONS: Tuple[Tuple[int, int], ...] = (
    (4, 5),
    (4, 6),
)

# Mutable module-level target version. Tool modules read this (via
# :func:`is_at_least` / :func:`version_gated_tool`) at import time, so
# this MUST be set before importing ``netbox_mcp.tools``.
_target_version: Tuple[int, int] = DEFAULT_NETBOX_VERSION


def parse_version(value: str) -> Tuple[int, int]:
    """Parse a ``"<major>.<minor>"`` string into a ``(major, minor)`` tuple.

    Raises :class:`ValueError` on malformed input. Patch components (e.g.
    ``"4.6.1"``) are accepted but only the major/minor are used.
    """
    parts = str(value).strip().split(".")
    if len(parts) < 2:
        raise ValueError(
            f"NetBox version must be in the form '<major>.<minor>', got {value!r}"
        )
    try:
        major = int(parts[0])
        minor = int(parts[1])
    except ValueError as exc:
        raise ValueError(
            f"NetBox version components must be integers, got {value!r}"
        ) from exc
    return (major, minor)


def set_netbox_version(version: Tuple[int, int]) -> None:
    """Set the target NetBox version.

    Must be called before any module under :mod:`netbox_mcp.tools` is
    imported, otherwise version-gated tools will use the wrong target.
    """
    global _target_version
    if version not in SUPPORTED_NETBOX_VERSIONS:
        supported = ", ".join(f"{m}.{n}" for m, n in SUPPORTED_NETBOX_VERSIONS)
        raise ValueError(
            f"Unsupported NetBox version {version[0]}.{version[1]}; "
            f"supported versions: {supported}"
        )
    _target_version = version


def get_netbox_version() -> Tuple[int, int]:
    """Return the currently selected target NetBox version."""
    return _target_version


def is_at_least(major: int, minor: int) -> bool:
    """Return ``True`` if the target NetBox version is >= ``major.minor``."""
    return _target_version >= (major, minor)


def version_gated_tool(
    mcp: Any,
    min_version: Tuple[int, int],
    **tool_kwargs: Any,
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Return a decorator that registers a tool only on supported versions.

    Usage::

        @version_gated_tool(mcp, min_version=(4, 6),
                            annotations={"title": "...", "readOnlyHint": True,
                                         "openWorldHint": True})
        async def search_rack_groups(args): ...

    When the target NetBox version is at least ``min_version`` this is
    equivalent to ``@mcp.tool(**tool_kwargs)``. When it is older, the
    decorator returns the undecorated function so it is never registered
    on the shared MCP registry; clients of the older NetBox simply won't
    see the tool.
    """
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        if is_at_least(*min_version):
            return mcp.tool(**tool_kwargs)(func)
        return func
    return decorator
