"""
Data processing utilities for demonstrating testing patterns.
"""

from typing import Dict, List, Optional, Union


class DataProcessor:
    """A class for processing and analyzing data."""

    def filter_positive_numbers(
        self, numbers: List[Union[int, float]]
    ) -> List[Union[int, float]]:
        """
        Filter out negative numbers from a list.

        Args:
            numbers: List of numbers

        Returns:
            List containing only positive numbers
        """
        return [n for n in numbers if n > 0]

    def calculate_average(self, numbers: List[Union[int, float]]) -> float:
        """
        Calculate the average of a list of numbers.

        Args:
            numbers: List of numbers

        Returns:
            Average of the numbers

        Raises:
            ValueError: If the list is empty
        """
        if not numbers:
            raise ValueError("Cannot calculate average of empty list")
        return sum(numbers) / len(numbers)

    def find_max_value(self, data: Dict[str, Union[int, float]]) -> Optional[float]:
        """
        Find the maximum value in a dictionary.

        Args:
            data: Dictionary with numeric values

        Returns:
            Maximum value or None if empty
        """
        if not data:
            return None
        return max(data.values())

    def group_by_range(
        self, numbers: List[Union[int, float]], range_size: int = 10
    ) -> Dict[str, List[Union[int, float]]]:
        """
        Group numbers into ranges.

        Args:
            numbers: List of numbers to group
            range_size: Size of each range

        Returns:
            Dictionary with range labels as keys and lists of numbers as values
        """
        groups: Dict[str, List[Union[int, float]]] = {}
        for num in numbers:
            range_start = (int(num) // range_size) * range_size
            range_end = range_start + range_size
            key = f"{range_start}-{range_end}"
            if key not in groups:
                groups[key] = []
            groups[key].append(num)
        return groups
