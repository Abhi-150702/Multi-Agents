from models.llm import get_coding_llm
from langchain.agents import create_agent
from agents.coding.prompt import CODING_AGENT_SYSTEM_PROMPT

from tools.coding.code_analysis import analyze_python_file
from tools.coding.filesystem import read_files, list_files

from config.settings import Settings

from config.logging_config import setup_logger

logger = setup_logger('coding_agent')

coding_tools = [
    analyze_python_file,
    read_files,
    list_files
]


def create_coding_agent(config_settings: Settings = None):
    logger.info('Intializing Coding Agent!')
    logger.info(f'Registered {len(coding_tools)} Tools with Coding Agent!')
    return create_agent(
        model=get_coding_llm(config_settings),
        tools=coding_tools,
        system_prompt=CODING_AGENT_SYSTEM_PROMPT
    )