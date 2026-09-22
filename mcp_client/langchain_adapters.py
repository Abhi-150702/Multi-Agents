from typing import Any, List

from langchain_core.tools import StructuredTool
from pydantic import Field, create_model

from mcp_client.client import MCPClient

from config.logging_config import setup_logger

logger = setup_logger("MCP tool for LangChain")

def json_schema_to_pydantic_model(tool_name: str, schema: dict) -> create_model:
    properties = schema.get('properties', {})
    required = schema.get('required', [])

    fields = {}

    type_mapping = {
        "string" : str,
        "integer" : int,
        "number" : float,
        "boolean" : bool
    }

    for name, definition in properties.items():
        python_type = type_mapping.get(definition.get('type'), Any)

        if name in required:
            default = ...
        else:
            default = definition.get('default', None)

        description = definition.get("description", "")

        fields[name] = (
            python_type, 
            Field(
                default=default,
                description=description
            )
        )

    return create_model(
        f"{tool_name}Input",
        **fields
    )


def create_langchain_tool(mcp_client: MCPClient, mcp_tool) -> StructuredTool:
    args_schema = json_schema_to_pydantic_model(mcp_tool.name, mcp_tool.input_schema)

    async def invoke_mcp_tool(**kwargs):
        logger.info(
            f"[MCP TOOL CALL] {mcp_tool.name} | "
            f"Arguments: {kwargs}"
        )

        result = await mcp_client.call_tool(
            mcp_tool.name,
            kwargs,
        )

        logger.info(
            f"[MCP TOOL RESULT] {mcp_tool.name}"
        )

        if result.data is not None:
            return result.data

        return str(result)

    return StructuredTool.from_function(
        coroutine=invoke_mcp_tool,
        name=mcp_tool.name,
        description=mcp_tool.description or "",
        args_schema=args_schema
    )


async def get_langchain_tools(mcp_client : MCPClient) -> List[StructuredTool]:
    mcp_tools = await mcp_client.list_tools()

    return [
        create_langchain_tool(mcp_client, mcp_tool) for mcp_tool in mcp_tools
    ]