"""
Simple logging schemas for the Report-Building Agent.

This module contains basic schemas for capturing tool calls and user sessions
as specified in the project requirements.
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any
from datetime import datetime


class SimpleLog(BaseModel):
    """
    Very simple schema for basic logging as mentioned in requirements.
    
    Just captures basic information about tool calls and sessions.
    """
    session_id: str
    tool_calls: List[str] = Field(default_factory=list, description="Simple list of tool names used")
    interactions: List[str] = Field(default_factory=list, description="Simple list of user interactions")
    timestamp: datetime = Field(default_factory=datetime.now)

    def log_tool_call(self, tool_name: str) -> None:
        """Log a tool call by name."""
        self.tool_calls.append(tool_name)

    def log_interaction(self, interaction: str) -> None:
        """Log a user interaction."""
        self.interactions.append(interaction)


# Example usage
if __name__ == "__main__":
    # Very simple logging example
    log = SimpleLog(session_id="session_001")
    
    log.log_tool_call("web_search")
    log.log_tool_call("document_retrieval")
    log.log_interaction("User asked about AI")
    
    print("Simple logging example:")
    print(log.model_dump_json(indent=2))
