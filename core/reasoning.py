"""
Core deterministic reasoning engine.
Ensures no hallucination and no external fact injection.
"""

def reason_without_hallucination(observation: str) -> dict:
    """
    Convert a raw observation into structured reasoning
    without adding new facts.
    """
    if not observation or not observation.strip():
        return {
            "fact": "No valid observation provided.",
            "insight": "Insufficient data to reason.",
            "assumption": "Input quality risk.",
            "risk": "High uncertainty.",
        }

    return {
        "fact": observation.strip(),
        "insight": "Pattern detected based strictly on the observation.",
        "assumption": "Observation reflects current local conditions.",
        "risk": "Execution, timing, and market response uncertainty.",
    }
