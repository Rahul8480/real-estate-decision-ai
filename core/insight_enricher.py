"""
Insight enrichment engine.
Expands insights deterministically without hallucination.
"""

def enrich_insight(base_insight: str,
                   confidence: int,
                   risk: str,
                   risk_note: str,
                   signal_type: str = "Generic") -> str:

    enriched = base_insight.strip()

    # Confidence-based framing
    if confidence < 55:
        enriched += " Signal strength is weak, suggesting observation rather than action."
    elif 55 <= confidence <= 65:
        enriched += " This indicates early-stage potential that warrants monitoring."
    else:
        enriched += " Signal strength is strong enough to justify selective action."

    # Risk-aware adjustment
    if risk and risk.lower() != "not specified":
        enriched += f" Key risk identified: {risk.lower()}."
        if "recurring" in risk_note.lower():
            enriched += " This risk has appeared repeatedly in similar cases."

    # Signal context
    if "residential" in signal_type.lower():
        enriched += " Residential demand dynamics are the primary driver."

    return enriched
