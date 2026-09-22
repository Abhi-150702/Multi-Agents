from pathlib import Path
from fastmcp.client import Client


class MCPClient:
    def __init__(self, server_path: str):
        self.server_path = Path(server_path)
        self.mcp_client = Client(self.server_path)

    async def connect(self):
        await self.mcp_client.__aenter__()

    async def disconnect(self):
        await self.mcp_client.__aexit__(None, None, None)

    async def list_tools(self):
        return await self.mcp_client.list_tools()

    async def call_tool(self, tool_name, arguments):
        return await self.mcp_client.call_tool(
            tool_name,
            arguments
        )