"""
Daily automation entry point for Real Estate Decision AI.
"""

import sys
from datetime import datetime

# Ensure repo path is available
sys.path.append("/content/real-estate-decision-ai")

from pipelines.batch_runner import run_batch_from_sheet # Import the new function

# Define the Google Sheet ID
SHEET_ID = "1h_KJ1apOVmW-6IbksC2HupobKkcz7R2JxbBVALWvWUw" # Replace with your actual sheet ID if different

def main():
    print(f"[{datetime.now()}] Starting daily AI run from Google Sheet...")

    results = run_batch_from_sheet(
        sheet_id=SHEET_ID,
        save_report=True
    )

    print(f"[{datetime.now()}] AI run completed.")
    print(f"Decisions generated: {len(results)}")

if __name__ == "__main__":
    main()
