from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class ToolCall(BaseModel):
    """Schema for logging tool calls."""
    tool_name: str
    parameters: dict
    result: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)


class SessionLog(BaseModel):
    """Schema for logging user sessions."""
    session_id: str
    user_query: str
    response: Optional[str] = None
    tool_calls: List[ToolCall] = Field(default_factory=list)
    started_at: datetime = Field(default_factory=datetime.now)
    ended_at: Optional[datetime] = None
