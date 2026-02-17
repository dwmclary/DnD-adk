
import os
from google.adk import Agent
from .prompt import ENCOUNTER_MANAGER_PROMPT
from ...tools import campaign_vertex_search_tool

# =============================
# Agent Definition
# =============================

encounter_manager_agent = Agent(
    name="encounter_manager_agent",
    model=os.getenv("MODEL_NAME"),
    description="Generates random encounter tables and quests for the D&D mini campaign.",
    instruction=ENCOUNTER_MANAGER_PROMPT,
    tools=[campaign_vertex_search_tool],
    output_key="encounters_and_quests"
)
