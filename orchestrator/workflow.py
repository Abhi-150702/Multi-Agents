from langgraph.graph import StateGraph, START

from orchestrator.nodes import supervisor_node, general_node, research_node, coding_node
from orchestrator.routes import route_from_supervisor, route_after_research, get_supervisor_routes, get_research_coder_routes
from schemas.state import AgentState

from config.logging_config import setup_logger
logger = setup_logger('workflow')

def get_workflow(config_settings):
    builder = StateGraph(AgentState)

    # Add nodes with consistent naming (Capital Case)
    builder.add_node('Supervisor', lambda state: supervisor_node(state, config_settings))
    builder.add_node('General', lambda state: general_node(state, config_settings))
    builder.add_node('Researcher', lambda state: research_node(state, config_settings))
    builder.add_node('Coder', lambda state: coding_node(state, config_settings))

    # Start with Supervisor
    builder.add_edge(START, 'Supervisor')

    # Conditional edges from Supervisor
    # The routing function returns a key, and the path mapping function maps it to a node
    builder.add_conditional_edges(
        'Supervisor',
        route_from_supervisor,
        get_supervisor_routes()
    )

    # Conditional edges from Researcher
    builder.add_conditional_edges(
        'Researcher',
        route_after_research,
        get_research_coder_routes()
    )

    return builder.compile()
