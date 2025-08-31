"""Test the calculator tool using unittest framework."""

import sys
import unittest
from pathlib import Path

# Add parent directory to path so we can import app module
sys.path.append(str(Path(__file__).parent.parent))

from app.tools import langchain_calculate


class TestCalculator(unittest.TestCase):
    """Unit tests for the LangChain calculator tool."""

    def test_addition(self):
        """Test basic addition operation."""
        result = langchain_calculate.invoke({"expression": "2 + 3"})
        self.assertEqual(result, "5")

    def test_multiplication(self):
        """Test multiplication operation."""
        result = langchain_calculate.invoke({"expression": "10 * 5"})
        self.assertEqual(result, "50")

    def test_division(self):
        """Test division operation."""
        result = langchain_calculate.invoke({"expression": "100 / 4"})
        self.assertEqual(result, "25.0")

    def test_subtraction(self):
        """Test subtraction operation."""
        result = langchain_calculate.invoke({"expression": "15 - 7"})
        self.assertEqual(result, "8")

    def test_parentheses(self):
        """Test operation with parentheses."""
        result = langchain_calculate.invoke({"expression": "(2 + 3) * 4"})
        self.assertEqual(result, "20")

    def test_decimal_numbers(self):
        """Test operations with decimal numbers."""
        result = langchain_calculate.invoke({"expression": "2.5 + 3.7"})
        self.assertEqual(result, "6.2")

    def test_division_by_zero(self):
        """Test division by zero error handling."""
        result = langchain_calculate.invoke({"expression": "10 / 0"})
        self.assertEqual(result, "Error: Division by zero.")

    def test_invalid_syntax(self):
        """Test invalid syntax error handling."""
        result = langchain_calculate.invoke({"expression": "2 +"})
        self.assertEqual(result, "Error: Invalid syntax in expression.")

    def test_invalid_characters(self):
        """Test invalid characters error handling."""
        result = langchain_calculate.invoke({"expression": "abc + 3"})
        self.assertEqual(
            result,
            "Invalid expression. Only numbers and operators (+, -, *, /, parentheses) are allowed.",
        )

    def test_empty_expression(self):
        """Test empty expression error handling."""
        result = langchain_calculate.invoke({"expression": ""})
        self.assertEqual(
            result,
            "Invalid expression. Only numbers and operators (+, -, *, /, parentheses) are allowed.",
        )

    def test_whitespace_handling(self):
        """Test that whitespace is handled correctly."""
        result = langchain_calculate.invoke({"expression": "  2 + 3  "})
        self.assertEqual(result, "5")

    def test_complex_expression(self):
        """Test more complex mathematical expression."""
        result = langchain_calculate.invoke({"expression": "((2 + 3) * 4) - 10"})
        self.assertEqual(result, "10")


if __name__ == "__main__":
    unittest.main()
