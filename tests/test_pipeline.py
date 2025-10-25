import pytest
import json
from pathlib import Path
from order_pipeline.pipeline import OrderPipeline

# Fixture to create a sample raw JSON file for the integration test
@pytest.fixture
def raw_data_file(tmp_path):
    """Creates a sample shoplink.json file in a temporary directory."""
    raw_data = [
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
        # 8. Valid (price/total with "N", wrong total)
        {
            "order_id": "ORD008", "timestamp": "2025-10-19T08:35:00Z", "item": "Charger",
            "quantity": 2, "price": "N4500", "total": "N10000", "payment_status": "pending"
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
    
    input_file = tmp_path / "test_input.json"
    with open(input_file, 'w') as f:
        json.dump(raw_data, f)
        
    return input_file

class TestOrderPipelineIntegration:

    def test_full_pipeline_run(self, raw_data_file, tmp_path):
        """
        Integration test for the entire pipeline.
        It runs the pipeline from file read to file export and verifies
        the final output file.
        """
        output_file = tmp_path / "test_output.json"
        
        # 1. Run the pipeline
        pipeline = OrderPipeline()
        pipeline.run(str(raw_data_file), str(output_file))
        
        # 2. Verify the output file exists
        assert output_file.exists()
        
        # 3. Load and verify the contents of the output file
        with open(output_file, 'r') as f:
            results = json.load(f)
            
        # 3a. Verify analysis summary
        analysis = results.get("analysis_summary")
        assert analysis is not None
        
        # Total Revenue: 31.98 (ORD001) + 12.50 (ORD002) + 6000 (ORD006) = 6044.48
        assert analysis["total_revenue"] == 6044.48
        assert analysis["total_orders"] == 5 # ORD001, 002, 006, 008, 010
        assert analysis["average_revenue"] == pytest.approx(6044.48 / 5)
        assert analysis["status_counts"] == {"paid": 3, "pending": 1, "refunded": 1}

        # 3b. Verify cleaned data
        cleaned_data = results.get("cleaned_data")
        assert cleaned_data is not None
        assert len(cleaned_data) == 5 # 5 valid records passed
        
        # Map data for easier checking
        data_map = {r['order_id']: r for r in cleaned_data}
        
        # Check ORD001
        r1 = data_map["ORD001"]
        assert r1["item"] == "Wireless mouse"
        assert r1["payment_status"] == "paid"
        assert r1["price"] == 15.99
        assert r1["total"] == 31.98
        assert "2025-10-19T08:00:00" in r1["timestamp"]
        
        # Check ORD002
        r2 = data_map["ORD002"]
        assert r2["item"] == "Laptop sleeve"
        assert r2["payment_status"] == "paid"
        assert r2["price"] == 12.50
        assert r2["total"] == 12.50
        assert r2["timestamp"] == "2025-10-19T08:05:00"

        # Check ORD006
        r3 = data_map["ORD006"]
        assert r3["item"] == "Phone case"
        assert r3["payment_status"] == "paid"
        assert r3["price"] == 2000.0
        assert r3["total"] == 6000.0
        assert "2025-10-19T08:25:00" in r3["timestamp"]

        # Check ORD008 (total recalculated)
        r4 = data_map["ORD008"]
        assert r4["item"] == "Charger"
        assert r4["payment_status"] == "pending"
        assert r4["price"] == 4500.0
        assert r4["total"] == 9000.0 # Recalculated from 10000

        # Check ORD010
        r5 = data_map["ORD010"]
        assert r5["item"] == "Mouse pad"
        assert r5["payment_status"] == "refunded"
        assert r5["price"] == 3.0
        assert r5["total"] == 15.0
        assert "2025-10-19T08:45:00" in r5["timestamp"]

    def test_pipeline_run_with_no_valid_data(self, tmp_path):
        """Tests pipeline run where validator filters out all records."""
        # Create a file with only invalid data
        invalid_data = [
            {"order_id": "ORD003", "quantity": -3, "price": "5usd", "total": 15, "payment_status": "pending", "item": "USB Cable", "timestamp": "..."},
            {"order_id": "ORD004", "quantity": "2pcs", "price": "$16", "total": "$32.00", "payment_status": "paid", "item": "Mouse", "timestamp": "..."},
            {"order_id": "ORD005", "item": "", "quantity": 1, "price": "45", "total": 45, "payment_status": "refunded", "timestamp": "..."},
            {"order_id": "ORD007", "quantity": "N/A", "price": "$25", "total": "$50", "payment_status": "Paid", "item": "Power Bank", "timestamp": "..."},
            {"order_id": "ORD009", "quantity": 1, "price": "$29.99", "payment_status": "PAID", "item": "Webcam", "timestamp": "..."} # Missing total
        ]
        input_file = tmp_path / "invalid_input.json"
        output_file = tmp_path / "invalid_output.json"
        
        with open(input_file, 'w') as f:
            json.dump(invalid_data, f)
            
        pipeline = OrderPipeline()
        pipeline.run(str(input_file), str(output_file))
        
        # The output file should not be created because the pipeline should stop.
        assert not output_file.exists()

    def test_pipeline_run_with_reader_error(self, tmp_path):
        """Tests pipeline run where the input file is missing."""
        input_file = "non_existent.json"
        output_file = tmp_path / "output.json"
        
        pipeline = OrderPipeline()
        pipeline.run(input_file, str(output_file))
        
        # No output file should be created
        assert not output_file.exists()

