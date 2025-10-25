import pytest
import json
from order_pipeline.exporter import DataExporter

@pytest.fixture
def exporter():
    """Returns a DataExporter instance."""
    return DataExporter()

@pytest.fixture
def sample_data_to_export():
    """Provides sample cleaned data and analysis for export."""
    cleaned_data = [
        {"order_id": "ORD100", "item": "Laptop", "total": 1200.00, "payment_status": "paid"}
    ]
    analysis = {
        "total_revenue": 1200.00,
        "average_revenue": 1200.00,
        "total_orders": 1,
        "status_counts": {"paid": 1, "pending": 0, "refunded": 0}
    }
    return cleaned_data, analysis

class TestDataExporter:

    def test_export_data(self, exporter, sample_data_to_export, tmp_path):
        """Tests successful data export."""
        cleaned_data, analysis = sample_data_to_export
        output_file = tmp_path / "output.json"
        
        exporter.export_data(cleaned_data, analysis, str(output_file))
        
        # Check file exists
        assert output_file.exists()
        
        # Check file content
        with open(output_file, 'r') as f:
            content = json.load(f)
            
        assert "analysis_summary" in content
        assert "cleaned_data" in content
        assert content["analysis_summary"]["total_revenue"] == 1200.00
        assert len(content["cleaned_data"]) == 1
        assert content["cleaned_data"][0]["order_id"] == "ORD100"

    def test_export_unsupported_format(self, exporter, sample_data_to_export):
        """Tests that exporting to a non-json file raises ValueError."""
        cleaned_data, analysis = sample_data_to_export
        with pytest.raises(ValueError, match="Export file must be a .json file"):
            exporter.export_data(cleaned_data, analysis, "output.txt")

    def test_export_no_permission(self, exporter, sample_data_to_export, monkeypatch):
        """
        Tests export failure due to file system error (e.g., permissions).
        We simulate this by patching 'open' to raise an IOError.
        """
        def mock_open(*args, **kwargs):
            raise IOError("Permission denied")

        # Temporarily replace the built-in 'open' with our mock
        monkeypatch.setattr("builtins.open", mock_open)
        
        cleaned_data, analysis = sample_data_to_export
        
        with pytest.raises(IOError, match="Permission denied"):
            exporter.export_data(cleaned_data, analysis, "locked_dir/output.json")

    def test_export_non_serializable_data(self, exporter, tmp_path):
        """Tests that a TypeError is raised for non-serializable data."""
        # 'bytes' are not JSON serializable by default
        cleaned_data = [{"order_id": "ORD100", "data": b"some-bytes"}]
        analysis = {"total_revenue": 0}
        output_file = tmp_path / "invalid.json"

        with pytest.raises(TypeError, match="Object of type bytes is not JSON serializable"):
            exporter.export_data(cleaned_data, analysis, str(output_file))

