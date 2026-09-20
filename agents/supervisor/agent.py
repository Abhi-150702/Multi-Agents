from langchain.agents import create_agent
from models.llm import get_supervisor_llm
from agents.supervisor.prompt import SUPERVISOR_SYSTEM_PROMPT
from schemas.routing import RoutingDecision

from config.settings import Settings
from config.logging_config import setup_logger

logger = setup_logger('supervisor_agent')

def create_supervisor_agent(config_settings: Settings = None) -> create_agent:
    logger.info("Initializing Supervisor Agent!")

    return create_agent(
        model=get_supervisor_llm(config_settings),
        system_prompt=SUPERVISOR_SYSTEM_PROMPT,
        response_format=RoutingDecision
    )
