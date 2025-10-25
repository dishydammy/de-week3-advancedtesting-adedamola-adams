"""
Unit tests for DataProcessor.
"""

import pytest


class TestDataProcessor:
    """Test suite for DataProcessor class."""

    def test_filter_positive_numbers(self, data_processor, sample_numbers):
        """Test filtering positive numbers."""
        result = data_processor.filter_positive_numbers(sample_numbers)
        assert result == [1, 2, 3, 4, 5]

    def test_filter_positive_numbers_empty_list(self, data_processor):
        """Test filtering with empty list."""
        result = data_processor.filter_positive_numbers([])
        assert result == []

    def test_filter_positive_numbers_all_negative(self, data_processor):
        """Test filtering when all numbers are negative."""
        result = data_processor.filter_positive_numbers([-1, -2, -3, -4])
        assert result == []

    def test_filter_positive_numbers_all_positive(self, data_processor):
        """Test filtering when all numbers are positive."""
        numbers = [1, 2, 3, 4, 5]
        result = data_processor.filter_positive_numbers(numbers)
        assert result == numbers

    def test_calculate_average_normal_list(self, data_processor):
        """Test calculating average of normal list."""
        result = data_processor.calculate_average([1, 2, 3, 4, 5])
        assert result == 3.0

    def test_calculate_average_single_element(self, data_processor):
        """Test calculating average of single element."""
        result = data_processor.calculate_average([42])
        assert result == 42.0

    def test_calculate_average_negative_numbers(self, data_processor):
        """Test calculating average with negative numbers."""
        result = data_processor.calculate_average([-1, -2, -3, -4])
        assert result == -2.5

    def test_calculate_average_empty_list_raises_error(self, data_processor):
        """Test that empty list raises ValueError."""
        with pytest.raises(ValueError, match="Cannot calculate average of empty list"):
            data_processor.calculate_average([])

    def test_find_max_value_normal_dict(self, data_processor, sample_dict):
        """Test finding max value in dictionary."""
        result = data_processor.find_max_value(sample_dict)
        assert result == 20

    def test_find_max_value_empty_dict(self, data_processor):
        """Test finding max value in empty dictionary."""
        result = data_processor.find_max_value({})
        assert result is None

    def test_find_max_value_single_item(self, data_processor):
        """Test finding max value with single item."""
        result = data_processor.find_max_value({"a": 42})
        assert result == 42

    def test_find_max_value_negative_numbers(self, data_processor):
        """Test finding max value with negative numbers."""
        result = data_processor.find_max_value({"a": -10, "b": -5, "c": -20})
        assert result == -5

    def test_group_by_range_default_range(self, data_processor):
        """Test grouping numbers with default range size."""
        numbers = [5, 15, 25, 8, 22, 35]
        result = data_processor.group_by_range(numbers)
        assert "0-10" in result
        assert "10-20" in result
        assert "20-30" in result
        assert "30-40" in result
        assert 5 in result["0-10"]
        assert 8 in result["0-10"]
        assert 15 in result["10-20"]

    def test_group_by_range_custom_range(self, data_processor):
        """Test grouping numbers with custom range size."""
        numbers = [5, 10, 15, 20, 25]
        result = data_processor.group_by_range(numbers, range_size=5)
        assert "5-10" in result
        assert "10-15" in result
        assert "15-20" in result
        assert "20-25" in result
        assert "25-30" in result

    def test_group_by_range_empty_list(self, data_processor):
        """Test grouping empty list."""
        result = data_processor.group_by_range([])
        assert result == {}


class TestDataProcessorParametrized:
    """Parametrized tests for DataProcessor."""

    @pytest.mark.parametrize(
        "numbers, expected",
        [
            ([1, 2, 3], [1, 2, 3]),
            ([-1, -2, -3], []),
            ([0, 1, -1], [1]),
            ([5, -5, 10, -10], [5, 10]),
        ],
    )
    def test_filter_positive_parametrized(self, data_processor, numbers, expected):
        """Parametrized test for filtering positive numbers."""
        result = data_processor.filter_positive_numbers(numbers)
        assert result == expected

    @pytest.mark.parametrize(
        "numbers, expected_avg",
        [
            ([1, 2, 3, 4, 5], 3.0),
            ([10, 20, 30], 20.0),
            ([100], 100.0),
            ([-10, 10], 0.0),
        ],
    )
    def test_calculate_average_parametrized(
        self, data_processor, numbers, expected_avg
    ):
        """Parametrized test for calculating average."""
        result = data_processor.calculate_average(numbers)
        assert result == expected_avg
