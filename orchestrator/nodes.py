from typing import Literal

from agents.supervisor.agent import create_supervisor_agent
from agents.research.agent import create_research_agent
from agents.coding.agent import create_coding_agent

from schemas.state import AgentState



def supervisor_node(state: AgentState) -> AgentState:
    supervisor_agent = create_supervisor_agent()

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


def research_node(state: AgentState) -> AgentState:
    research_agent = create_research_agent()

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
    coding_agent = create_coding_agent()

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
