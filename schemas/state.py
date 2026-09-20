from pydantic import BaseModel, Field
from typing import Optional

class AgentState(BaseModel):
    user_query: str = Field(description="Input query from user")
    supervisor_route: str = Field(default="", description="Decision for routing from supervisor Agent")
    supervisor_route_rationale: str = Field(default="", description="Reasoning behind the route from supervisor agent.")
    research_result: str = Field(default="", description="Output research data from research agent.")
    coding_result: str = Field(default="", description="Output coding result from coding agent.")