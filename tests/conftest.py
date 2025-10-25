"""
Test configuration and fixtures.
"""

import pytest
from src.calculator.operations import Calculator
from src.calculator.data_processor import DataProcessor


@pytest.fixture
def calculator():
    """Fixture that provides a Calculator instance."""
    return Calculator()


@pytest.fixture
def data_processor():
    """Fixture that provides a DataProcessor instance."""
    return DataProcessor()


@pytest.fixture
def sample_numbers():
    """Fixture that provides sample numbers for testing."""
    return [1, 2, 3, 4, 5, -1, -2, 0]


@pytest.fixture
def sample_dict():
    """Fixture that provides a sample dictionary for testing."""
    return {"a": 10, "b": 20, "c": 5, "d": 15}
