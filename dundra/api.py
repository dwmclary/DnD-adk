import os
import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from google.adk.cli.fast_api import get_fast_api_app
from google.cloud import storage

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize GCS client if configured
BUCKET_NAME = os.getenv("GCS_BUCKET_NAME")
storage_client = None
if BUCKET_NAME:
    try:
        storage_client = storage.Client()
    except Exception as e:
        logger.warning(f"Failed to initialize GCS client: {e}")

# Create the ADK FastAPI app
# We point agents_dir to the current directory ("."), 
# so 'dundra' package is loaded as an agent named 'dundra'
app = get_fast_api_app(
    agents_dir=".",
    web=False
)

# Allow CORS for development (if frontend is running separately)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/stories")
async def list_stories():
    """List generated stories from GCS bucket or local directory."""
    stories = []
    
    # List from GCS
    if storage_client and BUCKET_NAME:
        try:
            bucket = storage_client.bucket(BUCKET_NAME)
            blobs = bucket.list_blobs()
            for blob in blobs:
                if blob.name.endswith(".html"):
                    stories.append({
                        "name": blob.name,
                        "url": f"https://storage.googleapis.com/{BUCKET_NAME}/{blob.name}",
                        "source": "gcs",
                        "created": blob.time_created.isoformat() if blob.time_created else None
                    })
        except Exception as e:
            logger.error(f"Error listing GCS stories: {e}")

    # List from local (if any, or fallback)
    local_dir = "generated_stories"
    if os.path.exists(local_dir):
        for filename in os.listdir(local_dir):
            if filename.endswith(".html"):
                # If we already have it from GCS (same name), skip or mark?
                # For simplicity, we just list what we find.
                filepath = os.path.join(local_dir, filename)
                stories.append({
                    "name": filename,
                    "url": f"/stories/{filename}", # Local serve path
                    "source": "local",
                    "created": os.path.getmtime(filepath)
                })
    
    # Sort by creation time (descending)
    stories.sort(key=lambda x: x.get("created") or 0, reverse=True)
    return stories

# Serve local stories if needed
if os.path.exists("generated_stories"):
    app.mount("/stories", StaticFiles(directory="generated_stories"), name="stories")

# Serve frontend static files
# In production/docker, we will put the build in 'web/dist' or similar
frontend_dist = "web/dist"
if os.path.exists(frontend_dist):
    app.mount("/", StaticFiles(directory=frontend_dist, html=True), name="frontend")

@app.get("/health")
async def health():
    return {"status": "ok"}
