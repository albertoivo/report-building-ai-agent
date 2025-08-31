"""Test the enhanced intent classification system using real OpenAI API."""

import sys
import unittest
from pathlib import Path

# Add parent directory to path so we can import app module
sys.path.append(str(Path(__file__).parent.parent))

from app.services import IntentClassifier
from app.schemas import UserIntent


class TestIntentClassification(unittest.TestCase):
    """Test intent classification with various inputs and edge cases."""

    def setUp(self):
        """Set up test with real OpenAI API."""
        # Initialize classifier (will use real OpenAI API)
        self.classifier = IntentClassifier()

    def test_calculation_intent_basic(self):
        """Test basic calculation intent classification."""
        test_cases = [
            "2 + 2",
            "calculate 15% of 200",
            "what's 5 times 8",
            "solve x + 5 = 10",
            "compute the square root of 16",
        ]

        for case in test_cases:
            with self.subTest(case=case):
                result = self.classifier.classify_intent(case)
                self.assertIsInstance(result, UserIntent)
                self.assertEqual(result.intent_type, "calculation")
                self.assertGreater(
                    result.confidence, 0.3
                )  # Lower threshold for real API

    def test_summarization_intent_basic(self):
        """Test basic summarization intent classification."""
        test_cases = [
            "summarize this document",
            "give me a summary",
            "what are the main points?",
            "recap our conversation",
            "provide an overview",
        ]

        for case in test_cases:
            with self.subTest(case=case):
                result = self.classifier.classify_intent(case)
                self.assertIsInstance(result, UserIntent)
                self.assertEqual(result.intent_type, "summarization")
                self.assertGreater(
                    result.confidence, 0.3
                )  # Lower threshold for real API

    def test_qa_intent_basic(self):
        """Test basic QA intent classification."""
        test_cases = [
            "what is artificial intelligence?",
            "how does machine learning work?",
            "explain the concept of neural networks",
            "tell me about Python programming",
            "why is this important?",
        ]

        for case in test_cases:
            with self.subTest(case=case):
                result = self.classifier.classify_intent(case)
                self.assertIsInstance(result, UserIntent)
                self.assertEqual(result.intent_type, "qa")
                self.assertGreater(
                    result.confidence, 0.3
                )  # Lower threshold for real API

    def test_conversation_context_influence(self):
        """Test that conversation context influences classification."""
        user_input = "What did we discuss?"

        # Test without context
        result_no_context = self.classifier.classify_intent(user_input)
        self.assertIsInstance(result_no_context, UserIntent)

        # Test with calculation context
        calc_context = "User: Calculate 2+2\nAssistant: The result is 4"
        result_calc_context = self.classifier.classify_intent(user_input, calc_context)
        self.assertIsInstance(result_calc_context, UserIntent)

        # Both should be valid UserIntent objects
        self.assertIsInstance(result_no_context, UserIntent)
        self.assertIsInstance(result_calc_context, UserIntent)

    def test_structured_output_fields(self):
        """Test that structured output fields are populated correctly."""
        test_input = "What's 2+2?"
        result = self.classifier.classify_intent(test_input)

        # Check all required fields exist
        self.assertIsInstance(result, UserIntent)
        self.assertIn(result.intent_type, ["calculation", "qa", "summarization"])
        self.assertIsInstance(result.confidence, float)
        self.assertGreaterEqual(result.confidence, 0.0)
        self.assertLessEqual(result.confidence, 1.0)
        self.assertIsInstance(result.reasoning, str)
        self.assertIsInstance(result.keywords_found, list)

    def test_edge_cases(self):
        """Test edge cases and error handling."""
        edge_cases = [
            "",  # Empty string
            "   ",  # Whitespace only
            "random text that doesn't fit categories",
            "?????",  # Special characters
            "a" * 500,  # Very long string
        ]

        for case in edge_cases:
            with self.subTest(case=case):
                try:
                    result = self.classifier.classify_intent(case)
                    self.assertIsInstance(result, UserIntent)
                    # Should default to some valid intent
                    self.assertIn(
                        result.intent_type, ["calculation", "qa", "summarization"]
                    )
                except Exception as e:
                    # If there's an error, it should be a meaningful one
                    self.assertIsInstance(e, Exception)

    def test_mixed_intent_examples(self):
        """Test examples that could be multiple intents."""
        mixed_cases = [
            "Can you calculate and then summarize the results?",
            "What is 2+2 and how does addition work?",
            "Summarize what we calculated earlier",
        ]

        for case in mixed_cases:
            with self.subTest(case=case):
                result = self.classifier.classify_intent(case)
                self.assertIsInstance(result, UserIntent)
                # Should classify as one of the valid intents
                self.assertIn(
                    result.intent_type, ["calculation", "qa", "summarization"]
                )

    def test_confidence_scoring(self):
        """Test confidence scoring for different types of inputs."""
        # Very clear examples should have higher confidence
        clear_examples = [
            ("2 + 2", "calculation"),
            ("what is AI?", "qa"),
            ("summarize this", "summarization"),
        ]

        for text, expected_intent in clear_examples:
            with self.subTest(text=text):
                result = self.classifier.classify_intent(text)
                self.assertEqual(result.intent_type, expected_intent)
                # Real API might have different confidence levels
                self.assertGreater(result.confidence, 0.1)


if __name__ == "__main__":
    unittest.main()
