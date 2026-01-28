# Google ADK imports
import os
from google.adk import Agent

# Prompt for this agent
from .prompt import LOOT_MAKER_PROMPT

# =============================
# Agent Definition
# =============================

loot_maker_agent = Agent(
    name="loot_maker_agent",
    model=os.getenv("MODEL_NAME"),
    description="Generates magic items and rewards for the Dungeons and Dragons mini campaign adventure.",
    instruction=LOOT_MAKER_PROMPT,
    tools=[], 
    output_key="loot_brief",
)
