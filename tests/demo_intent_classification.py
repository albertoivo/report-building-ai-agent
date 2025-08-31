"""Demonstration of the enhanced intent classification system."""

import sys
from pathlib import Path

# Add parent directory to path so we can import app module
sys.path.append(str(Path(__file__).parent.parent))

from app.services import IntentClassifier


def demonstrate_intent_classification():
    """Demonstrate the enhanced intent classification capabilities."""
    
    classifier = IntentClassifier()
    
    test_cases = [
        # Calculation examples
        ("2 + 2", "Basic arithmetic"),
        ("calculate 15% of 200", "Percentage calculation"),
        ("what's 5 times 8", "Natural language math"),
        ("solve x + 5 = 10", "Equation solving"),
        
        # Summarization examples
        ("summarize this document", "Direct summarization request"),
        ("what are the main points?", "Main points request"),
        ("give me a recap", "Recap request"),
        ("provide an overview", "Overview request"),
        
        # QA examples
        ("what is artificial intelligence?", "Definition question"),
        ("how does machine learning work?", "Process explanation"),
        ("explain neural networks", "Concept explanation"),
        ("tell me about Python", "Information request"),
        
        # Ambiguous/mixed examples
        ("What about the calculation results?", "Context-dependent"),
        ("help", "Very ambiguous"),
        ("this", "Minimal context"),
    ]
    
    print("=== Enhanced Intent Classification Demonstration ===\n")
    
    for user_input, description in test_cases:
        print(f"Input: '{user_input}' ({description})")
        print("-" * 50)
        
        result = classifier.classify_with_fallback(user_input)
        
        print(f"Intent: {result.intent_type}")
        print(f"Confidence: {result.confidence:.2f}")
        print(f"Reasoning: {result.reasoning}")
        
        if result.keywords_found:
            print(f"Keywords Found: {result.keywords_found}")
        
        if result.context_influence:
            print(f"Context Influence: {result.context_influence}")
        
        print("\n" + "="*60 + "\n")


def demonstrate_context_influence():
    """Demonstrate how conversation context influences classification."""
    
    classifier = IntentClassifier()
    
    print("=== Context Influence Demonstration ===\n")
    
    ambiguous_input = "What about the results?"
    
    contexts = [
        ("", "No context"),
        ("User: Calculate 10 * 5\nAssistant: 10 * 5 = 50", "Calculation context"),
        ("User: Summarize the document\nAssistant: Here's a summary...", "Summarization context"),
        ("User: What is AI?\nAssistant: AI is artificial intelligence...", "QA context"),
    ]
    
    for context, description in contexts:
        print(f"Context: {description}")
        print(f"Input: '{ambiguous_input}'")
        print("-" * 40)
        
        result = classifier.classify_with_fallback(ambiguous_input, context)
        
        print(f"Intent: {result.intent_type}")
        print(f"Confidence: {result.confidence:.2f}")
        print(f"Reasoning: {result.reasoning}")
        
        if result.context_influence:
            print(f"Context Influence: {result.context_influence}")
        
        print("\n" + "="*50 + "\n")


if __name__ == "__main__":
    demonstrate_intent_classification()
    demonstrate_context_influence()
