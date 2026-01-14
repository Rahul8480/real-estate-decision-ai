"""
Daily AI runner.
Connects reasoning, risk, confidence, and strategy engines.
"""

import pandas as pd # Import pandas to create Series
from core.reasoning import reason_without_hallucination
from core.confidence import apply_confidence_decay, learned_confidence
from core.risk_engine import register_risk, compare_risk_with_history
from core.strategy import generate_strategy

# Placeholder for algorithm_scoreboard, as it's typically global or passed.
# For now, we'll mock a simple one that aligns with confidence.py's expectation if it's not truly global.
# In a fully integrated system, this would come from a shared state.
algorithm_scoreboard = {
    "reasoning": {"uses": 0, "success": 0, "failure": 0},
    "risk_tracking": {"uses": 0, "success": 0, "failure": 0},
    "strategy": {"uses": 0, "success": 0, "failure": 0},
}

def run_daily_ai(location: str, observation: str, base_confidence: int, outcome: str = None):
    """
    Run one full AI decision cycle.
    """

    # Construct a mock row (pandas Series) that reason_without_hallucination expects
    mock_row = pd.Series({
        "City – Micro Location": location,
        "Signal Type": "Generic/Batch Signal", # Default for batch processing
        "Observation": observation,
        "AI Insight": "", # To be filled by reason_without_hallucination
        "Confidence (0–100)": base_confidence,
        "Risk Flag": "Not specified", # To be filled by reason_without_hallucination or overridden
        "Outcome (later)": outcome, # Pass outcome for confidence decay logic
        "Correction / Lesson": "" # Default
    })

    # Step 1: Reasoning (now receives a proper row object)
    reasoning_output = reason_without_hallucination(mock_row)
    
    # Extract necessary fields for subsequent simplified core functions
    risk_flag = reasoning_output.get("RISK_ACKNOWLEDGED", "Not specified")
    confidence = reasoning_output.get("CONFIDENCE_CAPPED", base_confidence)

    # Step 2: Risk tracking (using simplified functions from core/risk_engine.py)
    register_risk(risk_flag) # This requires risk_pattern_memory to be global in risk_engine
    risk_note = compare_risk_with_history(risk_flag) # Uses risk_pattern_memory

    # Step 3: Confidence calibration (using simplified functions from core/confidence.py)
    if outcome:
        confidence = apply_confidence_decay(confidence, outcome)
    # The learned_confidence function in core/confidence.py expects only base_confidence
    # and uses a global algorithm_scoreboard. For this to work with the global scoreboard,
    # we need to ensure algorithm_scoreboard is properly managed/passed or that core/confidence.py
    # is updated to be comprehensive. For now, matching the existing simplified contract.
    # We'll use the confidence value after decay as input for learned_confidence for now.
    # Note: This is where the simple core/confidence vs. comprehensive notebook functions diverge.
    # The core/confidence.py learned_confidence takes base_confidence and calculates factor internally.
    confidence = learned_confidence(confidence)

    # Step 4: Strategy generation (using simplified function from core/strategy.py)
    strategy = generate_strategy(confidence, risk_note)

    # Final decision object
    return {
        "location": location,
        "observation": observation,
        "fact": reasoning_output["FACT"],
        "insight": reasoning_output["INFERENCE"],
        "assumption": reasoning_output["ASSUMPTIONS"],
        "risk": risk_flag,
        "risk_note": risk_note,
        "confidence": confidence,
        "strategy": strategy,
        "outcome": outcome # Include outcome for traceability
    }
