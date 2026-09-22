from langchain.agents import create_agent

from models.llm import get_research_llm

from agents.research.prompt import RESEARCH_AGENT_SYSTEM_PROMPT

from mcp_client.manager import MCPManager

from config.settings import Settings
from config.logging_config import setup_logger

logger = setup_logger("research_agent")


async def create_research_agent(
    config_settings: Settings = None,
    mcp_manager: MCPManager = None
) -> create_agent:

    logger.info("Initializing Research Agent...")

    if mcp_manager is not None:
        logger.info("Fetching tools from Research MCP Server...")

        mcp_tools = await mcp_manager.get_tools("research")

        logger.info(
            f"Discovered {len(mcp_tools)} "
            f"MCP tools for Research Agent."
        )

    else:
        logger.warning(
            "MCP Manager not provided. "
            "Research Agent has no tools."
        )
        mcp_tools = []
    logger.info(f"Registered {len(mcp_tools)} tools with Research Agent ")

    return create_agent(
        model=get_research_llm(config_settings),
        tools=mcp_tools,
        system_prompt=RESEARCH_AGENT_SYSTEM_PROMPT,
    )
