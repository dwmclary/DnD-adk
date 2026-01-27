import os
from google.adk import Agent
# from google.adk.code_executors import VertexAiCodeExecutor

# Tools from the project
from ...tools import adk_html_tool
from .prompt import PUBLISHER_PROMPT

# =============================
# Agent Definition
# =============================

publisher_agent = Agent(
    name="publisher_agent",
    model="gemini-3-pro-preview",
    description="Execute the code to publish the Dungeons and Dragons mini campaign adventure to a website",
    instruction=PUBLISHER_PROMPT,
    tools=[adk_html_tool],
    output_key="publication_html"
)
