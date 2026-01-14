"""
Loads data from Google Sheets.
"""

import pandas as pd

def load_sheet_as_dataframe(sheet_id: str) -> pd.DataFrame:
    sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
    df = pd.read_csv(sheet_url)
    # Ensure consistent column names expected by run_daily_ai
    df = df.rename(columns={
        "City – Micro Location": "location",
        "Observation": "observation",
        "Confidence (0–100)": "base_confidence",
        "Outcome (later)": "outcome"
    })
    return df
