"""
Batch runner for structured AI execution.
"""

import csv
from pipelines.daily_runner import run_daily_ai

def run_batch(csv_path: str):
    results = []

    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            result = run_daily_ai(
                observation=row["observation"],
                base_confidence=int(row["base_confidence"]),
                outcome=row.get("outcome") or None
            )
            result["location"] = row["location"]
            results.append(result)

    return results
