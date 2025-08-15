"""Test the prompt engineering system."""

import sys
from pathlib import Path

# Add parent directory to path so we can import app module
sys.path.append(str(Path(__file__).parent.parent))

from app.prompts import intent_classification_prompt, get_chat_prompt_template
from app.prompts.llm_simulator import SimpleLLMSimulator


def test_prompt_engineering():
    """Test the prompt engineering system."""
    # Initialize LLM simulator
    llm = SimpleLLMSimulator()
    
    # Test cases
    test_inputs = [
        "What is artificial intelligence?",
        "Summarize this document about AI",
        "Calculate 15 + 25",
        "Hello, how are you?"
    ]
    
    print("=== Prompt Engineering Tests ===\n")
    
    for user_input in test_inputs:
        print(f"🔸 User Input: '{user_input}'")
        print("-" * 50)
        
        # Step 1: Intent Classification
        classification_prompt = intent_classification_prompt.format(
            user_input=user_input,
            conversation_history="[]"
        )
        
        print("📋 Intent Classification Prompt:")
        print(classification_prompt[:200] + "...")
        print()
        
        # Simulate intent classification
        intent = llm.classify_intent(classification_prompt)
        print(f"🎯 Classified Intent: {intent.intent_type}")
        print(f"🎯 Confidence: {intent.confidence}")
        print(f"🎯 Reasoning: {intent.reasoning}")
        print()
        
        # Step 2: Get appropriate chat prompt
        chat_prompt = get_chat_prompt_template(intent.intent_type)
        messages = chat_prompt.format_messages(user_input=user_input)
        
        print("💬 System Prompt:")
        print(f"'{messages[0]['content'][:100]}...'")
        print()
        
        # Step 3: Generate response
        response = llm.chat(messages)
        print(f"🤖 LLM Response: {response}")
        print("=" * 60)
        print()


if __name__ == "__main__":
    test_prompt_engineering()
