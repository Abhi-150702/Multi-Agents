from typing import Literal
from schemas.state import AgentState
from langgraph.graph import END

def route_from_supervisor(state: AgentState) -> Literal["Research", "Coding", "ResearchAndCoding"]:
    """
    Route from supervisor based on the task type.
    Returns the routing decision in CamelCase format to match node names.
    """
    # The routing decision from supervisor
    route = state.supervisor_route
    print(f"DEBUG: Supervisor route decision: {route}")
    return route

def route_after_research(state: AgentState) -> str:
    """
    Route after research node completes.
    If supervisor chose ResearchAndCoding, go to Coder.
    Otherwise, end the workflow.
    """
    if state.supervisor_route == 'ResearchAndCoding':
        return "Coder"
    else:
        return "end"

def get_supervisor_routes():
    """
    A function to return the node based on the condition supervisor agents decides.
    It is a map of condition : node.
    Node names are in CamelCase format.
    """
    return {
        "Research" : "Researcher",
        "Coding" : "Coder",
        "ResearchAndCoding" : "Researcher"
    }

def get_research_coder_routes():
    """
    A function to return the node after research agents. (only for research + coding)
    It is a map of condition : node .
    """
    return {
        'Coder': "Coder",
        "end": END
    }