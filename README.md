# Data Engineering Week 3 - Advanced Testing with Python

[![Python Testing CI](https://github.com/dishydammy/de-week3-advancedtesting-adedamola-adams/actions/workflows/test.yml/badge.svg)](https://github.com/dishydammy/de-week3-advancedtesting-adedamola-adams/actions/workflows/test.yml)

A comprehensive Python project demonstrating advanced testing techniques including unit testing, parametrized tests, fixtures, and test coverage.

## Project Structure

```
.
├── src/
│   └── calculator/
│       ├── __init__.py
│       ├── operations.py       # Basic calculator operations
│       └── data_processor.py   # Data processing utilities
├── tests/
│   ├── conftest.py            # Test fixtures and configuration
│   ├── test_operations.py     # Tests for calculator operations
│   └── test_data_processor.py # Tests for data processor
├── pyproject.toml             # Project configuration
├── requirements.txt           # Project dependencies
└── README.md
```

## Features

- **Calculator Operations**: Basic arithmetic operations (add, subtract, multiply, divide, power, square root)
- **Data Processing**: Utilities for filtering, averaging, and grouping data
- **Comprehensive Testing**: Unit tests, parametrized tests, and fixtures
- **Code Coverage**: Full test coverage reporting
- **CI/CD**: Automated testing with GitHub Actions
- **Code Quality**: Linting with flake8, formatting with black, type checking with mypy

## Setup

### Prerequisites

- Python 3.8 or higher
- pip

### Installation

1. Clone the repository:
```bash
git clone https://github.com/dishydammy/de-week3-advancedtesting-adedamola-adams.git
cd de-week3-advancedtesting-adedamola-adams
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running Tests

### Run all tests:
```bash
pytest
```

### Run tests with coverage:
```bash
pytest --cov=src --cov-report=term-missing
```

### Run tests with verbose output:
```bash
pytest -v
```

### Run specific test file:
```bash
pytest tests/test_operations.py
```

### Run specific test:
```bash
pytest tests/test_operations.py::TestCalculator::test_add_positive_numbers
```

## Code Quality

### Format code with black:
```bash
black src tests
```

### Check code style with flake8:
```bash
flake8 src tests
```

### Type check with mypy:
```bash
mypy src
```

## Usage Examples

### Calculator Operations

```python
from src.calculator.operations import Calculator

calc = Calculator()

# Basic operations
result = calc.add(5, 3)        # Returns 8
result = calc.subtract(10, 4)  # Returns 6
result = calc.multiply(3, 7)   # Returns 21
result = calc.divide(15, 3)    # Returns 5.0
result = calc.power(2, 3)      # Returns 8
result = calc.square_root(16)  # Returns 4.0
```

### Data Processing

```python
from src.calculator.data_processor import DataProcessor

processor = DataProcessor()

# Filter positive numbers
numbers = [1, -2, 3, -4, 5]
positive = processor.filter_positive_numbers(numbers)  # Returns [1, 3, 5]

# Calculate average
avg = processor.calculate_average([1, 2, 3, 4, 5])  # Returns 3.0

# Find max value in dictionary
data = {"a": 10, "b": 20, "c": 5}
max_val = processor.find_max_value(data)  # Returns 20

# Group numbers by range
numbers = [5, 15, 25, 8, 22]
groups = processor.group_by_range(numbers, range_size=10)
# Returns {'0-10': [5, 8], '10-20': [15], '20-30': [25, 22]}
```

## Testing Techniques Demonstrated

1. **Unit Testing**: Individual test methods for each function
2. **Parametrized Tests**: Using `@pytest.mark.parametrize` for testing multiple inputs
3. **Fixtures**: Reusable test data and object instances
4. **Exception Testing**: Testing error conditions with `pytest.raises`
5. **Approximate Comparisons**: Using `pytest.approx` for floating-point comparisons
6. **Test Coverage**: Measuring code coverage with pytest-cov
7. **Test Organization**: Grouping tests into classes

## CI/CD

The project includes a GitHub Actions workflow that:
- Tests against multiple Python versions (3.8, 3.9, 3.10, 3.11)
- Runs linting checks (flake8)
- Checks code formatting (black)
- Performs type checking (mypy)
- Runs all tests with coverage reporting
- Uploads coverage reports to Codecov

## License

This project is for educational purposes.
