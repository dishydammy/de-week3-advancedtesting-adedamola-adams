import json
import logging
from typing import List, Dict, Any

class DataExporter:
    """Exports cleaned data to a JSON file."""

    def export_data(self, data: List[Dict[str, Any]], analysis: Dict[str, Any], filepath: str):
        """Writes the cleaned data and analysis to a JSON file."""
        
        if not filepath.endswith('.json'):
            raise ValueError("Export file must be a .json file.")

        output_data = {
            "analysis_summary": analysis,
            "cleaned_data": data
        }

        try:
            with open(filepath, 'w') as f:
                json.dump(output_data, f, indent=4)
            logging.info(f"Successfully exported data to {filepath}")
        except IOError as e:
            logging.error(f"Failed to write to file {filepath}: {e}")
            raise
        except TypeError as e:
            logging.error(f"Data is not JSON serializable: {e}")
            raise
