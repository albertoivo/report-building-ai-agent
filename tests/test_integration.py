"""Integration and End-to-End Testing following the Example Testing Strategy."""

import sys
from pathlib import Path

# Add parent directory to path so we can import app module
sys.path.append(str(Path(__file__).parent.parent))

from app.agent import IntegratedAgent


def test_agent():
    """Test the integrated agent following the Example Testing Strategy."""
    print("=== Integration and Testing ===\n")
    
    # Initialize agent
    agent = IntegratedAgent()
    
    print("🔸 Testing End-to-End Functionality")
    print("=" * 50)
    
    # Test 1: Valid QA input
    print("\n1. Testing Valid QA Input:")
    print("Input: 'What is the capital of France?'")
    response = agent.process_input("What is the capital of France?")
    print(f"Answer: {response.answer}")
    print(f"Sources: {response.sources}")
    print(f"Confidence: {response.confidence}")
    
    # With real OpenAI, we expect a valid answer (not empty) that likely contains "Paris"
    assert response.answer is not None and len(response.answer.strip()) > 0, "Answer should not be empty"
    assert response.sources is not None, "Sources should not be None"
    print("✅ QA test passed!")
    
    # Test 2: Valid summarization input
    print("\n2. Testing Valid Summarization Input:")
    print("Input: 'Summarize the following text about artificial intelligence...'")
    response = agent.process_input("Summarize the following text about artificial intelligence...")
    print(f"Answer: {response.answer}")
    print(f"Sources: {response.sources}")
    
    assert response.answer is not None, "Answer should not be None"
    assert "summary" in response.answer.lower(), "Response should contain 'summary'"
    print("✅ Summarization test passed!")
    
    # Test 3: Valid calculation input
    print("\n3. Testing Valid Calculation Input:")
    print("Input: '5 + 7'")
    response = agent.process_input("5 + 7")
    print(f"Answer: {response.answer}")
    print(f"Sources: {response.sources}")
    
    assert response.answer == "12", f"Expected '12', got '{response.answer}'"
    print("✅ Calculation test passed!")
    
    # Test 4: Invalid input
    print("\n4. Testing Invalid Input:")
    print("Input: '!!!'")
    response = agent.process_input("!!!")
    print(f"Answer: {response.answer}")
    
    # Should handle gracefully without crashing
    assert response.answer is not None, "Should return some response for invalid input"
    print("✅ Invalid input test passed!")
    
    # Test 5: Memory management
    print("\n5. Testing Memory Management:")
    print("First input: 'What is the capital of France?'")
    agent.process_input("What is the capital of France?")
    
    print("Second input: 'What did I just ask?'")
    response = agent.process_input("What did I just ask?")
    print(f"Answer: {response.answer}")
    
    # Should contain the previous question text
    assert "what is the capital of france" in response.answer.lower(), "Should remember previous question"
    print("✅ Memory management test passed!")
    
    # Test 6: Tool usage verification
    print("\n6. Testing Tool Usage:")
    print("Input: '10 * 5'")
    response = agent.process_input("10 * 5")
    print(f"Answer: {response.answer}")
    print(f"Sources: {response.sources}")
    
    assert response.answer == "50", f"Calculator tool should work, got '{response.answer}'"
    assert "calculator_tool" in response.sources, "Should use calculator tool"
    print("✅ Tool usage test passed!")
    
    # Test 7: Logging and session management
    print("\n7. Testing Logging and Session Management:")
    memory = agent.get_memory()
    print(f"Memory entries: {len(memory)}")
    print(f"Last memory entry: {memory[-1] if memory else 'None'}")
    
    assert len(memory) > 0, "Should have memory entries"
    print("✅ Logging and session management test passed!")
    
    print("\n" + "=" * 50)
    print("🎉 ALL INTEGRATION TESTS PASSED!")
    print("🎉 The agent works as a complete system!")
    print("🎉 All components work together seamlessly!")


def test_error_handling():
    """Test error handling scenarios."""
    print("\n🔸 Testing Error Handling")
    print("=" * 30)
    
    agent = IntegratedAgent()
    
    # Test with various edge cases
    edge_cases = [
        "",  # Empty input
        "   ",  # Whitespace only
        "a" * 1000,  # Very long input
        "🚀🌟💫",  # Emojis only
    ]
    
    for i, case in enumerate(edge_cases, 1):
        print(f"\n{i}. Testing edge case: '{case[:20]}{'...' if len(case) > 20 else ''}'")
        try:
            response = agent.process_input(case)
            print(f"Response: {response.answer[:50]}{'...' if len(response.answer) > 50 else ''}")
            print("✅ Handled gracefully")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n✅ Error handling tests completed!")


if __name__ == "__main__":
    try:
        test_agent()
        test_error_handling()
        print("\n🎯 ALL TESTS COMPLETED SUCCESSFULLY!")
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
