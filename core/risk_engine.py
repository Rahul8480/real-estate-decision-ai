"""
Risk analysis and memory engine.
Tracks recurring and systemic risks.
"""

from collections import defaultdict

# Persistent risk memory
risk_pattern_memory = defaultdict(int)

def register_risk(risk_flag: str):
    """
    Store observed risks for pattern detection.
    """
    if not risk_flag or risk_flag.lower() == "not specified":
        return
    risk_pattern_memory[risk_flag] += 1

def compare_risk_with_history(risk_flag: str) -> str:
    """
    Compare current risk with historical patterns.
    """
    count = risk_pattern_memory.get(risk_flag, 0)
    if count >= 3:
        return "Recurring risk pattern detected"
    if count == 2:
        return "Risk repetition emerging"
    return "New or isolated risk"

def cross_location_risk_correlation(risk_flags: list) -> list:
    """
    Identify systemic risks across locations.
    """
    correlated = []
    for risk in set(risk_flags):
        if risk_pattern_memory.get(risk, 0) >= 2:
            correlated.append(risk)
    return correlated
