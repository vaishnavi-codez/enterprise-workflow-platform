from langchain.tools import tool


def calculate(expression: str) -> str:
    """
    Safely evaluates a basic math expression and returns the result as a string.
    Supports +, -, *, /, and parentheses.
    """
    try:
        # Only allow safe characters — digits, operators, parentheses, decimal points, spaces
        allowed_chars = set("0123456789+-*/(). ")
        if not all(char in allowed_chars for char in expression):
            return "Sorry, that expression contains characters I can't safely evaluate. Please use only numbers and +, -, *, /, ( )."

        result = eval(expression)
        return f"The result of {expression} is {result}."

    except ZeroDivisionError:
        return "That expression involves dividing by zero, which isn't possible."
    except (SyntaxError, TypeError):
        return f"Sorry, '{expression}' isn't a valid math expression."
    except Exception as e:
        return f"Something went wrong while calculating: {e}"


@tool
def calculator_tool(expression: str) -> str:
    """Evaluate a basic math expression (addition, subtraction, multiplication, division). Use this when the user asks a math question or wants a calculation done."""
    return calculate(expression)


# Quick standalone test
if __name__ == "__main__":
    print(calculate("12 + 8"))
    print(calculate("10 / 0"))
    print(calculate("2 + hello"))