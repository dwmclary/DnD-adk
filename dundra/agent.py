# Agents from the project
import os
from .sub_agents.writer import writer_agent
from .sub_agents.character_creator import character_creator_agent
from .sub_agents.editor import editor_agent
from .sub_agents.penciller import penciller_agent
from .sub_agents.publisher import publisher_agent
from google.adk.agents.llm_agent import Agent
from google.adk.agents import LoopAgent, SequentialAgent

# =============================
# Workflow: Loop and Sequential Agents
# =============================

iterative_story_refinement_agent = LoopAgent(
    name="iterative_story_refinement_agent",
    description="Iterates through writing and editing to improve the D&D mini campaign adventure.",
    sub_agents=[
        writer_agent,
        character_creator_agent,
        editor_agent
    ],
    max_iterations=3
)

story_creation_agent = SequentialAgent(
    name="story_creation_agent",
    description="The story team agent is responsible for creating the story for the D&D mini campaign adventure.",
    sub_agents=[
        iterative_story_refinement_agent,
        penciller_agent,
        publisher_agent
    ]
)

root_agent = Agent(
    name="root_agent",
    description="The root agent is the entry point for the D&D mini campaign adventure.",
    model="gemini-3-flash-preview",
    instruction="""
    - Greet the user and let them know you will help them write a D&D mini campaign adventure.
    - Ask them for a topic that the mini campaign should be about.
    - When they respond, set the value of 'prompt' to the user's input AND transfer to the 'story_creation' agent
    """,
    output_key="prompt",
    sub_agents=[story_creation_agent]
)
