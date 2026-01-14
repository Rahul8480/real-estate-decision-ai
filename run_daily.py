"""
Daily automation entry point for Real Estate Decision AI.
"""

import sys
from datetime import datetime

# Ensure repo path is available
sys.path.append("/content/real-estate-decision-ai")

from pipelines.batch_runner import run_batch

def main():
    print(f"[{datetime.now()}] Starting daily AI run...")

    results = run_batch(
        "/content/real-estate-decision-ai/data/sample_inputs.csv",
        save_report=True
    )

    print(f"[{datetime.now()}] AI run completed.")
    print(f"Decisions generated: {len(results)}")

if __name__ == "__main__":
    main()
