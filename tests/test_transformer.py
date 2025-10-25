import pytest
from order_pipeline.transformer import DataTransformer

@pytest.fixture
def transformer():
    """Returns a DataTransformer instance."""
    return DataTransformer()

@pytest.fixture
def valid_data():
    """Provides validated data for transformation tests."""
    return [
        # 1. Valid (price/total with $)
        {
            "order_id": "ORD001", "timestamp": "2025-10-19T08:00:00Z", "item": "Wireless Mouse",
            "quantity": 2, "price": "$15.99", "total": "$31.98", "payment_status": "paid"
        },
        # 2. Valid (string numbers, different timestamp)
        {
            "order_id": "ORD002", "timestamp": "2025-10-19 08:05", "item": "Laptop Sleeve",
            "quantity": "1", "price": "12.50", "total": "12.50", "payment_status": "PAID"
        },
        # 3. Valid (price/total with "N", different timestamp)
        {
            "order_id": "ORD006", "timestamp": "2025/10/19T08:25Z", "item": "Phone Case",
            "quantity": 3, "price": "N2000", "total": "N6000", "payment_status": "PAID"
        },
        # 4. Valid (price/total with "N", wrong total)
        {
            "order_id": "ORD008", "timestamp": "2025-10-19T08:35:00Z", "item": "Charger",
            "quantity": 2, "price": "N4500", "total": "N10000", "payment_status": "pending" # Should be 9000
        },
        # 5. Valid (all clean, different timestamp)
        {
            "order_id": "ORD010", "timestamp": "19/10/2025 08:45 AM", "item": "Mouse Pad",
            "quantity": 5, "price": 3, "total": 15, "payment_status": "refunded"
        },
        # 6. Record with non-numeric quantity (should fail transformation)
        {
            "order_id": "ORD109", "timestamp": "2025-01-15T10:45:00Z", "item": "Desk",
            "quantity": "one", "price": 150.00, "payment_status": "paid", "total": 150.00
        }
    ]

class TestDataTransformer:

    def test_transform_data(self, transformer, valid_data):
        """Tests the main transformation logic."""
        transformed_data = transformer.transform_data(valid_data)
        
        # Record 6 (ORD109) should fail and be skipped
        assert len(transformed_data) == 5
        
        # Check transformed data by order_id
        transformed_map = {r['order_id']: r for r in transformed_data}
        
        # Test 1 (ORD001): Cleaning $, timestamp
        r1 = transformed_map["ORD001"]
        assert r1['item'] == "Wireless mouse"
        assert r1['quantity'] == 2.0
        assert r1['price'] == 15.99
        assert r1['total'] == 31.98 # 2 * 15.99
        assert "2025-10-19T08:00:00" in r1['timestamp']

        # Test 2 (ORD002): Type conversion, status, timestamp
        r2 = transformed_map["ORD002"]
        assert r2['item'] == "Laptop sleeve"
        assert r2['quantity'] == 1.0
        assert r2['price'] == 12.50
        assert r2['payment_status'] == "paid"
        assert r2['total'] == 12.50
        assert r2['timestamp'] == "2025-10-19T08:05:00"
        
        # Test 3 (ORD006): Cleaning N, status, timestamp
        r3 = transformed_map["ORD006"]
        assert r3['item'] == "Phone case"
        assert r3['quantity'] == 3.0
        assert r3['price'] == 2000.0
        assert r3['payment_status'] == "paid"
        assert r3['total'] == 6000.0 # 3 * 2000
        assert "2025-10-19T08:25:00" in r3['timestamp']

        # Test 4 (ORD008): Cleaning N, recalculate total
        r4 = transformed_map["ORD008"]
        assert r4['item'] == "Charger"
        assert r4['quantity'] == 2.0
        assert r4['price'] == 4500.0
        assert r4['payment_status'] == "pending"
        assert r4['total'] == 9000.0 # 2 * 4500, not 10000

        # Test 5 (ORD010): Clean, timestamp AM/PM
        r5 = transformed_map["ORD010"]
        assert r5['item'] == "Mouse pad"
        assert r5['payment_status'] == "refunded"
        assert r5['total'] == 15.0
        assert r5['timestamp'] == "2025-10-19T08:45:00"

    def test_empty_input(self, transformer):
        """Tests that empty input data returns an empty list."""
        assert transformer.transform_data([]) == []

    def test_internal_normalize_status(self, transformer):
        """Unit test for the _normalize_status helper."""
        assert transformer._normalize_status(" PAID ") == "paid"
        assert transformer._normalize_status("Pending") == "pending"
        assert transformer._normalize_status("refunded") == "refunded"
        assert transformer._normalize_status("RefUND") == "refunded"
        assert transformer._normalize_status("Completed (Paid)") == "paid"
        assert transformer._normalize_status("SHIPPED") == "pending"
        assert transformer._normalize_status(None) == "pending"
        assert transformer._normalize_status(123) == "pending"

    def test_internal_clean_text(self, transformer):
        """Unit test for the _clean_text helper."""
        assert transformer._clean_text("  my item ") == "My item"
        assert transformer._clean_text("ALL CAPS") == "All caps"
        assert transformer._clean_text("already good") == "Already good"
        assert transformer._clean_text(123) == ""
        assert transformer._clean_text(None) == ""
        assert transformer._clean_text(" ") == ""
    
    def test_internal_clean_numeric_string(self, transformer):
        """Unit test for the _clean_numeric_string helper."""
        assert transformer._clean_numeric_string(10.5) == 10.5
        assert transformer._clean_numeric_string("$15.99") == 15.99
        assert transformer._clean_numeric_string("N2000") == 2000.0
        assert transformer._clean_numeric_string("45 dollars") == 45.0
        assert transformer._clean_numeric_string("2pcs") == 2.0
        assert transformer._clean_numeric_string("5usd") == 5.0
        assert transformer._clean_numeric_string("N/A") == 0.0
        assert transformer._clean_numeric_string("abc") == 0.0
        assert transformer._clean_numeric_string(None) == 0.0

    def test_internal_parse_timestamp(self, transformer):
        """Unit test for the _parse_timestamp helper."""
        assert transformer._parse_timestamp("2025-10-19T08:00:00Z") == "2025-10-19T08:00:00+00:00"
        assert transformer._parse_timestamp("2025-10-19 08:05") == "2025-10-19T08:05:00"
        assert transformer._parse_timestamp("19/10/2025 08:10 AM") == "2025-10-19T08:10:00"
        assert transformer._parse_timestamp("2025/10/19T08:25Z") == "2025-10-19T08:25:00+00:00"
        assert transformer._parse_timestamp("invalid-date") == ""
        assert transformer._parse_timestamp(None) == ""

