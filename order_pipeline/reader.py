import json
import os
from typing import List, Dict, Any

class DataReader:
    """Reads order data from a JSON file."""

    def read_json_data(self, filepath: str) -> List[Dict[str, Any]]:
        """
        Reads data from a JSON file.

        Args:
            filepath: The path to the JSON file.

        Returns:
            A list of dictionaries, where each dictionary is an order record.

        Raises:
            ValueError: If the file is not a .json file, is empty,
                        or contains malformed JSON.
        """
        if not filepath.endswith('.json'):
            raise ValueError("Unsupported file format. Only .json files are accepted.")

        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found at path: {filepath}")
            
        if os.path.getsize(filepath) == 0:
            raise ValueError("File is empty.")

        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            if not isinstance(data, list):
                raise ValueError("JSON content is not a list of records.")
                
            if not data:
                raise ValueError("File contains an empty list.")

            return data
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to decode JSON: {e}")
        except Exception as e:
            # Catch other potential issues like permissions
            raise IOError(f"Error reading file: {e}")
