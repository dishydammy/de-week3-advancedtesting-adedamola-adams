import pytest
import json
import os
from order_pipeline.reader import DataReader

# Fixture to create temporary test files
@pytest.fixture
def temp_file(tmp_path):
    """A fixture to create temporary files for testing."""
    files = {}
    
    def _create_file(filename, content):
        file_path = tmp_path / filename
        if content is not None:
            file_path.write_text(content)
        else:
            # Create an empty file
            open(file_path, 'w').close()
        files[filename] = file_path
        return file_path

    yield _create_file
    
    # Teardown (not strictly needed with tmp_path, but good practice)
    for file in files.values():
        if os.path.exists(file):
            os.remove(file)

class TestDataReader:

    def test_read_valid_json(self, temp_file):
        """Tests reading a valid JSON file."""
        content = json.dumps([{"id": 1, "item": "test"}])
        json_file = temp_file("valid.json", content)
        
        reader = DataReader()
        data = reader.read_json_data(str(json_file))
        
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["id"] == 1

    def test_read_unsupported_format(self):
        """Tests that a non-json file raises ValueError."""
        reader = DataReader()
        with pytest.raises(ValueError, match="Unsupported file format"):
            reader.read_json_data("test.txt")

    def test_read_file_not_found(self):
        """Tests that a missing file raises FileNotFoundError."""
        reader = DataReader()
        with pytest.raises(FileNotFoundError):
            reader.read_json_data("non_existent_file.json")

    def test_read_empty_file(self, temp_file):
        """Tests that an empty file raises ValueError."""
        empty_file = temp_file("empty.json", None) # Creates empty file
        
        reader = DataReader()
        with pytest.raises(ValueError, match="File is empty"):
            reader.read_json_data(str(empty_file))

    def test_read_malformed_json(self, temp_file):
        """Tests that malformed JSON raises ValueError."""
        malformed_file = temp_file("malformed.json", '{"id": 1, "item": "test"')
        
        reader = DataReader()
        with pytest.raises(ValueError, match="Failed to decode JSON"):
            reader.read_json_data(str(malformed_file))

    def test_read_json_not_a_list(self, temp_file):
        """Tests JSON that is a valid object but not a list."""
        content = json.dumps({"id": 1, "item": "test"})
        json_file = temp_file("object.json", content)
        
        reader = DataReader()
        with pytest.raises(ValueError, match="JSON content is not a list"):
            reader.read_json_data(str(json_file))

    def test_read_empty_list_json(self, temp_file):
        """Tests JSON file containing just an empty list."""
        content = json.dumps([])
        json_file = temp_file("empty_list.json", content)
        
        reader = DataReader()
        with pytest.raises(ValueError, match="File contains an empty list"):
            reader.read_json_data(str(json_file))
