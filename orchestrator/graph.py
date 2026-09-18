from langgraph.graph import StateGraph, START

from orchestrator.nodes import supervisor_node, research_node, coding_node
from orchestrator.routes import route_from_supervisor, route_after_research, get_supervisor_routes, get_research_coder_routes
from schemas.state import AgentState


def get_workflow():
    builder = StateGraph(AgentState)

    # Add nodes with consistent naming (Capital Case)
    builder.add_node('Supervisor', supervisor_node)
    builder.add_node('Researcher', research_node)
    builder.add_node('Coder', coding_node)

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
