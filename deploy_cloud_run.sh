#!/bin/bash
set -e

# Configuration
SERVICE_NAME="dundra-adk-agent"
REGION="us-central1"
IMAGE_NAME="gcr.io/${GOOGLE_CLOUD_PROJECT}/${SERVICE_NAME}"

# Colors
GREEN='\033[0;32m'
NC='\033[0m' # No Color

echo -e "${GREEN}Deploying $SERVICE_NAME to Google Cloud Run...${NC}"

# Check for gcloud
if ! command -v gcloud &> /dev/null; then
    echo "gcloud command not found. Please install the Google Cloud SDK."
    exit 1
fi

# Get Project ID
PROJECT_ID=$(gcloud config get-value project)
if [ -z "$PROJECT_ID" ]; then
    echo "No Google Cloud Project ID set. Please run 'gcloud config set project YOUR_PROJECT_ID'."
    exit 1
fi
echo "Project ID: $PROJECT_ID"

# Prepare environment variables from web/.env
FIREBASE_ENV_VARS=""
if [ -f "web/.env" ]; then
    echo "Loading environment variables from web/.env..."
    while IFS='=' read -r key value; do
        # Skip comments and empty lines
        if [[ $key =~ ^#.* ]] || [[ -z $key ]]; then
            continue
        fi
        # Map VITE_FIREBASE_ to FIREBASE_
        if [[ $key == VITE_FIREBASE_* ]]; then
            # Strip VITE_ prefix
            NEW_KEY=${key#VITE_}
            FIREBASE_ENV_VARS="${FIREBASE_ENV_VARS}${NEW_KEY}=${value},"
        fi
    done < "web/.env"
    # Remove trailing comma
    FIREBASE_ENV_VARS=${FIREBASE_ENV_VARS%,}
fi

# Build the image using Cloud Build
echo -e "${GREEN}Building image...${NC}"
gcloud builds submit --tag "gcr.io/$PROJECT_ID/$SERVICE_NAME" .

# Load environment variables from dundra/.env
if [ -f "dundra/.env" ]; then
    echo "Loading environment variables from dundra/.env..."
    export $(grep -v '^#' dundra/.env | xargs)
fi

# Map GOOGLE_CLOUD_STORAGE_BUCKET to GCS_BUCKET_NAME if not already set
if [ -z "$GCS_BUCKET_NAME" ] && [ -n "$GOOGLE_CLOUD_STORAGE_BUCKET" ]; then
    export GCS_BUCKET_NAME="$GOOGLE_CLOUD_STORAGE_BUCKET"
fi

# Deploy to Cloud Run
echo -e "${GREEN}Deploying to Cloud Run...${NC}"
gcloud run deploy "$SERVICE_NAME" \
    --image "gcr.io/$PROJECT_ID/$SERVICE_NAME" \
    --platform managed \
    --region "$REGION" \
    --no-allow-unauthenticated \
    --set-env-vars "GCS_BUCKET_NAME=${GCS_BUCKET_NAME},MODEL_NAME=${MODEL_NAME},DND_DATASTORE_CHARACTERS_ID=${DND_DATASTORE_CHARACTERS_ID},DND_DATASTORE_CAMPAIGN_ID=${DND_DATASTORE_CAMPAIGN_ID},GOOGLE_GENAI_USE_VERTEXAI=${GOOGLE_GENAI_USE_VERTEXAI},GOOGLE_CLOUD_PROJECT=${GOOGLE_CLOUD_PROJECT},GOOGLE_CLOUD_LOCATION=${GOOGLE_CLOUD_LOCATION},${FIREBASE_ENV_VARS}" \
    --timeout=3600

echo -e "${GREEN}Deployment Complete!${NC}"
