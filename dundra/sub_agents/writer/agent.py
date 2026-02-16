# Google ADK imports
import os
from google.adk import Agent

# Tools from the project
from ...tools import campaign_vertex_search_tool
# Prompt for this agent
from .prompt import WRITER_PROMPT

# =============================
# Agent Definition
# =============================

writer_agent = Agent(
    name="writer_agent",
    model=os.getenv("MODEL_NAME"),
    description=" Writes the initial draft of the Dungeons and Dragons mini campaign adventure. ",
    instruction=WRITER_PROMPT,
    tools=[campaign_vertex_search_tool],
    output_key="current_story",
)
