# This is the main calculator module

from langchain_core.tools import tool

# @ tool is a decorartor thast helps the langchain to recognize this function as a tool

@tool
def add( a: float, b: float) -> float:

    """
        Calculate the addition of two numbers.
        Use this for sum operations.
    """

    return a + b

@tool
def sub( a: float, b: float) -> float:
    """
        Calculate the subtraction of two numbers.
        Use this for subtraction operations.
        Use this for sub operations.
    """

    return a - b

@tool
def mul( a: float, b: float) -> float:

    """
        Calculate the multiplication of two numbers.
        Use this tool whenever you need to perform mathematical multiplication.
    """

    return a * b

@tool
def divide( a: float, b: float) -> float:
    """
        Calculate the division of two numbers.
        Use this tool whenever you need to perform mathematical division.
        If b is zero, raise a ValueError and indicate that division by zero is not allowed and stop the operation.
    """

    if b == 0:
        raise ValueError("Division by zero is not allowed.")
    
    return a / b