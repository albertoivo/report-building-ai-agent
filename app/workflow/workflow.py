from typing import Literal
from langgraph.graph import StateGraph, END
from .state import AgentState
from .nodes import (
    classify_intent,
    qa_agent,
    summarization_agent,
    calculation_agent,
    update_memory,
)


def should_continue(
    state: AgentState,
) -> Literal["qa_agent", "summarization_agent", "calculation_agent", "__end__"]:
    """Built-in LangGraph routing function to determine next step."""
    if state["intent"] and state["intent"].intent_type == "qa":
        return "qa_agent"
    elif state["intent"] and state["intent"].intent_type == "summarization":
        return "summarization_agent"
    elif state["intent"] and state["intent"].intent_type == "calculation":
        return "calculation_agent"
    else:
        return "qa_agent"  # Default to Q&A agent


def should_end(state: AgentState) -> Literal["__end__"]:
    """Built-in routing function to end the workflow after memory update."""
    return "__end__"


def create_workflow():
    """Create and configure the agent workflow using LangGraph StateGraph with built-in routing."""
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

    # Use LangGraph's built-in routing with should_continue
    workflow.add_conditional_edges(
        "classify_intent",
        should_continue,
        {
            "qa_agent": "qa_agent",
            "summarization_agent": "summarization_agent",
            "calculation_agent": "calculation_agent",
            "__end__": END,
        },
    )

    # Add edges from agents to update_memory using built-in routing patterns
    workflow.add_edge("qa_agent", "update_memory")
    workflow.add_edge("summarization_agent", "update_memory")
    workflow.add_edge("calculation_agent", "update_memory")

    # Use built-in routing to end workflow
    workflow.add_conditional_edges("update_memory", should_end, {"__end__": END})

    # Compile and return the workflow
    return workflow.compile()
