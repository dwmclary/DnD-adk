import os
from datetime import datetime
import logging
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import JSONResponse, FileResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from google.adk.cli.fast_api import get_fast_api_app
from google.cloud import storage
from dundra.auth import verify_user, verify_user_query_token

# Configure logging
logging.basicConfig(level=logging.INFO)
logging.getLogger("google.adk").setLevel(logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize GCS client if configured
BUCKET_NAME = os.getenv("GCS_BUCKET_NAME") or os.getenv("GOOGLE_CLOUD_STORAGE_BUCKET")
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

# Middleware to protect ADK routes
@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    # List of paths to protect
    protected_paths = ["/run_sse", "/active_agents"]
    
    # Check if path starts with any protected path
    is_protected = any(request.url.path.startswith(path) for path in protected_paths)
    
    if is_protected:
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse(status_code=401, content={"detail": "Missing or invalid Authorization header"})
        
        token = auth_header.split(" ")[1]
        try:
             # We manually verify here because we are in middleware
             # and can't easily use Depends
             from firebase_admin import auth
             decoded_token = auth.verify_id_token(token)
             email = decoded_token.get("email")
             
             if email != "dan.mcclary@gmail.com":
                 return JSONResponse(status_code=403, content={"detail": f"Access denied for {email}"})
                 
             # Store user in request state if needed
             request.state.user = decoded_token
        except Exception as e:
             logger.error(f"Middleware auth failed: {e}")
             return JSONResponse(status_code=401, content={"detail": "Authentication failed"})

    response = await call_next(request)
    return response

@app.get("/api/stories", dependencies=[Depends(verify_user)])
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
                        "url": f"/api/stories/{blob.name}",
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
                    "created": datetime.fromtimestamp(os.path.getmtime(filepath)).isoformat()
                })
    
    # Sort by creation time (descending)
    stories.sort(key=lambda x: x.get("created") or 0, reverse=True)
    return stories

@app.get("/api/stories/{filename:path}")
async def get_story_content(filename: str, request: Request, user: dict = Depends(verify_user_query_token)):
    """Proxy story content from local storage or GCS. Requires token query param."""
    # check local first
    local_path = os.path.join("generated_stories", filename)
    if os.path.exists(local_path):
        return FileResponse(local_path)

    # force check GCS if configured
    if storage_client and BUCKET_NAME:
        try:
            bucket = storage_client.bucket(BUCKET_NAME)
            blob = bucket.blob(filename)
            if blob.exists():
                # Determine media type based on extension
                media_type = "application/octet-stream"
                if filename.endswith(".html"):
                    media_type = "text/html"
                elif filename.endswith(".png"):
                    media_type = "image/png"
                elif filename.endswith(".jpg") or filename.endswith(".jpeg"):
                    media_type = "image/jpeg"
                elif filename.endswith(".gif"):
                    media_type = "image/gif"
                elif filename.endswith(".webp"):
                    media_type = "image/webp"

                content = blob.download_as_bytes()
                
                # If HTML, rewrite GCS links to proxy links WITH token
                if media_type == "text/html":
                    text_content = content.decode("utf-8")
                    gcs_prefix = f"https://storage.googleapis.com/{BUCKET_NAME}/"
                    
                    # We need to append ?token=... to the proxy URL
                    # The incoming request has the token in query params
                    token = request.query_params.get("token")
                    proxy_prefix = f"/api/stories/"
                    
                    # We can't just do a simple string replace if we want to append the token
                    # But we can replace the prefix and then regex to append token? 
                    # Or just simple replace and hope for the best? 
                    # If we just replace prefix, the images will be loaded as /api/stories/image.png
                    # The browser will NOT attach the token query param to subresources automatically.
                    # So we MUST Embed the token.
                    
                    # Strategy: Replace GCS URL with /api/stories/FILENAME?token=TOKEN
                    # Since we don't know the filename length easily with simple replace, 
                    # we might need regex.
                    import re
                    # Pattern: https://storage.googleapis.com/BUCKET/([^"'\s]+)
                    # We want to capture the path after the bucket
                    
                    def replace_link(match):
                        path = match.group(1)
                        return f"/api/stories/{path}?token={token}"

                    pattern = f"https://storage.googleapis.com/{BUCKET_NAME}/([^\"'\\s>]+)"
                    text_content = re.sub(pattern, replace_link, text_content)
                    
                    content = text_content.encode("utf-8")

                return Response(
                    content=content,
                    media_type=media_type,
                    status_code=200
                )
        except Exception as e:
             logger.error(f"Error fetching GCS story {filename}: {e}")
    
    raise HTTPException(status_code=404, detail="Story not found")

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/api/config")
async def get_config():
    """Returns the Firebase configuration for the frontend."""
    return {
        "apiKey": os.getenv("FIREBASE_API_KEY"),
        "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN"),
        "projectId": os.getenv("FIREBASE_PROJECT_ID"),
        "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET"),
        "messagingSenderId": os.getenv("FIREBASE_MESSAGING_SENDER_ID"),
        "appId": os.getenv("FIREBASE_APP_ID")
    }

# Serve local stories if needed
if os.path.exists("generated_stories"):
    app.mount("/stories", StaticFiles(directory="generated_stories"), name="stories")

# Serve frontend static files
# In production/docker, we will put the build in 'web/dist' or similar
frontend_dist = "web/dist"
if os.path.exists(frontend_dist):
    app.mount("/", StaticFiles(directory=frontend_dist, html=True), name="frontend")
