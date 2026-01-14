"""
Strategy generation engine.
Converts intelligence signals into actionable strategies.
"""

def generate_strategy(confidence: int, risk_note: str) -> str:
    """
    Generate an action strategy based on confidence and risk context.
    """
    if confidence >= 70 and "Recurring" not in risk_note:
        return "Selective entry strategy: proceed with controlled exposure."

    if confidence >= 60 and "Recurring" in risk_note:
        return "Risk-aware strategy: monitor closely and mitigate risks."

    if confidence < 60:
        return "Conservative strategy: wait for stronger confirmation."

    return "Observation mode: insufficient clarity for action."
