from pydantic import BaseModel, Field
from datetime import datetime
from typing import Dict, Any, Optional


class ToolCall(BaseModel):
    """Schema for logging tool calls."""
    
    tool_name: str
    parameters: Dict[str, Any]
    timestamp: datetime = Field(default_factory=datetime.now)
    result: Optional[str] = None


class SessionLog(BaseModel):
    """Schema for logging user sessions."""
    
    session_id: str
    user_query: str
    tool_calls: list[ToolCall] = Field(default_factory=list)
    response: Optional[str] = None
    started_at: datetime = Field(default_factory=datetime.now)
    ended_at: Optional[datetime] = None
