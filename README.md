# Order Processing Pipeline

A simple ETL pipeline for processing shop order data from JSON files with comprehensive testing.

## Project Structure

```
order_pipeline/
├── __init__.py
├── reader.py       # Reads JSON data
├── validator.py    # Validates and filters data
├── transformer.py  # Cleans and transforms data
├── analyzer.py     # Computes statistics
├── exporter.py     # Exports results
└── pipeline.py     # Main orchestrator
tests/
├── test_*.py       # Unit tests for each module
└── test_pipeline.py # Integration test
requirements.txt    # Python dependencies
README.md          # This file
.gitignore         # Git ignore rules
shoplink.json      # Sample input data
shoplink_cleaned.json # Sample output data
```

## Installation

```bash
pip install -r requirements.txt
```

## Usage

Run the pipeline with default files:
```bash
python -m order_pipeline.pipeline
```

This processes `shoplink.json` and creates `shoplink_cleaned.json`.

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=order_pipeline
```

## Pipeline Process

1. **Read** - Loads JSON data from file
2. **Validate** - Filters out invalid records 
3. **Transform** - Cleans and standardizes data
4. **Analyze** - Computes revenue statistics
5. **Export** - Saves results to JSON file
