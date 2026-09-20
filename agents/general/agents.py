from langchain.agents import create_agent
from models.llm import get_general_llm
from agents.general.prompt import GENERAL_AGENT_SYSTEM_PROMPT
from config.logging_config import setup_logger

logger = setup_logger('general_agent')

def create_general_agent():
    logger.info("Initializing General Agent!")
    return create_agent(
        model=get_general_llm(),
        system_prompt=GENERAL_AGENT_SYSTEM_PROMPT,
    )