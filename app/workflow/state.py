from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from ..schemas import UserIntent, AnswerResponse


class AgentState(BaseModel):
    """State schema for the agent workflow."""
    
    user_input: str
    intent: Optional[UserIntent] = None
    response: Optional[AnswerResponse] = None
    memory: List[Dict[str, Any]] = []
    current_step: str = "start"
