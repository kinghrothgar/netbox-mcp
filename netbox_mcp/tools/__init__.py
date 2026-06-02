"""Tool submodules.

Importing this package imports every per-app submodule for its side
effect (registering tools on the shared `mcp` instance from
`netbox_mcp.server`). Add a new NetBox app by creating a new submodule
and importing it here.
"""

from . import circuits, dcim, ipam, tenancy, virtualization  # noqa: F401
