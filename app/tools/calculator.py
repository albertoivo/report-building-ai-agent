"""Calculator tool for mathematical calculations."""

import re


def tool(func):
    """Simple tool decorator."""
    func.is_tool = True
    return func


def is_valid_expression(expr: str) -> bool:
    """Validate mathematical expression to allow only safe characters."""
    # Allow only numbers, operators, parentheses, and whitespace
    allowed_pattern = r'^[0-9+\-*/().\s]+$'
    return bool(re.match(allowed_pattern, expr))


@tool
def calculate(expression: str) -> str:
    """
    Calculate mathematical expressions safely.
    
    Args:
        expression: Mathematical expression as string (e.g., "2 + 3", "10 * 5")
    
    Returns:
        Result as string or error message
    """
    # Remove whitespace
    expression = expression.strip()
    
    # Validate expression
    if not is_valid_expression(expression):
        return "Invalid expression. Only numbers and operators (+, -, *, /, parentheses) are allowed."
    
    # Check for empty expression
    if not expression:
        return "Error: Empty expression."
    
    try:
        # Evaluate the expression safely
        result = eval(expression)
        return str(result)
    except ZeroDivisionError:
        return "Error: Division by zero."
    except SyntaxError:
        return "Error: Invalid syntax in expression."
    except Exception as e:
        return f"Error: {str(e)}"
