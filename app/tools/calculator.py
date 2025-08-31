from langchain_core.tools import tool
from pydantic import BaseModel, Field
import re


class CalculatorInput(BaseModel):
    expression: str = Field(
        ..., description="A mathematical expression (e.g., '2 + 2', '(5 + 3) * 4')"
    )


@tool(
    "calculator",
    args_schema=CalculatorInput,
    return_direct=True,
    description="Safely evaluate a mathematical expression. Supports numbers, +, -, *, /, and parentheses.",
)
def langchain_calculate(expression: str) -> str:
    """LangChain-compatible calculator tool."""
    expr = expression.strip()

    # Check for empty expression
    if not expr:
        return "Invalid expression. Only numbers and operators (+, -, *, /, parentheses) are allowed."

    # Check if contains only allowed characters
    if not re.match(r"^[0-9+\-*/().\s]+$", expr):
        return "Invalid expression. Only numbers and operators (+, -, *, /, parentheses) are allowed."

    # Must contain at least one digit
    if not re.search(r"\d", expr):
        return "Invalid expression. Only numbers and operators (+, -, *, /, parentheses) are allowed."

    try:
        result = str(eval(expr))
        return result
    except ZeroDivisionError:
        return "Error: Division by zero."
    except SyntaxError:
        return "Error: Invalid syntax in expression."
    except Exception as e:
        return f"Error: {str(e)}"
