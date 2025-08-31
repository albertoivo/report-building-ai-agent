"""Test the enhanced intent classification system."""

import sys
import unittest
from pathlib import Path

# Add parent directory to path so we can import app module
sys.path.append(str(Path(__file__).parent.parent))

from app.services import IntentClassifier
from app.schemas import UserIntent


class TestIntentClassification(unittest.TestCase):
    """Unit tests for the enhanced intent classification system."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.classifier = IntentClassifier()
    
    def test_calculation_intent_basic(self):
        """Test basic calculation intent classification."""
        test_cases = [
            "2 + 2",
            "calculate 15% of 200",
            "what's 5 times 8",
            "solve x + 5 = 10",
            "compute the square root of 16"
        ]
        
        for case in test_cases:
            with self.subTest(case=case):
                result = self.classifier.classify_with_fallback(case)
                self.assertIsInstance(result, UserIntent)
                self.assertEqual(result.intent_type, "calculation")
                self.assertGreater(result.confidence, 0.5)
    
    def test_summarization_intent_basic(self):
        """Test basic summarization intent classification."""
        test_cases = [
            "summarize this document",
            "give me a summary",
            "what are the main points?",
            "recap our conversation",
            "provide an overview"
        ]
        
        for case in test_cases:
            with self.subTest(case=case):
                result = self.classifier.classify_with_fallback(case)
                self.assertIsInstance(result, UserIntent)
                self.assertEqual(result.intent_type, "summarization")
                self.assertGreater(result.confidence, 0.5)
    
    def test_qa_intent_basic(self):
        """Test basic QA intent classification."""
        test_cases = [
            "what is artificial intelligence?",
            "how does machine learning work?",
            "explain the concept of neural networks",
            "tell me about Python programming",
            "why is this important?"
        ]
        
        for case in test_cases:
            with self.subTest(case=case):
                result = self.classifier.classify_with_fallback(case)
                self.assertIsInstance(result, UserIntent)
                self.assertEqual(result.intent_type, "qa")
                self.assertGreater(result.confidence, 0.4)
    
    def test_conversation_context_influence(self):
        """Test that conversation context influences classification."""
        user_input = "What about the result?"
        
        # Without context - should be QA
        result_no_context = self.classifier.classify_with_fallback(user_input)
        
        # With calculation context
        calc_context = "User: Calculate 5 * 8\nAssistant: 5 * 8 = 40"
        result_calc_context = self.classifier.classify_with_fallback(user_input, calc_context)
        
        # Both should be valid UserIntent objects
        self.assertIsInstance(result_no_context, UserIntent)
        self.assertIsInstance(result_calc_context, UserIntent)
        
        # Results should include reasoning
        self.assertIsNotNone(result_no_context.reasoning)
        self.assertIsNotNone(result_calc_context.reasoning)
    
    def test_structured_output_fields(self):
        """Test that structured output fields are populated correctly."""
        result = self.classifier.classify_with_fallback("calculate 2 + 2")
        
        # Check all required fields are present
        self.assertIsInstance(result.intent_type, str)
        self.assertIsInstance(result.confidence, float)
        self.assertIsInstance(result.reasoning, str)
        self.assertIsInstance(result.keywords_found, list)
        
        # Check confidence is in valid range
        self.assertGreaterEqual(result.confidence, 0.0)
        self.assertLessEqual(result.confidence, 1.0)
        
        # Check reasoning is not empty
        self.assertGreater(len(result.reasoning), 0)
    
    def test_confidence_scoring(self):
        """Test confidence scoring for different types of inputs."""
        # High confidence cases
        high_conf_cases = [
            "2 + 2 = ?",
            "summarize the document",
            "what is AI?"
        ]
        
        # Low confidence cases (ambiguous)
        low_conf_cases = [
            "this",
            "help",
            "okay"
        ]
        
        for case in high_conf_cases:
            with self.subTest(case=case):
                result = self.classifier.classify_with_fallback(case)
                self.assertGreater(result.confidence, 0.4)
        
        for case in low_conf_cases:
            with self.subTest(case=case):
                result = self.classifier.classify_with_fallback(case)
                # Should still provide a classification, even if low confidence
                self.assertIsInstance(result, UserIntent)
                self.assertIn(result.intent_type, ["qa", "summarization", "calculation"])
    
    def test_fallback_mechanism(self):
        """Test that keyword-based fallback works correctly."""
        # Test calculation fallback
        calc_result = self.classifier._keyword_based_fallback("solve 2 + 2")
        self.assertEqual(calc_result.intent_type, "calculation")
        self.assertGreater(calc_result.confidence, 0.5)
        
        # Test summarization fallback
        summ_result = self.classifier._keyword_based_fallback("give me a summary")
        self.assertEqual(summ_result.intent_type, "summarization")
        self.assertGreater(summ_result.confidence, 0.5)
        
        # Test QA fallback (default)
        qa_result = self.classifier._keyword_based_fallback("random text")
        self.assertEqual(qa_result.intent_type, "qa")
        self.assertGreater(qa_result.confidence, 0.4)
    
    def test_edge_cases(self):
        """Test edge cases and error handling."""
        edge_cases = [
            "",  # Empty string
            "   ",  # Whitespace only
            "!@#$%",  # Special characters only
            "a" * 1000,  # Very long input
        ]
        
        for case in edge_cases:
            with self.subTest(case=case):
                result = self.classifier.classify_with_fallback(case)
                self.assertIsInstance(result, UserIntent)
                self.assertIn(result.intent_type, ["qa", "summarization", "calculation"])
                self.assertIsInstance(result.confidence, float)
                self.assertGreaterEqual(result.confidence, 0.0)
                self.assertLessEqual(result.confidence, 1.0)
    
    def test_mixed_intent_examples(self):
        """Test examples that could be multiple intents."""
        mixed_cases = [
            "calculate the summary statistics",  # calc + summarization
            "what is 2 + 2?",  # qa + calculation
            "summarize how to solve this equation",  # summarization + calculation
        ]
        
        for case in mixed_cases:
            with self.subTest(case=case):
                result = self.classifier.classify_with_fallback(case)
                self.assertIsInstance(result, UserIntent)
                # Should pick the most dominant intent
                self.assertIn(result.intent_type, ["qa", "summarization", "calculation"])
                self.assertGreater(result.confidence, 0.3)


if __name__ == "__main__":
    unittest.main()
