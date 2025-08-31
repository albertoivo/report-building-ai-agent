"""LangGraph workflow implementation for the agent."""

from typing import Callable, Dict
from langgraph.graph import StateGraph, END
from .state import AgentState
from .nodes import classify_intent, qa_agent, summarization_agent, calculation_agent, update_memory


def create_workflow():
    """Create and configure the agent workflow using LangGraph StateGraph."""
    # Create StateGraph with AgentState
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("classify_intent", classify_intent)
    workflow.add_node("qa_agent", qa_agent)
    workflow.add_node("summarization_agent", summarization_agent)
    workflow.add_node("calculation_agent", calculation_agent)
    workflow.add_node("update_memory", update_memory)
    
    # Set entry point
    workflow.set_entry_point("classify_intent")
    
    # Define routing function for conditional edges
    def route_from_classify_intent(state: AgentState) -> str:
        """Route from intent classification to appropriate agent."""
        if state["intent"] and state["intent"].intent_type == "qa":
            return "qa_agent"
        elif state["intent"] and state["intent"].intent_type == "summarization":
            return "summarization_agent"
        elif state["intent"] and state["intent"].intent_type == "calculation":
            return "calculation_agent"
        return "qa_agent"  # Default fallback
    
    # Add conditional edges from classify_intent to agents
    workflow.add_conditional_edges(
        "classify_intent",
        route_from_classify_intent,
        {
            "qa_agent": "qa_agent",
            "summarization_agent": "summarization_agent", 
            "calculation_agent": "calculation_agent"
        }
    )
    
    # Add edges from agents to update_memory
    workflow.add_edge("qa_agent", "update_memory")
    workflow.add_edge("summarization_agent", "update_memory")
    workflow.add_edge("calculation_agent", "update_memory")
    
    # Add edge from update_memory to END
    workflow.add_edge("update_memory", END)
    
    # Compile and return the workflow
    return workflow.compile()
