"""
Basic calculator operations module.
"""

from typing import Union


class Calculator:
    """A simple calculator class for basic arithmetic operations."""

    def add(self, a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
        """
        Add two numbers.

        Args:
            a: First number
            b: Second number

        Returns:
            Sum of a and b
        """
        return a + b

    def subtract(self, a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
        """
        Subtract b from a.

        Args:
            a: First number
            b: Second number

        Returns:
            Difference of a and b
        """
        return a - b

    def multiply(self, a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
        """
        Multiply two numbers.

        Args:
            a: First number
            b: Second number

        Returns:
            Product of a and b
        """
        return a * b

    def divide(self, a: Union[int, float], b: Union[int, float]) -> float:
        """
        Divide a by b.

        Args:
            a: Numerator
            b: Denominator

        Returns:
            Quotient of a and b

        Raises:
            ValueError: If b is zero
        """
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b

    def power(self, base: Union[int, float], exponent: Union[int, float]) -> float:
        """
        Raise base to the power of exponent.

        Args:
            base: Base number
            exponent: Exponent

        Returns:
            base raised to the power of exponent
        """
        return base**exponent

    def square_root(self, n: Union[int, float]) -> float:
        """
        Calculate the square root of a number.

        Args:
            n: Number to calculate square root of

        Returns:
            Square root of n

        Raises:
            ValueError: If n is negative
        """
        if n < 0:
            raise ValueError("Cannot calculate square root of negative number")
        return n**0.5
