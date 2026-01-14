"""
Daily AI runner.
Connects reasoning, risk, confidence, and strategy engines.
"""

from core.reasoning import reason_without_hallucination
from core.confidence import apply_confidence_decay, learned_confidence
from core.risk_engine import register_risk, compare_risk_with_history
from core.strategy import generate_strategy

def run_daily_ai(location: str, observation: str, base_confidence: int, outcome: str = None):
    """
    Run one full AI decision cycle.
    """

    # Step 1: Reasoning
    reasoning = reason_without_hallucination(observation)

    # Step 2: Risk tracking
    risk_flag = reasoning.get("risk", "Not specified")
    register_risk(risk_flag)
    risk_note = compare_risk_with_history(risk_flag)

    # Step 3: Confidence calibration
    confidence = base_confidence
    if outcome:
        confidence = apply_confidence_decay(confidence, outcome)

    confidence = learned_confidence(confidence)

    # Step 4: Strategy generation
    strategy = generate_strategy(confidence, risk_note)

    # Final decision object
    return {
        "location": location,
        "observation": observation,
        "fact": reasoning["fact"],
        "insight": reasoning["insight"],
        "assumption": reasoning["assumption"],
        "risk": risk_flag,
        "risk_note": risk_note,
        "confidence": confidence,
        "strategy": strategy,
    }
