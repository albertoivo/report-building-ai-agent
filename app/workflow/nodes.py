"""Node functions for the agent workflow."""

from typing import Dict, Any
from datetime import datetime
from ..schemas import UserIntent, AnswerResponse
from .state import AgentState


def classify_intent(state: AgentState) -> AgentState:
    """Classify user intent based on input."""
    user_input = state.user_input.lower()
    
    # Simple keyword-based intent classification
    if any(word in user_input for word in ["what", "how", "why", "who", "when", "where"]):
        intent_type = "qa"
        confidence = 0.8
        reasoning = "Detected question words indicating Q&A intent"
    elif any(word in user_input for word in ["summarize", "summary", "brief", "overview"]):
        intent_type = "summarization"
        confidence = 0.9
        reasoning = "Detected summarization keywords"
    elif any(word in user_input for word in ["calculate", "compute", "math", "+", "-", "*", "/"]):
        intent_type = "calculation"
        confidence = 0.85
        reasoning = "Detected calculation keywords or operators"
    else:
        intent_type = "qa"
        confidence = 0.6
        reasoning = "Default to Q&A for unclear intent"
    
    state.intent = UserIntent(
        intent_type=intent_type,
        confidence=confidence,
        reasoning=reasoning
    )
    state.current_step = "intent_classified"
    return state


def qa_agent(state: AgentState) -> AgentState:
    """Handle question-answering requests."""
    response = AnswerResponse(
        question=state.user_input,
        answer=f"This is a Q&A response to: {state.user_input}",
        sources=["knowledge_base"],
        confidence=0.8
    )
    
    state.response = response
    state.current_step = "qa_completed"
    return state


def summarization_agent(state: AgentState) -> AgentState:
    """Handle summarization requests."""
    response = AnswerResponse(
        question=state.user_input,
        answer=f"Summary: {state.user_input[:50]}...",
        sources=["document_processor"],
        confidence=0.9
    )
    
    state.response = response
    state.current_step = "summarization_completed"
    return state


def calculation_agent(state: AgentState) -> AgentState:
    """Handle calculation requests."""
    try:
        # Simple calculation evaluation (for demo purposes only)
        # In production, use a proper math parser
        if any(op in state.user_input for op in ["+", "-", "*", "/"]):
            # This is a simplified example - use proper parsing in production
            result = "Calculation result would be processed here"
        else:
            result = "No calculation detected"
        
        response = AnswerResponse(
            question=state.user_input,
            answer=f"Calculation result: {result}",
            sources=["calculator"],
            confidence=0.95
        )
    except Exception:
        response = AnswerResponse(
            question=state.user_input,
            answer="Unable to process calculation",
            sources=["calculator"],
            confidence=0.3
        )
    
    state.response = response
    state.current_step = "calculation_completed"
    return state


def update_memory(state: AgentState) -> AgentState:
    """Update agent memory with conversation information."""
    memory_entry = {
        "timestamp": datetime.now().isoformat(),
        "user_input": state.user_input,
        "intent": state.intent.model_dump() if state.intent else None,
        "response": state.response.model_dump() if state.response else None
    }
    
    state.memory.append(memory_entry)
    state.current_step = "memory_updated"
    return state
