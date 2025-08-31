from typing import TypedDict, Optional, List, Dict, Any, Annotated
from langgraph.graph import add_messages
from langchain_core.messages import BaseMessage
from ..schemas import UserIntent, AnswerResponse


class AgentState(TypedDict):
    """State schema for the agent workflow compatible with LangGraph."""
    
    user_input: str
    intent: Optional[UserIntent]
    response: Optional[AnswerResponse]
    memory: List[Dict[str, Any]]
    current_step: str
    
    # LangGraph state annotations for conversation handling
    messages: Annotated[List[BaseMessage], add_messages]
