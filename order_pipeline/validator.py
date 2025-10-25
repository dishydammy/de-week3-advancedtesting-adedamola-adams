import logging
import re
from typing import List, Dict, Any, Optional

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DataValidator:
    """Validates a list of order records."""

    def __init__(self):
        self.required_fields = [
            'order_id', 'timestamp', 'item', 'quantity', 
            'price', 'payment_status', 'total'
        ]
        # Regex to find a valid number (int or float) inside a string
        # It allows for decimal points, and strips common currency/unit symbols
        self.numeric_clean_pattern = re.compile(r"[^0-9\.]")

    def _is_positive_numeric_string(self, value: Any) -> bool:
        """
        Checks if a value is, or can be cleaned to, a positive number.
        Handles strings like "$15.99", "2pcs", "N2000", "N/A".
        """
        if isinstance(value, (int, float)):
            return value > 0

        if not isinstance(value, str):
            return False
        
        # Remove common symbols and letters
        cleaned_value = self.numeric_clean_pattern.sub('', value)
        
        if not cleaned_value:
            return False # Was "N/A" or "usd" etc.

        try:
            numeric_value = float(cleaned_value)
            return numeric_value > 0
        except (ValueError, TypeError):
            return False # Failed to convert

    def _is_field_valid(self, record: Dict[str, Any], field: str) -> bool:
        """Checks if a single field is present and valid."""
        value = record.get(field)
        
        if value is None:
            logging.warning(f"Skipping record (order_id: {record.get('order_id', 'N/A')}): Missing required field '{field}'.")
            return False
        
        # Check for non-empty item string
        if field == 'item' and (not isinstance(value, str) or value.strip() == ""):
            logging.warning(f"Skipping record (order_id: {record.get('order_id', 'N/A')}): Missing or empty required field 'item'.")
            return False

        if field in ['quantity', 'price', 'total']:
            if not self._is_positive_numeric_string(value):
                logging.warning(
                    f"Skipping record (order_id: {record.get('order_id', 'N/A')}): "
                    f"Invalid or non-positive value for '{field}': {value}"
                )
                return False
        
        return True

    def validate_data(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Filters a list of records, returning only valid ones.

        A record is valid if:
        1. All required fields are present.
        2. 'quantity', 'price', and 'total' are positive numeric values.
        """
        validated_data = []
        for record in data:
            is_valid = True
            for field in self.required_fields:
                if not self._is_field_valid(record, field):
                    is_valid = False
                    break  # Stop checking this record
            
            if is_valid:
                validated_data.append(record)
        
        logging.info(f"Validation complete. Passed: {len(validated_data)} / Original: {len(data)}")
        return validated_data

