# Google ADK imports
import os
from google.adk import Agent
from google.adk.tools import agent_tool

# Tools from the project
from ...tools import characters_vertex_search_tool
from ...sub_agents.penciller.agent import penciller_agent
from .prompt import CHARACTER_CREATOR_PROMPT

# =============================
# Agent Definition
# =============================

character_creator_agent = Agent(
    name="character_writer_agent",
    model=os.getenv("MODEL_NAME"),
    description="""
    Generates pre-made Non-Player Characters (NPCs) for the Dungeons and Dragons mini campaign adventure.
    """,
    instruction=CHARACTER_CREATOR_PROMPT,
    tools=[characters_vertex_search_tool],
    output_key="characters_brief",
)
