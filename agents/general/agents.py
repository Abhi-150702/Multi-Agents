from langchain.agents import create_agent
from models.llm import get_general_llm
from agents.general.prompt import GENERAL_AGENT_SYSTEM_PROMPT

from mcp_client.manager import MCPManager

from config.settings import Settings
from config.logging_config import setup_logger

logger = setup_logger('general_agent')

async def create_general_agent(config_settings: Settings = None, mcp_manager: MCPManager = None):
    logger.info("Initializing General Agent!")
    return create_agent(
        model=get_general_llm(config_settings),
        system_prompt=GENERAL_AGENT_SYSTEM_PROMPT,
    )