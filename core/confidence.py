# Confidence calibration and learning engine

algorithm_scoreboard = {
    "reasoning": {"uses": 0, "success": 0, "failure": 0},
    "risk_tracking": {"uses": 0, "success": 0, "failure": 0},
    "strategy": {"uses": 0, "success": 0, "failure": 0},
}

def apply_confidence_decay(base_confidence, outcome):
    if outcome == "Correct":
        return min(100, base_confidence + 3)
    if outcome == "Incorrect":
        return max(0, base_confidence - 7)
    return base_confidence

def learning_adjustment_factor():
    total_uses = sum(v["uses"] for v in algorithm_scoreboard.values())
    if total_uses == 0:
        return 1.0
    total_success = sum(v["success"] for v in algorithm_scoreboard.values())
    return 1.0 + (total_success / total_uses) * 0.1

def learned_confidence(base_confidence):
    return min(100, int(base_confidence * learning_adjustment_factor()))
