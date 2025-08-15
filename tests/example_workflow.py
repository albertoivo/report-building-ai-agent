"""Example usage of the agent workflow."""

import sys
from pathlib import Path

# Add parent directory to path so we can import app module
sys.path.append(str(Path(__file__).parent.parent))

from app.workflow import create_workflow, AgentState


def main():
    """Demonstrate the workflow functionality."""
    # Create workflow
    workflow = create_workflow()
    
    # Test different types of inputs
    test_inputs = [
        "What is the weather today?",
        "Summarize this document",
        "Calculate 2 + 2",
        "Hello there"
    ]
    
    for user_input in test_inputs:
        print(f"\n--- Processing: '{user_input}' ---")
        
        # Create initial state
        initial_state = AgentState(user_input=user_input)
        
        # Run workflow
        final_state = workflow.run(initial_state)
        
        # Display results
        print(f"Intent: {final_state.intent.intent_type if final_state.intent else 'None'}")
        print(f"Response: {final_state.response.answer if final_state.response else 'None'}")
        print(f"Memory entries: {len(final_state.memory)}")


if __name__ == "__main__":
    main()
