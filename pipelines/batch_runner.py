"""
Batch runner using Google Sheets as live input.
"""

from datetime import date
from .daily_runner import run_daily_ai
from reports.report_generator import generate_markdown_report
from data.sheets_loader import load_sheet_as_dataframe

def run_batch_from_sheet(sheet_id: str, save_report: bool = True):
    df = load_sheet_as_dataframe(sheet_id)
    results = []

    for _, row in df.iterrows():
        result = run_daily_ai(
            location=row["location"],
            observation=row["observation"],
            base_confidence=int(row["base_confidence"]),
            outcome=row.get("outcome") or None
        )
        results.append(result)

    if save_report:
        report = generate_markdown_report(results)
        filename = f"/content/real-estate-decision-ai/reports/report_{date.today().isoformat()}.md"
        with open(filename, "w") as f:
            f.write(report)

    return results
