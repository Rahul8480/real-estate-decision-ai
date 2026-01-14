"""
Batch runner for structured AI execution with reporting.
"""

import csv
from datetime import date
from pipelines.daily_runner import run_daily_ai
from reports.report_generator import generate_markdown_report

def run_batch(csv_path: str, save_report: bool = True):
    results = []

    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
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
