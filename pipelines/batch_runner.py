"""
Batch runner using Google Sheets as live input.
Exports Markdown + JSON.
"""

from datetime import date
from .daily_runner import run_daily_ai
from reports.report_generator import generate_markdown_report
from reports.json_exporter import export_results_to_json
from data.sheets_loader import load_sheet_as_dataframe

OUTPUT_DIR = "/content/real-estate-decision-ai/reports"

def run_batch_from_sheet(sheet_id: str, save_outputs: bool = True):
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

    if save_outputs:
        # Markdown report
        report = generate_markdown_report(results)
        md_path = f"{OUTPUT_DIR}/report_{date.today().isoformat()}.md"
        with open(md_path, "w") as f:
            f.write(report)

        # JSON output
        export_results_to_json(results, OUTPUT_DIR)

    return results
