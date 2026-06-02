"""FastMCP server singleton.

Importing this module gives access to the shared `mcp` registry. All tool
modules under `netbox_mcp.tools` decorate functions on this instance.
"""

from fastmcp import FastMCP

mcp = FastMCP("NetBox Streaming MCP Server")
