"""
Exports AI results to JSON for programmatic consumption.
"""

import json
from datetime import date

def export_results_to_json(results: list, output_dir: str) -> str:
    filename = f"{output_dir}/results_{date.today().isoformat()}.json"
    with open(filename, "w") as f:
        json.dump(results, f, indent=2)
    return filename
