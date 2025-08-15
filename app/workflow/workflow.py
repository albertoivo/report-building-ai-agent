"""Simple workflow implementation for the agent."""

from typing import Callable, Dict
from .state import AgentState
from .nodes import classify_intent, qa_agent, summarization_agent, calculation_agent, update_memory


class SimpleWorkflow:
    """Simple workflow implementation that routes between nodes based on state."""
    
    def __init__(self):
        self.nodes: Dict[str, Callable] = {}
        self.entry_point: str = ""
        self.routing_rules: Dict[str, Callable] = {}
    
    def add_node(self, name: str, func: Callable):
        """Add a node to the workflow."""
        self.nodes[name] = func
    
    def set_entry_point(self, name: str):
        """Set the entry point for the workflow."""
        self.entry_point = name
    
    def add_routing_rule(self, from_node: str, router: Callable):
        """Add routing logic to determine next node."""
        self.routing_rules[from_node] = router
    
    def run(self, initial_state: AgentState) -> AgentState:
        """Execute the workflow."""
        current_node = self.entry_point
        state = initial_state
        
        while current_node:
            # Execute current node
            if current_node in self.nodes:
                state = self.nodes[current_node](state)
            
            # Determine next node
            if current_node in self.routing_rules:
                current_node = self.routing_rules[current_node](state)
            else:
                current_node = None
        
        return state


def create_workflow() -> SimpleWorkflow:
    """Create and configure the agent workflow."""
    workflow = SimpleWorkflow()
    
    # Add nodes
    workflow.add_node("classify_intent", classify_intent)
    workflow.add_node("qa_agent", qa_agent)
    workflow.add_node("summarization_agent", summarization_agent)
    workflow.add_node("calculation_agent", calculation_agent)
    workflow.add_node("update_memory", update_memory)
    
    # Set entry point
    workflow.set_entry_point("classify_intent")
    
    # Add routing rules
    def route_from_classify_intent(state: AgentState) -> str:
        """Route from intent classification to appropriate agent."""
        if state.intent and state.intent.intent_type == "qa":
            return "qa_agent"
        elif state.intent and state.intent.intent_type == "summarization":
            return "summarization_agent"
        elif state.intent and state.intent.intent_type == "calculation":
            return "calculation_agent"
        return "qa_agent"  # Default fallback
    
    def route_to_memory(state: AgentState) -> str:
        """Route completed agents to memory update."""
        return "update_memory"
    
    def route_from_memory(state: AgentState) -> str:
        """End workflow after memory update."""
        return None  # End workflow
    
    # Configure routing
    workflow.add_routing_rule("classify_intent", route_from_classify_intent)
    workflow.add_routing_rule("qa_agent", route_to_memory)
    workflow.add_routing_rule("summarization_agent", route_to_memory)
    workflow.add_routing_rule("calculation_agent", route_to_memory)
    workflow.add_routing_rule("update_memory", route_from_memory)
    
    return workflow
