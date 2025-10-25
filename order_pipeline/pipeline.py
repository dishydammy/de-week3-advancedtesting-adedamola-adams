import logging
from order_pipeline.reader import DataReader
from order_pipeline.validator import DataValidator
from order_pipeline.transformer import DataTransformer
from order_pipeline.analyzer import DataAnalyzer
from order_pipeline.exporter import DataExporter

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class OrderPipeline:
    """Orchestrates the entire order processing pipeline."""
    
    def __init__(self):
        self.reader = DataReader()
        self.validator = DataValidator()
        self.transformer = DataTransformer()
        self.analyzer = DataAnalyzer()
        self.exporter = DataExporter()

    def run(self, input_filepath: str, output_filepath: str):
        """
        Runs the full ETL pipeline.
        
        1. Reads data
        2. Validates data
        3. Transforms data
        4. Analyzes data
        5. Exports results
        """
        try:
            # 1. Reader
            logging.info(f"Starting pipeline for file: {input_filepath}")
            raw_data = self.reader.read_json_data(input_filepath)
            
            # 2. Validator
            validated_data = self.validator.validate_data(raw_data)
            if not validated_data:
                logging.warning("No valid data found after validation. Pipeline stopping.")
                return

            # 3. Transformer
            transformed_data = self.transformer.transform_data(validated_data)
            if not transformed_data:
                logging.warning("No data survived transformation. Pipeline stopping.")
                return

            # 4. Analyzer
            analysis_results = self.analyzer.analyze_data(transformed_data)
            logging.info(f"Analysis complete: {analysis_results}")

            # 5. Exporter
            self.exporter.export_data(transformed_data, analysis_results, output_filepath)
            logging.info(f"Pipeline finished. Output saved to {output_filepath}")

        except (ValueError, FileNotFoundError, IOError) as e:
            logging.critical(f"Pipeline failed: {e}")
        except Exception as e:
            logging.critical(f"An unexpected error occurred: {e}", exc_info=True)

def main():
    """Main entry point to run the pipeline."""
    # Define file paths
    # In a real app, these would come from config or args
    input_file = "shoplink.json"
    output_file = "shoplink_cleaned.json"
    
    pipeline = OrderPipeline()
    pipeline.run(input_file, output_file)

if __name__ == "__main__":
    main()
