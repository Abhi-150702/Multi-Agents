from mcp_client.client import MCPClient
from mcp_client.langchain_adapters import get_langchain_tools


class MCPManager:
    def __init__(self):
        self.clients = {}
        self.tools = {}

    async def register_server(self, server_name: str, server_path: str):
        """
        Register and connect with the MCP Server.
        """
        client = MCPClient(server_path)
        await client.connect()

        self.clients[server_name] = client

        tools = await get_langchain_tools(client)

        self.tools[server_name] = tools

    async def get_tools(self, server_name: str):
        """
        Return Langchain tools exposed by an MCP server.
        """

        if server_name not in self.tools:
            raise ValueError(
                f"MCP server '{server_name}' is not registered"
            )

        return self.tools[server_name]


    async def disconnect(self):
        """
        Disconnect all the registered MCP servers.
        """

        for client in self.clients.values():
            await client.disconnect()

        self.clients.clear()
        self.tools.clear()