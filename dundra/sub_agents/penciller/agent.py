# Google ADK imports
import os
from google.adk import Agent

# Tools from the project
from ...tools import adk_imagen_tool
from .prompt import PENCILER_PROMPT

# =============================
# Agent Definition
# =============================

penciller_agent = Agent(
    name="penciller_agent",
    model=os.getenv("MODEL_NAME"),
    description="""
    Generates fantasy character images in a style suitable for Dungeons and Dragons mini campaign adventure illustrations, using Imagen.
    """,
    instruction=PENCILER_PROMPT,
    tools=[adk_imagen_tool],
    output_key="generated_images"
)
