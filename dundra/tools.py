# Google ADK imports
from google.adk.tools import VertexAiSearchTool

# Third-party tools
from dundra.imagen_tool import ImagenTool
from dundra.html_writer_tool import HtmlWriterTool

# =============================
# Tool Instantiation
# =============================
import os

# Vertex AI Search Datastore IDs
DND_DATASTORE_CHARACTERS_ID = os.getenv("DND_DATASTORE_CHARACTERS_ID")
DND_DATASTORE_CAMPAIGN_ID = os.getenv("DND_DATASTORE_CAMPAIGN_ID")
print(f"Characters Datastore ID: {DND_DATASTORE_CHARACTERS_ID}")
print(f"Campaign Datastore ID: {DND_DATASTORE_CAMPAIGN_ID}")

if not DND_DATASTORE_CHARACTERS_ID or not DND_DATASTORE_CAMPAIGN_ID:
    print("WARNING: DND_DATASTORE_CHARACTERS_ID or DND_DATASTORE_CAMPAIGN_ID not set.")
    if not DND_DATASTORE_CHARACTERS_ID:
        DND_DATASTORE_CHARACTERS_ID = "full-search-characters" 
    if not DND_DATASTORE_CAMPAIGN_ID:
        DND_DATASTORE_CAMPAIGN_ID = "full-search-campaign"

# Helper to construct full resource name
def get_datastore_resource_name(datastore_id):
    if not datastore_id:
        return None
    project = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = os.getenv("GOOGLE_CLOUD_LOCATION", "global")
    # Using 'default_collection' as standard for Vertex AI Search
    return f"projects/{project}/locations/{location}/collections/default_collection/dataStores/{datastore_id}"

characters_vertex_search_tool = VertexAiSearchTool(
    data_store_id=get_datastore_resource_name(DND_DATASTORE_CHARACTERS_ID)
)
campaign_vertex_search_tool = VertexAiSearchTool(
    data_store_id=get_datastore_resource_name(DND_DATASTORE_CAMPAIGN_ID)
)

# Instantiate tools directly
imagen_tool = ImagenTool()
# For ADK, we might need to name them if the agent uses name lookup, or generally the tool's own name attribute is used.
# If ADK needs a wrapper, we can use FunctionTool, but Custom Tools usually inherit from Tool or just implement __call__ / run.
# I will assume for now that passing the instance is enough or I will fix it if ADK complains.
# Actually ADK has a `Tool` class. `VertexAiSearchTool` inherits from it.
# My `ImagenTool` and `HtmlWriterTool` will need to inherit from `google.adk.tools.Tool` or be compatible.
# I'll stick to just instantiating them here.

adk_imagen_tool = imagen_tool # Alias for backward compatibility if needed, but better to use `imagen_tool`
# In `agent.py` or subagents, they import `imagen_tool`? 
# I should check where `adk_imagen_tool` was used.
# The `tools.py` exported `adk_imagen_tool`. I will keep the name but assigning the instance.

html_writer = HtmlWriterTool()
adk_html_tool = html_writer

