import sys
from pathlib import Path

# Add parent directory to path so we can import app module
sys.path.append(str(Path(__file__).parent.parent))

from app.agent import IntegratedAgent
from langchain_core.messages import HumanMessage, AIMessage


def test_memory_step_by_step():
    """Debug memory management step by step."""
    print("=== Memory Debug Test ===\n")

    agent = IntegratedAgent()

    # Step 1: First question
    print("🔸 Step 1: First question")
    print("Input: 'What is the capital of France?'")
    response1 = agent.process_input("What is the capital of France?")
    print(f"Answer: {response1.answer}")
    print(f"Conversation messages count: {len(agent.conversation_messages)}")

    # Debug: Print all messages
    print("\nMessages after first interaction:")
    for i, msg in enumerate(agent.conversation_messages):
        msg_type = (
            "Human"
            if isinstance(msg, HumanMessage)
            else "AI" if isinstance(msg, AIMessage) else "System"
        )
        print(f"  {i+1}. {msg_type}: {msg.content}")

    # Step 2: Context question
    print("\n🔸 Step 2: Context question")
    print("Input: 'What did I just ask?'")
    response2 = agent.process_input("What did I just ask?")
    print(f"Answer: {response2.answer}")
    print(f"Conversation messages count: {len(agent.conversation_messages)}")

    # Debug: Print all messages after second interaction
    print("\nMessages after second interaction:")
    for i, msg in enumerate(agent.conversation_messages):
        msg_type = (
            "Human"
            if isinstance(msg, HumanMessage)
            else "AI" if isinstance(msg, AIMessage) else "System"
        )
        print(f"  {i+1}. {msg_type}: {msg.content}")

    # Check if the context question worked
    print(f"\n🔍 Analysis:")
    print(f"Response contains 'capital': {'capital' in response2.answer.lower()}")
    print(f"Response contains 'france': {'france' in response2.answer.lower()}")
    print(f"Full response: '{response2.answer}'")

    # Test result
    if "what is the capital of france" in response2.answer.lower():
        print("\n✅ Memory test PASSED!")
        return True
    else:
        print("\n❌ Memory test FAILED!")
        return False


if __name__ == "__main__":
    test_memory_step_by_step()
