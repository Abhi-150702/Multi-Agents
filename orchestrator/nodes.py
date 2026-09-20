from typing import Literal

from agents.supervisor.agent import create_supervisor_agent
from agents.general.agents import create_general_agent
from agents.research.agent import create_research_agent
from agents.coding.agent import create_coding_agent

from schemas.state import AgentState
from config.logging_config import setup_logger

logger = setup_logger('nodes')

# Cache agents to avoid reinitialization on every query
_supervisor_agent = None
_general_agent = None
_research_agent = None
_coding_agent = None


def initialize_agents():
    """
    Initialize all agents at application startup.
    This ensures agents are ready before the first query hits.
    """
    global _supervisor_agent, _general_agent, _research_agent, _coding_agent

    logger.info("=" * 60)
    logger.info("Initializing all agents at application startup...")
    logger.info("=" * 60)

    # Initialize supervisor agent
    logger.info("[1/4] Initializing Supervisor Agent...")
    _supervisor_agent = create_supervisor_agent()
    logger.info("[1/4] Supervisor Agent initialized successfully!")

    # Initialize general agent
    logger.info("[2/4] Initializing General Agent...")
    _general_agent = create_general_agent()
    logger.info("[2/4] General Agent initialized successfully!")

    # Initialize research agent
    logger.info("[3/4] Initializing Research Agent...")
    _research_agent = create_research_agent()
    logger.info("[3/4] Research Agent initialized successfully!")

    # Initialize coding agent
    logger.info("[4/4] Initializing Coding Agent...")
    _coding_agent = create_coding_agent()
    logger.info("[4/4] Coding Agent initialized successfully!")


def get_agents_status():
    """
    Check if all agents are initialized.
    Returns a dictionary with initialization status of each agent.
    """
    return {
        'supervisor_initialized': _supervisor_agent is not None,
        "general_initialized" : _general_agent is not None,
        'research_initialized': _research_agent is not None,
        'coding_initialized': _coding_agent is not None,
        'all_initialized': all([
            _supervisor_agent is not None,
            _general_agent is not None,
            _research_agent is not None,
            _coding_agent is not None
        ])
    }


def supervisor_node(state: AgentState) -> AgentState:
    global _supervisor_agent

    # Fallback: Initialize agent if not already initialized
    # This should not happen if initialize_agents() is called at startup
    if _supervisor_agent is None:
        logger.warning("Supervisor agent not initialized at startup. Initializing now...")
        _supervisor_agent = create_supervisor_agent()

    supervisor_agent = _supervisor_agent

    response = supervisor_agent.invoke(
        {
            "messages" : [
                {
                    "role" : 'user',
                    'content' : state.user_query
                }
            ]
        }
    )

    decision = response['structured_response']

    state.supervisor_route = decision.route
    state.supervisor_route_rationale = decision.rationale

    return state


def general_node(state: AgentState) -> AgentState:
    global _general_agent

    # Fallback: Initialize agent if not already initialized
    # This should not happen if initialize_agents() is called at startup
    if _general_agent is None:
        logger.warning("General agent not initialized at startup. Initializing now...")
        _general_agent = create_general_agent()

    general_agent = _general_agent

    response = general_agent.invoke(
        {
            "messages" : [
                {
                    "role" : 'user',
                    "content" : state.user_query
                }
            ]
        }
    )

    state.general_result = response["messages"][-1].content

    return state


def research_node(state: AgentState) -> AgentState:
    global _research_agent

    # Fallback: Initialize agent if not already initialized
    # This should not happen if initialize_agents() is called at startup
    if _research_agent is None:
        logger.warning("Research agent not initialized at startup. Initializing now...")
        _research_agent = create_research_agent()

    research_agent = _research_agent

    response = research_agent.invoke(
        {
            "messages" : [
                {
                    "role" : 'user',
                    'content' : state.user_query
                }
            ]
        }
    )

    state.research_result = response['messages'][-1].content

    return state


def coding_node(state: AgentState) -> AgentState:
    global _coding_agent

    # Fallback: Initialize agent if not already initialized
    # This should not happen if initialize_agents() is called at startup
    if _coding_agent is None:
        logger.warning("Coding agent not initialized at startup. Initializing now...")
        _coding_agent = create_coding_agent()

    coding_agent = _coding_agent

    if state.research_result:
        prompt = f"""
User request:

{state.user_query}


Research performed by the Research Agent:

{state.research_result}


Using the research above, complete the user's coding request.

Do not blindly trust the research.
Use your own reasoning and produce the appropriate implementation.
"""

    else:
        prompt = state.user_query

    response = coding_agent.invoke(
        {
            'messages' : [
                {
                    'role' : 'user',
                    'content' : prompt
                }
            ]
        }
    )

    state.coding_result = response['messages'][-1].content

    return state
