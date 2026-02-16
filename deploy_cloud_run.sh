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

# Build the image using Cloud Build
echo -e "${GREEN}Building image...${NC}"
gcloud builds submit --tag "gcr.io/$PROJECT_ID/$SERVICE_NAME" .

# Deploy to Cloud Run
echo -e "${GREEN}Deploying to Cloud Run...${NC}"
gcloud run deploy "$SERVICE_NAME" \
    --image "gcr.io/$PROJECT_ID/$SERVICE_NAME" \
    --platform managed \
    --region "$REGION" \
    --allow-unauthenticated \
    --set-env-vars "GCS_BUCKET_NAME=${GCS_BUCKET_NAME}"

echo -e "${GREEN}Deployment Complete!${NC}"
