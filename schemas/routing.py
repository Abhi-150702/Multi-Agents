from pydantic import BaseModel, Field
from typing import Literal


class RoutingDecision(BaseModel):
    route: Literal["Research", "Coding", "ResearchAndCoding"] = Field(
        description="The workflow that should handle the users request. Use CamelCase format."
    )
    rationale: str = Field(description="Brief explanation about why this route was selected.")