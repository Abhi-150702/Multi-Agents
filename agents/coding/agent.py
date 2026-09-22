from models.llm import get_coding_llm
from langchain.agents import create_agent
from agents.coding.prompt import CODING_AGENT_SYSTEM_PROMPT

from tools.coding.code_analysis import analyze_python_file
from tools.coding.filesystem import (
    read_files, 
    list_files, 
    write_file, 
    create_file, 
    append_to_file
)

from mcp_client.manager import MCPManager

from config.settings import Settings

from config.logging_config import setup_logger

logger = setup_logger('coding_agent')




async def create_coding_agent(config_settings: Settings = None, mcp_manager: MCPManager = None):
    logger.info('Intializing Coding Agent!')

    coding_tools = [
        # File reading
        read_files,
        list_files,

        # File writing
        write_file,
        create_file,
        append_to_file,

        # Code analysis
        analyze_python_file,
    ]

    logger.info(f'Total tools registered with Coding Agent: {len(coding_tools)}')

    return create_agent(
        model=get_coding_llm(config_settings),
        tools=coding_tools,
        system_prompt=CODING_AGENT_SYSTEM_PROMPT
    )