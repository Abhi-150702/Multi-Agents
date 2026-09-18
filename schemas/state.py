from pydantic import BaseModel, Field

class AgentState(BaseModel):
    user_query: str = Field(description="Input query from user")
    supervisor_route: str = Field(description="Decision for routing from supervisor Agent")
    supervisor_route_rationale: str = Field(description="Reasoning behind the route from supervisor agent.")
    research_result : str = Field(description="Output research data from research agent.")
    coding_result : str = Field(description="Output coding result from coding agent.")