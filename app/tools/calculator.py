from langchain_core.tools import tool
from pydantic import BaseModel, Field
from typing import Any
from app.logging import SimpleLogger
import re

def is_valid_expression(expr: str) -> bool:
    allowed_pattern = r'^[0-9+\-*/().\s]+$'
    return bool(re.match(allowed_pattern, expr))

class CalculatorInput(BaseModel):
    expression: str = Field(..., description="A valid mathematical expression (e.g., '2 + 2')")

logger = SimpleLogger()

@tool(
    "calculator",
    args_schema=CalculatorInput,
    return_direct=True,
    description="Safely evaluate a mathematical expression provided as a string. Only numbers and operators (+, -, *, /, parentheses) are allowed. Returns the result as a string."
)
def langchain_calculate(expression: str) -> str:
    """LangChain-compatible calculator tool with logging."""
    expression = expression.strip()
    if not is_valid_expression(expression):
        result = "Invalid expression. Only numbers and operators (+, -, *, /, parentheses) are allowed."
    elif not expression:
        result = "Error: Empty expression."
    else:
        try:
            result = str(eval(expression))
        except ZeroDivisionError:
            result = "Error: Division by zero."
        except SyntaxError:
            result = "Error: Invalid syntax in expression."
        except Exception as e:
            result = f"Error: {str(e)}"

    logger.log_tool_call(
        tool_name="calculator",
        parameters={"expression": expression},
        result=result
    )
    return result
