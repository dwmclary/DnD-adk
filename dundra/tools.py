# Google ADK imports
from google.adk.tools import VertexAiSearchTool
from google.adk.tools.crewai_tool import CrewaiTool

# Third-party tools
from dundra.imagen_tool import ImagenTool

# =============================
# Tool Instantiation
# =============================
# Vertex AI Search Datastore IDs (replace with your actual IDs as needed)

DND_DATASTORE_CHARACTERS_ID = (
    "<your-characters-datastore-id>"
)
DND_DATASTORE_CAMPAIGN_ID = (
    "<your-campaign-datastore-id>"
)

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
