from langgraph.graph import StateGraph, START

from orchestrator.nodes import (
    supervisor_node,
    general_node,
    research_node,
    coding_node
)

from orchestrator.routes import (
    route_from_supervisor,
    route_after_research,
    get_supervisor_routes,
    get_research_coder_routes
)

from schemas.state import AgentState

from config.logging_config import setup_logger


logger = setup_logger("workflow")


def get_workflow(config_settings):

    builder = StateGraph(AgentState)

    # ========================================================
    # Supervisor
    # ========================================================

    builder.add_node(
        "Supervisor",
        lambda state: supervisor_node(
            state,
            config_settings
        )
    )

    # ========================================================
    # General
    # ========================================================

    builder.add_node(
        "General",
        lambda state: general_node(
            state,
            config_settings
        )
    )

    # ========================================================
    # Research
    # ========================================================

    async def research_node_with_config(
        state: AgentState
    ) -> AgentState:

        return await research_node(
            state,
            config_settings
        )

    builder.add_node(
        "Researcher",
        research_node_with_config
    )

    # ========================================================
    # Coding
    # ========================================================

    builder.add_node(
        "Coder",
        lambda state: coding_node(
            state,
            config_settings
        )
    )

    # ========================================================
    # Start
    # ========================================================

    builder.add_edge(
        START,
        "Supervisor"
    )

    # ========================================================
    # Supervisor Routing
    # ========================================================

    builder.add_conditional_edges(
        "Supervisor",
        route_from_supervisor,
        get_supervisor_routes()
    )

    # ========================================================
    # Research Routing
    # ========================================================

    builder.add_conditional_edges(
        "Researcher",
        route_after_research,
        get_research_coder_routes()
    )

    # ========================================================
    # Compile
    # ========================================================

    return builder.compile()