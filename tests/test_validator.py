import pytest
from order_pipeline.validator import DataValidator

@pytest.fixture
def validator():
    """Returns a DataValidator instance."""
    return DataValidator()

# Updated sample data for tests
@pytest.fixture
def sample_data():
    """Provides sample data for validation tests based on new JSON."""
    return [
        # 1. Valid (price/total with $)
        {
            "order_id": "ORD001", "timestamp": "2025-10-19T08:00:00Z", "item": "Wireless Mouse",
            "quantity": 2, "price": "$15.99", "total": "$31.98", "payment_status": "paid"
        },
        # 2. Valid (string numbers)
        {
            "order_id": "ORD002", "timestamp": "2025-10-19 08:05", "item": "Laptop Sleeve",
            "quantity": "1", "price": "12.50", "total": "12.50", "payment_status": "PAID"
        },
        # 3. Invalid (negative quantity)
        {
            "order_id": "ORD003", "timestamp": "19/10/2025 08:10 AM", "item": "USB Cable",
            "quantity": -3, "price": "5usd", "total": 15, "payment_status": "pending"
        },
        # 4. Invalid (quantity with "pcs")
        {
            "order_id": "ORD004", "timestamp": "2025-10-19T08:15:00Z", "item": "Wireless Mouse",
            "quantity": "2pcs", "price": "$16", "total": "$32.00", "payment_status": "paid"
        },
        # 5. Invalid (empty item)
        {
            "order_id": "ORD005", "timestamp": "2025-10-19T08:20:00Z", "item": "",
            "quantity": 1, "price": "45 dollars", "total": 45, "payment_status": "refunded"
        },
        # 6. Valid (price/total with "N")
        {
            "order_id": "ORD006", "timestamp": "2025/10/19T08:25Z", "item": "Phone Case",
            "quantity": 3, "price": "N2000", "total": "N6000", "payment_status": "PAID"
        },
        # 7. Invalid (quantity "N/A")
        {
            "order_id": "ORD007", "timestamp": "2025-10-19T08:30:00Z", "item": "Power Bank",
            "quantity": "N/A", "price": "$25", "total": "$50", "payment_status": "Paid"
        },
        # 8. Valid (price/total with "N")
        {
            "order_id": "ORD008", "timestamp": "2025-10-19T08:35:00Z", "item": "Charger",
            "quantity": 2, "price": "N4500", "total": "N9000", "payment_status": "pending"
        },
        # 9. Invalid (missing total)
        {
            "order_id": "ORD009", "timestamp": "2025-10-19T08:40:00Z", "item": "Webcam",
            "quantity": 1, "price": "$29.99", "payment_status": "PAID"
        },
        # 10. Valid (all clean)
        {
            "order_id": "ORD010", "timestamp": "2025-10-19T08:45:00Z", "item": "Mouse Pad",
            "quantity": 5, "price": 3, "total": 15, "payment_status": "refunded"
        }
    ]

class TestDataValidator:

    def test_validate_data(self, validator, sample_data):
        """Tests the main validation logic."""
        validated_data = validator.validate_data(sample_data)
        
        # Should pass: ORD001, ORD002, ORD006, ORD008, ORD010
        assert len(validated_data) == 5
        
        validated_ids = {r['order_id'] for r in validated_data}
        assert "ORD001" in validated_ids # Valid (with $)
        assert "ORD002" in validated_ids # Valid (string nums)
        assert "ORD006" in validated_ids # Valid (with N)
        assert "ORD008" in validated_ids # Valid (with N)
        assert "ORD010" in validated_ids # Valid (clean)

        assert "ORD003" not in validated_ids # Negative quantity
        assert "ORD004" not in validated_ids # "2pcs"
        assert "ORD005" not in validated_ids # Empty item
        assert "ORD007" not in validated_ids # "N/A"
        assert "ORD009" not in validated_ids # Missing total

    def test_empty_input(self, validator):
        """Tests that empty input data returns an empty list."""
        assert validator.validate_data([]) == []

    def test_all_invalid_data(self, validator, sample_data):
        """Tests that a list with only invalid records returns an empty list."""
        invalid_only = [
            sample_data[2], sample_data[3], sample_data[4], 
            sample_data[6], sample_data[8]
        ]
        assert validator.validate_data(invalid_only) == []
    
    def test_all_valid_data(self, validator, sample_data):
        """Tests that a list with only valid records returns the same list."""
        valid_only = [
            sample_data[0], sample_data[1], sample_data[5], 
            sample_data[7], sample_data[9]
        ]
        result = validator.validate_data(valid_only)
        assert len(result) == 5
        assert result == valid_only

    def test_internal_is_positive_numeric_string(self, validator):
        """Unit test for the _is_positive_numeric_string helper."""
        assert validator._is_positive_numeric_string(10) == True
        assert validator._is_positive_numeric_string(10.5) == True
        assert validator._is_positive_numeric_string("10.5") == True
        assert validator._is_positive_numeric_string("$15.99") == True
        assert validator._is_positive_numeric_string("N2000") == True
        assert validator._is_positive_numeric_string("45 dollars") == False # Changed
        
        assert validator._is_positive_numeric_string(0) == False
        assert validator._is_positive_numeric_string(-3) == False
        assert validator._is_positive_numeric_string("-3") == False # Changed
        assert validator._is_positive_numeric_string("2pcs") == False # Changed
        assert validator._is_positive_numeric_string("5usd") == False # Changed
        
        assert validator._is_positive_numeric_string("N/A") == False
        assert validator._is_positive_numeric_string("abc") == False
        assert validator._is_positive_numeric_string(None) == False


