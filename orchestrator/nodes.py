import asyncio

from agents.supervisor.agent import create_supervisor_agent
from agents.general.agents import create_general_agent
from agents.research.agent import create_research_agent
from agents.coding.agent import create_coding_agent

from schemas.state import AgentState

from config.settings import Settings
from config.logging_config import setup_logger

logger = setup_logger("nodes")


# ============================================================
# Agent Cache
# ============================================================

_supervisor_agent = None
_general_agent = None
_research_agent = None
_coding_agent = None


# ============================================================
# Initialize All Agents
# ============================================================

async def initialize_agents(
    config_settings: Settings = None,
    mcp_manager=None
):
    """
    Initialize all agents at application startup.

    MCP-backed tools are discovered through the MCP Manager
    and passed to the Research Agent during initialization.
    """

    global _supervisor_agent, _general_agent, _research_agent, _coding_agent

    logger.info("=" * 60)
    logger.info("Initializing all agents at application startup...")
    logger.info("=" * 60)

    # --------------------------------------------------------
    # 1. Supervisor Agent
    # --------------------------------------------------------

    logger.info("[1/4] Initializing Supervisor Agent...")

    _supervisor_agent = await create_supervisor_agent(config_settings=config_settings, mcp_manager=mcp_manager)

    logger.info(
        "[1/4] Supervisor Agent initialized successfully!"
    )

    # --------------------------------------------------------
    # 2. General Agent
    # --------------------------------------------------------

    logger.info("[2/4] Initializing General Agent...")

    _general_agent = await create_general_agent(config_settings=config_settings, mcp_manager=mcp_manager)

    logger.info("[2/4] General Agent initialized successfully!")

    # --------------------------------------------------------
    # 3. Research Agent
    # --------------------------------------------------------

    logger.info("[3/4] Initializing Research Agent...")

    _research_agent = await create_research_agent(config_settings=config_settings, mcp_manager=mcp_manager)

    logger.info("[3/4] Research Agent initialized successfully!")

    # --------------------------------------------------------
    # 4. Coding Agent
    # --------------------------------------------------------

    logger.info("[4/4] Initializing Coding Agent...")

    _coding_agent = await create_coding_agent(config_settings=config_settings, mcp_manager=mcp_manager)

    logger.info("[4/4] Coding Agent initialized successfully!")
    logger.info("=" * 60)
    logger.info("All agents initialized successfully!")
    logger.info("=" * 60)


# ============================================================
# Agent Status
# ============================================================

def get_agents_status():
    """
    Check whether all agents are initialized.
    """
    return {
        "supervisor_initialized": _supervisor_agent is not None,
        "general_initialized": _general_agent is not None,
        "research_initialized": _research_agent is not None,
        "coding_initialized": _coding_agent is not None,
        "all_initialized": all([
            _supervisor_agent is not None,
            _general_agent is not None,
            _research_agent is not None,
            _coding_agent is not None
        ])
    }


# ============================================================
# Supervisor Node
# ============================================================

async def supervisor_node(
    state: AgentState,
    config_settings: Settings = None
) -> AgentState:

    global _supervisor_agent

    # Fallback initialization
    if _supervisor_agent is None:

        logger.warning(
            "Supervisor agent not initialized at startup. "
            "Initializing now..."
        )

        _supervisor_agent = await create_supervisor_agent(config_settings)

    supervisor_agent = _supervisor_agent

    logger.info("Executing Supervisor Agent...")

    response = await supervisor_agent.ainvoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": state.user_query
                }
            ]
        }
    )

    decision = response["structured_response"]

    state.supervisor_route = decision.route
    state.supervisor_route_rationale = decision.rationale

    logger.info(f"Supervisor route decision: {decision.route}")

    return state


# ============================================================
# General Node
# ============================================================

async def general_node(
    state: AgentState,
    config_settings: Settings = None
) -> AgentState:

    global _general_agent

    # Fallback initialization
    if _general_agent is None:
        logger.warning(
            "General agent not initialized at startup. "
            "Initializing now..."
        )

        _general_agent = await create_general_agent(config_settings)

    general_agent = _general_agent

    logger.info("Executing General Agent...")

    response = await general_agent.ainvoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": state.user_query
                }
            ]
        }
    )

    state.general_result = response["messages"][-1].content

    logger.info("General Agent execution completed.")

    return state


# ============================================================
# Research Node
# ============================================================

async def research_node(
    state: AgentState,
    config_settings: Settings = None
) -> AgentState:

    global _research_agent

    # Fallback initialization
    if _research_agent is None:

        logger.warning(
            "Research agent not initialized at startup. "
            "Initializing now..."
        )

        _research_agent = await create_research_agent(config_settings)

    research_agent = _research_agent

    logger.info("Executing Research Agent...")

    response = await research_agent.ainvoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": state.user_query
                }
            ]
        }
    )

    state.research_result = response["messages"][-1].content

    logger.info("Research Agent execution completed.")

    return state


# ============================================================
# Coding Node
# ============================================================

async def coding_node(state: AgentState, config_settings: Settings = None) -> AgentState:
    global _coding_agent

    # Fallback initialization
    if _coding_agent is None:
        logger.warning(
            "Coding agent not initialized at startup. "
            "Initializing now..."
        )

        _coding_agent = await create_coding_agent(config_settings)

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

    logger.info("Executing Coding Agent...")

    response = await coding_agent.ainvoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
    )

    state.coding_result = response["messages"][-1].content

    logger.info("Coding Agent execution completed.")

    return state