"""
Unit tests for Calculator operations.
"""

import pytest


class TestCalculator:
    """Test suite for Calculator class."""

    def test_add_positive_numbers(self, calculator):
        """Test addition of positive numbers."""
        assert calculator.add(2, 3) == 5
        assert calculator.add(10, 20) == 30

    def test_add_negative_numbers(self, calculator):
        """Test addition with negative numbers."""
        assert calculator.add(-5, -3) == -8
        assert calculator.add(-10, 5) == -5

    def test_add_floats(self, calculator):
        """Test addition of floating point numbers."""
        result = calculator.add(2.5, 3.7)
        assert result == pytest.approx(6.2, abs=0.01)

    def test_subtract_positive_numbers(self, calculator):
        """Test subtraction of positive numbers."""
        assert calculator.subtract(10, 5) == 5
        assert calculator.subtract(20, 8) == 12

    def test_subtract_negative_result(self, calculator):
        """Test subtraction resulting in negative number."""
        assert calculator.subtract(5, 10) == -5

    def test_multiply_positive_numbers(self, calculator):
        """Test multiplication of positive numbers."""
        assert calculator.multiply(3, 4) == 12
        assert calculator.multiply(7, 8) == 56

    def test_multiply_by_zero(self, calculator):
        """Test multiplication by zero."""
        assert calculator.multiply(5, 0) == 0
        assert calculator.multiply(0, 10) == 0

    def test_multiply_negative_numbers(self, calculator):
        """Test multiplication with negative numbers."""
        assert calculator.multiply(-3, 4) == -12
        assert calculator.multiply(-5, -2) == 10

    def test_divide_positive_numbers(self, calculator):
        """Test division of positive numbers."""
        assert calculator.divide(10, 2) == 5
        assert calculator.divide(15, 3) == 5

    def test_divide_with_remainder(self, calculator):
        """Test division with remainder."""
        result = calculator.divide(10, 3)
        assert result == pytest.approx(3.33, abs=0.01)

    def test_divide_by_zero_raises_error(self, calculator):
        """Test that division by zero raises ValueError."""
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            calculator.divide(10, 0)

    def test_power_positive_exponent(self, calculator):
        """Test raising to positive power."""
        assert calculator.power(2, 3) == 8
        assert calculator.power(5, 2) == 25

    def test_power_zero_exponent(self, calculator):
        """Test raising to power of zero."""
        assert calculator.power(5, 0) == 1
        assert calculator.power(100, 0) == 1

    def test_power_negative_exponent(self, calculator):
        """Test raising to negative power."""
        assert calculator.power(2, -1) == 0.5
        result = calculator.power(4, -2)
        assert result == pytest.approx(0.0625, abs=0.01)

    def test_square_root_positive_number(self, calculator):
        """Test square root of positive numbers."""
        assert calculator.square_root(4) == 2
        assert calculator.square_root(9) == 3
        assert calculator.square_root(16) == 4

    def test_square_root_zero(self, calculator):
        """Test square root of zero."""
        assert calculator.square_root(0) == 0

    def test_square_root_negative_raises_error(self, calculator):
        """Test that square root of negative number raises ValueError."""
        with pytest.raises(
            ValueError, match="Cannot calculate square root of negative number"
        ):
            calculator.square_root(-4)


class TestCalculatorParametrized:
    """Parametrized tests for Calculator class."""

    @pytest.mark.parametrize(
        "a, b, expected",
        [
            (1, 1, 2),
            (0, 0, 0),
            (-1, 1, 0),
            (100, 200, 300),
            (2.5, 3.5, 6.0),
        ],
    )
    def test_add_parametrized(self, calculator, a, b, expected):
        """Parametrized test for addition."""
        assert calculator.add(a, b) == expected

    @pytest.mark.parametrize(
        "a, b, expected",
        [
            (2, 3, 6),
            (0, 5, 0),
            (-2, 3, -6),
            (4, -2, -8),
            (-3, -3, 9),
        ],
    )
    def test_multiply_parametrized(self, calculator, a, b, expected):
        """Parametrized test for multiplication."""
        assert calculator.multiply(a, b) == expected

    @pytest.mark.parametrize(
        "base, exp, expected",
        [
            (2, 2, 4),
            (3, 3, 27),
            (10, 0, 1),
            (5, 1, 5),
        ],
    )
    def test_power_parametrized(self, calculator, base, exp, expected):
        """Parametrized test for power operation."""
        assert calculator.power(base, exp) == expected
