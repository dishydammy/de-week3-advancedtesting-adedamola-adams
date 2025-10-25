import logging
import re
from typing import List, Dict, Any
from dateutil.parser import parse as parse_datetime

class DataTransformer:
    """Transforms and cleans validated order data."""

    _valid_statuses = {'paid', 'pending', 'refunded'}
    _numeric_extract_pattern = re.compile(r"(\d+(\.\d+)?)")

    @staticmethod
    def _clean_numeric_string(value: Any) -> float:
        """Cleans a string and returns a float. Returns 0.0 if conversion fails."""
        if isinstance(value, (int, float)):
            return float(value)
        
        if not isinstance(value, str):
            return 0.0

        match = DataTransformer._numeric_extract_pattern.search(value)
        if match:
            try:
                return float(match.group(1))
            except (ValueError, TypeError):
                return 0.0
        return 0.0

    @staticmethod
    def _normalize_status(status: Any) -> str:
        """Normalizes the payment_status field."""
        if not isinstance(status, str):
            return 'pending'
        
        normalized = status.strip().lower()
        
        if normalized not in DataTransformer._valid_statuses:
            if 'paid' in normalized:
                return 'paid'
            if 'refund' in normalized:
                return 'refunded'
            return 'pending'
        return normalized

    @staticmethod
    def _clean_text(text: Any) -> str:
        """Cleans a single text field."""
        if not isinstance(text, str):
            return ""
        cleaned = text.strip()
        if cleaned:
            return cleaned[0].upper() + cleaned[1:].lower()
        return ""

    @staticmethod
    def _parse_timestamp(timestamp: Any) -> str:
        """Parses various datetime formats into a standard ISO string."""
        if not isinstance(timestamp, str) or not timestamp:
            return ""
        try:
            # dateutil.parser is very flexible
            dt = parse_datetime(timestamp)
            return dt.isoformat()
        except Exception as e:
            logging.warning(f"Could not parse timestamp '{timestamp}': {e}")
            return ""

    def transform_data(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Transforms a list of validated order records.
        
        Transformations:
        1. Converts 'quantity', 'price', 'total' to numeric.
        2. Normalizes 'payment_status' to lowercase.
        3. Cleans text fields ('item', 'order_id').
        4. Recalculates 'total' as quantity * price for consistency.
        5. Parses and standardizes 'timestamp'.
        """
        transformed_data = []
        for record in data:
            try:
                transformed_record = record.copy()
                
                quantity = self._clean_numeric_string(transformed_record['quantity'])
                price = self._clean_numeric_string(transformed_record['price'])
                orig_qty_val = str(transformed_record.get('quantity', '')).strip()
                if quantity == 0.0 and orig_qty_val not in ('0', '0.0'):
                    logging.warning(
                        f"Skipping record {record.get('order_id', 'N/A')} due to "
                        f"unparseable quantity: {orig_qty_val}"
                    )
                    continue

                orig_price_val = str(transformed_record.get('price', '')).strip()
                if price == 0.0 and orig_price_val not in ('0', '0.0'):
                    logging.warning(
                        f"Skipping record {record.get('order_id', 'N/A')} due to "
                        f"unparseable price: {orig_price_val}"
                    )
                    continue

                transformed_record['payment_status'] = self._normalize_status(transformed_record['payment_status'])
                transformed_record['item'] = self._clean_text(transformed_record['item'])
                transformed_record['order_id'] = str(transformed_record['order_id']).strip()
                
                recalculated_total = round(quantity * price, 2)
                
                original_total = self._clean_numeric_string(transformed_record['total'])
                if original_total != recalculated_total:
                    logging.debug(
                        f"Correcting total for order_id {transformed_record['order_id']}: "
                        f"Original={original_total}, New={recalculated_total}"
                    )
                
                transformed_record['quantity'] = quantity
                transformed_record['price'] = price
                transformed_record['total'] = recalculated_total
                transformed_record['timestamp'] = self._parse_timestamp(transformed_record['timestamp'])

                transformed_data.append(transformed_record)
                
            except Exception as e:
                logging.error(f"Error transforming record {record.get('order_id', 'N/A')}: {e}")
                continue
                
        logging.info(f"Transformation complete. Processed {len(transformed_data)} records.")
        return transformed_data


