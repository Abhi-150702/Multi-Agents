import asyncio

from mcp_client.manager import MCPManager


async def main():

    manager = MCPManager()

    await manager.register_server(
        "research",
        "mcp_servers/research_server.py"
    )

    tools = await manager.get_tools("research")

    print("\nAVAILABLE TOOLS:")

    for tool in tools:
        print(f"- {tool.name}")

    print("\nTESTING TOOL:\n")

    result = await tools[0].ainvoke({
        "query": "latest developments in generative AI",
        "max_results": 3,
    })

    print(result)

    await manager.disconnect()


if __name__ == "__main__":
    asyncio.run(main())