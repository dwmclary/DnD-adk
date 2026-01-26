# Google ADK imports
from google.adk.tools import VertexAiSearchTool
from google.adk.tools.crewai_tool import CrewaiTool

# Third-party tools
from dundra.imagen_tool import ImagenTool

# =============================
# Tool Instantiation
# =============================
import os

# Vertex AI Search Datastore IDs
DND_DATASTORE_CHARACTERS_ID = os.getenv("DND_DATASTORE_CHARACTERS_ID")
DND_DATASTORE_CAMPAIGN_ID = os.getenv("DND_DATASTORE_CAMPAIGN_ID")

if not DND_DATASTORE_CHARACTERS_ID or not DND_DATASTORE_CAMPAIGN_ID:
    # Use dummy values if not set to avoid import errors during testing if tools aren't used
    # But print a warning
    print("WARNING: DND_DATASTORE_CHARACTERS_ID or DND_DATASTORE_CAMPAIGN_ID not set.")
    # We might want to set them to something that won't crash immediately but fails if used
    if not DND_DATASTORE_CHARACTERS_ID:
        DND_DATASTORE_CHARACTERS_ID = "full-search-characters" # Fallback or dummy
    if not DND_DATASTORE_CAMPAIGN_ID:
        DND_DATASTORE_CAMPAIGN_ID = "full-search-campaign"   # Fallback or dummy


characters_vertex_search_tool = VertexAiSearchTool(
    data_store_id=DND_DATASTORE_CHARACTERS_ID
)
campaign_vertex_search_tool = VertexAiSearchTool(
    data_store_id=DND_DATASTORE_CAMPAIGN_ID
)

imagen_tool = ImagenTool()

adk_imagen_tool = CrewaiTool(
    name="Imagen_Images_Creator",
    description="""A tool designed to generate images using Google's Imagen model.""",
    tool=imagen_tool
)
