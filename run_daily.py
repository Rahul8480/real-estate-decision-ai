"""
Daily automation entry point for Real Estate Decision AI.
"""

import sys
from datetime import datetime

# Ensure repo path is available
sys.path.append("/content/real-estate-decision-ai")

# Import the batch runner that loads from CSV
from pipelines.batch_runner import run_batch

# Define the path to the local CSV input
CSV_INPUT_PATH = "/content/real-estate-decision-ai/data/sample_inputs.csv"

def main():
    print(f"[{datetime.now()}] Starting daily AI run from local CSV...")

    results = run_batch(
        csv_path=CSV_INPUT_PATH,
        save_report=True
    )

    print(f"[{datetime.now()}] AI run completed.")
    print(f"Decisions generated: {len(results)}")

if __name__ == "__main__":
    main()
