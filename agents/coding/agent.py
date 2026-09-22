from models.llm import get_coding_llm
from langchain.agents import create_agent
from agents.coding.prompt import CODING_AGENT_SYSTEM_PROMPT

from tools.coding.code_analysis import analyze_python_file
from tools.coding.filesystem import read_files, list_files

from mcp_client.manager import MCPManager

from config.settings import Settings

from config.logging_config import setup_logger

logger = setup_logger('coding_agent')

coding_tools = [
    analyze_python_file,
    read_files,
    list_files
]


async def create_coding_agent(config_settings: Settings = None, mcp_manager: MCPManager = None):
    logger.info('Intializing Coding Agent!')
    if mcp_manager is not None:
        logger.info("Fetching tools from Coding MCP Server...")

        mcp_tools = await mcp_manager.get_tools("coding")

        logger.info(
            f"Discovered {len(mcp_tools)} "
            f"MCP tools for Coding Agent."
        )

    else:
        logger.warning(
            "MCP Manager not provided. "
            "Coding Agent has no local tools."
        )
        mcp_tools = []

    logger.info(f'Registered {len(mcp_tools)} Tools with Coding Agent!')

    return create_agent(
        model=get_coding_llm(config_settings),
        tools=mcp_tools,
        system_prompt=CODING_AGENT_SYSTEM_PROMPT
    )