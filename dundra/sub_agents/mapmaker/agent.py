# Google ADK imports
import os
from google.adk import Agent

# Tools from the project
from ...tools import adk_imagen_tool
from .prompt import MAPMAKER_PROMPT

# =============================
# Agent Definition
# =============================

mapmaker_agent = Agent(
    name="mapmaker_agent",
    model=os.getenv("MODEL_NAME"),
    description="""
    Generates battle maps for key locations in the Dungeons and Dragons mini campaign adventure using Imagen.
    """,
    instruction=MAPMAKER_PROMPT,
    tools=[adk_imagen_tool],
    output_key="battle_maps"
)
