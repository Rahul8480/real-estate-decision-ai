"""
Generates human-readable AI decision reports in Markdown format.
"""

from datetime import date

def generate_markdown_report(results: list) -> str:
    today = date.today().isoformat()
    lines = [
        f"# Real Estate AI Decision Report — {today}",
        "",
        f"Total Decisions: {len(results)}",
        "",
        "---",
        ""
    ]

    for i, r in enumerate(results, 1):
        lines.extend([
            f"## Decision {i}: {r['location']}",
            "",
            f"**Observation:** {r['observation']}",
            "",
            f"**Fact:** {r['fact']}",
            "",
            f"**Insight:** {r['insight'] or 'No derived insight (deterministic mode)'}",
            "",
            f"**Assumption:** {r['assumption']}",
            "",
            f"**Risk:** {r['risk']}",
            "",
            f"**Risk Note:** {r['risk_note']}",
            "",
            f"**Confidence:** {r['confidence']}/100",
            "",
            f"**Strategy:** {r['strategy']}",
            "",
            "---",
            ""
        ])

    return "\n".join(lines)
