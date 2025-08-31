import sys
from pathlib import Path

# Add parent directory to path so we can import app module
sys.path.append(str(Path(__file__).parent.parent))

from app.agent import IntegratedAgent
from app.workflow.state import AgentState
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

def test_messages_conversation():
    """Test conversation using messages field."""
    print("=== Testing Messages in Conversation ===\n")
    
    agent = IntegratedAgent()
    
    # First interaction
    print("1. First question:")
    response1 = agent.process_input("What is the capital of France?")
    print(f"Answer: {response1.answer}")
    
    # Test the workflow with conversation context
    print("\n2. Follow-up question with context:")
    response2 = agent.process_input("What did I just ask?")
    print(f"Answer: {response2.answer}")
    
    # Test calculation with messages
    print("\n3. Calculation request:")
    response3 = agent.process_input("Calculate 15 + 25")
    print(f"Answer: {response3.answer}")
    
    # Show that messages preserve conversation flow
    print("\n4. Memory check:")
    print(f"Total interactions in memory: {len(agent.memory)}")
    
    return True

def test_messages_state_directly():
    """Test messages field directly in workflow."""
    from app.workflow import create_workflow
    
    print("\n=== Testing Messages State Directly ===\n")
    
    workflow = create_workflow()
    
    # Create state with pre-existing messages using proper LangChain message types
    initial_state = AgentState(
        user_input="What did we talk about before?",
        intent=None,
        response=None,
        memory=[],
        current_step="start",
        messages=[
            HumanMessage(content="Hello"),
            AIMessage(content="Hi there!"),
            HumanMessage(content="What is AI?"),
            AIMessage(content="AI is artificial intelligence.")
        ]
    )
    
    # Run workflow
    final_state = workflow.invoke(initial_state)
    
    print("Messages in final state:")
    for i, msg in enumerate(final_state["messages"]):
        role = "user" if isinstance(msg, HumanMessage) else "assistant" if isinstance(msg, AIMessage) else "system"
        print(f"{i+1}. {role}: {msg.content}")
    
    print(f"\nFinal response: {final_state['response'].answer}")
    
    return True

def test_message_types():
    """Test different message types."""
    print("\n=== Testing Message Types ===\n")
    
    # Test creating different message types
    human_msg = HumanMessage(content="Hello")
    ai_msg = AIMessage(content="Hi there!")
    system_msg = SystemMessage(content="System ready")
    
    messages = [human_msg, ai_msg, system_msg]
    
    print("Message types test:")
    for msg in messages:
        msg_type = type(msg).__name__
        print(f"- {msg_type}: {msg.content}")
    
    return True

if __name__ == "__main__":
    test_message_types()
    test_messages_conversation()
    test_messages_state_directly()
    print("\n✅ All message tests completed!")