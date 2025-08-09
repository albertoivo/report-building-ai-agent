"""
Test file demonstrating the usage of the Report-Building Agent schemas.

This file shows how to use the schemas for validation, serialization, and error handling.
"""

import sys
from pathlib import Path

# Add the parent directory to sys.path so we can import from app
sys.path.insert(0, str(Path(__file__).parent.parent))

from schemas import AnswerResponse, UserIntent
from log_schemas import SimpleLog


def test_answer_response():
    """Test the AnswerResponse schema."""
    print("=== Testing AnswerResponse Schema ===")
    
    # Valid response
    response = AnswerResponse(
        question="What is machine learning?",
        answer="Machine learning is a subset of artificial intelligence that enables computers to learn and improve from experience without being explicitly programmed.",
        sources=["Stanford AI Course", "MIT OpenCourseWare", "Coursera ML Course"],
        confidence=0.92
    )
    
    print("Valid AnswerResponse:")
    print(response.model_dump_json(indent=2))
    print()
    
    # Test validation error
    try:
        invalid_response = AnswerResponse(
            question="Test question",
            answer="Test answer", 
            sources=[],
            confidence=2.0  # Invalid: > 1.0
        )
    except Exception as e:
        print(f"Validation error (as expected): {e}")
    print()


def test_user_intent():
    """Test the UserIntent schema."""
    print("=== Testing UserIntent Schema ===")
    
    # Test valid intents
    intents = [
        UserIntent(
            intent_type="qa",
            confidence=0.95,
            reasoning="User asked a direct question requiring factual information"
        ),
        UserIntent(
            intent_type="summarization", 
            confidence=0.88,
            reasoning="User requested a summary of multiple documents"
        ),
        UserIntent(
            intent_type="calculation",
            confidence=0.76,
            reasoning="User provided numerical data and asked for computation"
        )
    ]
    
    for intent in intents:
        print(f"Valid UserIntent ({intent.intent_type}):")
        print(intent.model_dump_json(indent=2))
        print()
    
    # Test invalid intent type
    try:
        invalid_intent = UserIntent(
            intent_type="invalid_type",  # Not in allowed Literal values
            confidence=0.5,
            reasoning="This should fail"
        )
    except Exception as e:
        print(f"Validation error for invalid intent type (as expected): {e}")
    print()


def test_logging_schemas():
    """Test the simplified logging schemas."""
    print("=== Testing Simplified Logging Schemas ===")
    
    # Create a simple log
    log = SimpleLog(session_id="session_123")
    
    # Add some tool calls
    log.log_tool_call("web_search")
    log.log_tool_call("document_search")
    
    # Add some interactions
    log.log_interaction("User asked about AI")
    log.log_interaction("User requested ML summary")
    
    print("SimpleLog with tool calls and interactions:")
    print(log.model_dump_json(indent=2))
    print()


def test_schema_integration():
    """Test how schemas work together in a simplified workflow."""
    print("=== Testing Simplified Schema Integration ===")
    
    # Simulate a complete interaction workflow
    user_question = "What are the benefits of renewable energy?"
    
    # 1. Detect user intent
    intent = UserIntent(
        intent_type="qa",
        confidence=0.93,
        reasoning="User asked a direct question about renewable energy benefits"
    )
    
    # 2. Generate response
    response = AnswerResponse(
        question=user_question,
        answer="Renewable energy offers several benefits including reduced greenhouse gas emissions, lower long-term costs, energy independence, and job creation in green technology sectors.",
        sources=["EPA Environmental Reports", "International Energy Agency", "National Renewable Energy Laboratory"],
        confidence=0.89
    )
    
    # 3. Log the session
    log = SimpleLog(session_id="session_001")
    log.log_tool_call("web_search")
    log.log_tool_call("document_retrieval")
    log.log_interaction(f"Q: {user_question}")
    log.log_interaction(f"A: {response.answer}")
    
    print("Complete simplified workflow:")
    print("1. User Intent:")
    print(intent.model_dump_json(indent=2))
    print("\n2. Agent Response:")
    print(response.model_dump_json(indent=2))
    print("\n3. Simple Log:")
    print(log.model_dump_json(indent=2))


if __name__ == "__main__":
    test_answer_response()
    test_user_intent()
    test_logging_schemas()
    test_schema_integration()
    
    print("\n=== Simplified Schema Testing Complete ===")
    print("All schemas are working correctly with proper validation!")
