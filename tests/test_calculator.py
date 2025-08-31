"""Test the calculator tool."""

import sys
from pathlib import Path

# Add parent directory to path so we can import app module
sys.path.append(str(Path(__file__).parent.parent))

from app.tools import langchain_calculate


def test_calculator():
    """Test various calculator operations."""
    test_cases = [
        "2 + 3",
        "10 * 5", 
        "100 / 4",
        "15 - 7",
        "(2 + 3) * 4",
        "2.5 + 3.7",
        "10 / 0",  # Division by zero
        "2 +",     # Invalid syntax
        "abc + 3", # Invalid characters
        "",        # Empty expression
    ]
    
    print("=== Calculator Tool Tests ===\n")
    
    for expression in test_cases:
        result = langchain_calculate.invoke({"expression": expression})
        print(f"Expression: '{expression}'")
        print(f"Result: {result}")
        print("-" * 30)


if __name__ == "__main__":
    test_calculator()
