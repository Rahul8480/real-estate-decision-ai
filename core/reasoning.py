import pandas as pd
import os
import glob
import time
from datetime import date
from typing import List, Dict, Any

# --- Global Configuration (for this module's self-containment) ---
# These paths would ideally be managed centrally in a larger application config
KNOWLEDGE_BASE_PATH = "/content/drive/MyDrive/AI_Knowledge_Base"
NEWS_PATH = "/content/drive/MyDrive/AI_Knowledge_Base/news"
MAX_CONFIDENCE = 70
MIN_CONFIDENCE = 30

# Global LLM variable (will be set to an Llama object if loaded externally)
# This is assumed to be set in the main script and accessed here.
llm = None

# --- Helper Functions for LLM/Knowledge Integration ---
def retrieve_knowledge(keywords, max_files=2):
    matched_contents = []
    if not os.path.exists(KNOWLEDGE_BASE_PATH):
        # print(f"Warning: Knowledge base path '{KNOWLEDGE_BASE_PATH}' does not exist.") # Suppress in module
        return []
    for category_path in glob.glob(f"{KNOWLEDGE_BASE_PATH}/*"):
        for file in glob.glob(f"{category_path}/*.md"):
            with open(file, "r") as f:
                text = f.read().lower()
                if any(k.lower() in text for k in keywords):
                    matched_contents.append(text)
                    if len(matched_contents) >= max_files:
                        return matched_contents
    return matched_contents

def retrieve_recent_news(keywords, max_files=3):
    matches = []
    if not os.path.exists(NEWS_PATH):
        # print(f"Warning: News path '{NEWS_PATH}' does not exist.") # Suppress in module
        return []
    for file in sorted(glob.glob(f"{NEWS_PATH}/*.md"), reverse=True):
        with open(file, "r") as f:
            text = f.read().lower()
            if any(k.lower() in text for k in keywords):
                matches.append(text)
                if len(matches) >= max_files:
                    break
    return matches

def generate_llm_insight_and_risk(reasoning_prompt: str) -> str:
    """
    Placeholder function to simulate LLM generating insights and risk flags.
    In a real scenario, this would call the actual LLM (e.g., llm.create_completion).
    The output format is crucial for parse_llm_output.
    """
    # print("Simulating LLM generation...") # Suppress in module
    # Based on keywords in the prompt, simulate a response
    if "ghangapatna" in reasoning_prompt.lower() and "residential" in reasoning_prompt.lower():
        return "LLM_INSIGHT: Micro-location continues to show strong residential potential. LLM_RISK: Local regulatory changes could impact project timelines."
    elif "it corridor" in reasoning_prompt.lower():
        return "LLM_INSIGHT: IT corridor expansion drives demand. LLM_RISK: Overtaxed infrastructure is a concern."
    else:
        return "LLM_INSIGHT: General positive outlook based on trends. LLM_RISK: No specific risks identified by LLM."

def parse_llm_output(llm_raw_output: str) -> dict:
    """
    Parses the simulated LLM output to extract structured insight and risk.
    """
    insight = ""
    risk = "Not specified"

    if "LLM_INSIGHT:" in llm_raw_output:
        parts = llm_raw_output.split("LLM_INSIGHT:", 1)
        if "LLM_RISK:" in parts[1]:
            insight = parts[1].split("LLM_RISK:", 1)[0].strip()
            risk = parts[1].split("LLM_RISK:", 1)[1].strip()
        else:
            insight = parts[1].strip()

    # Fallback if no specific insight tag
    if not insight and "LLM_RISK:" not in llm_raw_output:
        insight = llm_raw_output # Assume whole output is insight if no specific tags

    return {"insight": insight, "risk": risk}

# --- Core AI Function ---
def reason_without_hallucination(row: pd.Series) -> dict:
    """
    Deterministic reasoning function, modified to conditionally use LLM.
    No guessing. No new facts.
    """

    fact = row["Observation"]
    current_insight = row["AI Insight"]
    current_risk = row.get("Risk Flag", "Not specified")
    current_confidence = row["Confidence (0–100)"]

    # Hard safety rules for confidence
    if current_confidence > MAX_CONFIDENCE:
        current_confidence = MAX_CONFIDENCE

    # Retrieve context for LLM if available
    keywords = [
        row["Signal Type"],
        row["City – Micro Location"]
    ]
    knowledge_notes = retrieve_knowledge(keywords)
    news_context = retrieve_recent_news(keywords)

    llm_generated_insight = None
    llm_generated_risk = None

    # Use the global llm variable
    global llm

    if llm: # If LLM model is loaded
        # print("LLM available. Generating nuanced insights and risks...") # Suppress in module
        llm_prompt = f"""
        Review the following real estate observation, knowledge context, and news context.
        Based ONLY on the provided information, generate a concise AI Insight and identify any clear Risk Flag.
        Do NOT introduce new facts or speculate.
        Format your response as: LLM_INSIGHT: [Your Insight] LLM_RISK: [Your Risk Flag or 'None']

        Observation: {fact}
        Knowledge Context: {knowledge_notes[:1] if knowledge_notes else 'None'}
        News Context: {news_context[:1] if news_context else 'None'}
        """
        try:
            # This is where the actual LLM call would be (e.g., llm.create_completion)
            # For this definition, we call the placeholder function
            llm_raw_output = generate_llm_insight_and_risk(llm_prompt)
            parsed_llm_output = parse_llm_output(llm_raw_output)
            llm_generated_insight = parsed_llm_output["insight"]
            llm_generated_risk = parsed_llm_output["risk"]
            if llm_generated_risk.lower() == 'none':
                llm_generated_risk = 'Not specified'
        except Exception as e:
            # print(f"Error during LLM call or parsing: {e}. Falling back to default insight/risk.") # Suppress in module
            llm_generated_insight = None
            llm_generated_risk = None
    else:
        pass # print("LLM not loaded. Using default insight/risk from row.") # Suppress in module

    # Use LLM-generated values if available, otherwise fallback to existing row values
    final_insight = llm_generated_insight if llm_generated_insight else current_insight
    final_risk = llm_generated_risk if llm_generated_risk else current_risk

    reasoning = {
        "FACT": fact,
        "INFERENCE": final_insight,
        "ASSUMPTIONS": "Inference assumes observation is accurate and execution timelines hold.",
        "RISK_ACKNOWLEDGED": final_risk,
        "KNOWLEDGE_REFERENCE": knowledge_notes[:1] if knowledge_notes else [],
        "NEWS_CONTEXT": news_context[:1] if news_context else [],
        "CONFIDENCE_CAPPED": current_confidence
    }

    return reasoning
