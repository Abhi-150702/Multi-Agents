from langchain.agents import create_agent
from models.llm import get_supervisor_agent
from agents.supervisor.prompt import SUPERVISOR_SYSTEM_PROMPT
from schemas.routing import RoutingDecision

from config.logging_config import setup_logger
logger = setup_logger('supervisor_agent')

def create_supervisor_agent() -> create_agent:
    logger.info("Initializing Supervisor Agent!")
    return create_agent(
        model=get_supervisor_agent(),
        system_prompt=SUPERVISOR_SYSTEM_PROMPT,
        response_format=RoutingDecision
    )
