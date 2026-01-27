# Google ADK imports
import os
from google.adk import Agent

# Prompt for this agent
from .prompt import MONSTER_MAKER_PROMPT

# =============================
# Agent Definition
# =============================

monster_maker_agent = Agent(
    name="monster_maker_agent",
    model=os.getenv("MODEL_NAME"),
    description="Generates monsters and stat blocks for the Dungeons and Dragons mini campaign adventure.",
    instruction=MONSTER_MAKER_PROMPT,
    tools=[], # Uses internal model knowledge for Monster Manual
    output_key="monsters_brief",
)
