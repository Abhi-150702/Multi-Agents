# mcp_client/test_client.py

import asyncio

from mcp_client.client import MCPClient
from mcp_client.langchain_adapters import get_langchain_tools


async def main():

    client = MCPClient(
        "mcp_servers/research_server.py"
    )

    try:
        await client.connect()

        print("Connected to MCP server.")

        tools = await get_langchain_tools(client)

        print("\nLangChain tools:")

        for tool in tools:
            print(f"- {tool.name}")
            print(f"  Description: {tool.description}")
            print(f"  Schema: {tool.args_schema}")

        result = await tools[0].ainvoke(
            {
                "query": "latest developments in generative AI",
                "max_results": 5,
            }
        )

        print("\nTool Result:")
        print(result)

    finally:
        await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())