"""
Generates formatted reports from AI results.
"""

from datetime import date

def generate_markdown_report(results: list) -> str:
    report_lines = ["# Real Estate AI Daily Report", ""]
    report_lines.append(f"Generated on: {date.today().isoformat()}")
    report_lines.append("")

    if not results:
        report_lines.append("No decisions generated for today.")
        return "\n".join(report_lines)

    for i, r in enumerate(results, 1):
        report_lines.extend([
            f"## Decision {i}: {r.get('location', 'N/A')}",
            "",
            f"**Observation:** {r.get('observation', 'N/A')}",
            f"**Insight:** {r.get('insight', 'N/A')}",
            f"**Assumptions:** {r.get('assumption', 'N/A')}",
            f"**Risk:** {r.get('risk', 'Not specified')} ({r.get('risk_note', 'N/A')})",
            f"**Confidence:** {r.get('confidence', 'N/A')}/100",
            f"**Strategy:** {r.get('strategy', 'N/A')}",
            "---",
            ""
        ])

    return "\n".join(report_lines)
