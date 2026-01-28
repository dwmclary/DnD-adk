
import os
from google.adk import Agent
from .prompt import ENCOUNTER_MANAGER_PROMPT

# =============================
# Agent Definition
# =============================

encounter_manager_agent = Agent(
    name="encounter_manager_agent",
    model=os.getenv("MODEL_NAME", "gemini-3-flash-preview"),
    description="Generates random encounter tables and quests for the D&D mini campaign.",
    instruction=ENCOUNTER_MANAGER_PROMPT,
    output_key="encounters_and_quests"
)
