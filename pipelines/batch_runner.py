"""
Batch processing pipeline.
Reads from a Google Sheet and runs daily AI for each entry.
"""

import pandas as pd
from pipelines.daily_runner import run_daily_ai

def run_batch_from_sheet(sheet_id: str, save_report: bool = False):
    sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
    df = pd.read_csv(sheet_url)

    all_results = []

    for _, row in df.iterrows():
        result = run_daily_ai(
            observation=row["Observation"], # Corrected column name
            base_confidence=int(row["Confidence (0–100)"]), # Corrected column name
            outcome=row.get("Outcome (later)") # Use .get for optional column
        )
        all_results.append(result)

    return all_results
