#!/bin/bash
set -e

# Configuration
# Set GCS_BUCKET_NAME locally if you want to test against real GCS
# export GCS_BUCKET_NAME="your-bucket-name"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Setting up local environment for DunDra...${NC}"

# Check for npm
if ! command -v npm &> /dev/null; then
    echo "npm command not found. Please install Node.js."
    exit 1
fi

# Build Frontend
echo -e "${GREEN}Building Frontend...${NC}"
cd web
npm install
npm run build
cd ..

# Verify Frontend Build
if [ ! -d "web/dist" ]; then
    echo "Frontend build failed. 'web/dist' directory not found."
    exit 1
fi

# Check if venv exists and activate it
if [ -d "venv" ]; then
    echo -e "${GREEN}Activating venv...${NC}"
    source venv/bin/activate
fi

# Install Python Dependencies
echo -e "${GREEN}Installing Python dependencies...${NC}"
pip install -r requirements.txt

# Run Backend
echo -e "${GREEN}Starting Backend...${NC}"
echo -e "${YELLOW}Access the app at http://localhost:8000${NC}"

# Check if .env exists
if [ -f ".env" ]; then
    echo -e "${GREEN}Loading environment variables from .env${NC}"
    export $(grep -v '^#' .env | xargs)
fi

# Load and map web/.env to FIREBASE_ vars for local dev
if [ -f "web/.env" ]; then
    echo -e "${GREEN}Loading and mapping web/.env variables...${NC}"
    while IFS='=' read -r key value; do
        if [[ $key == VITE_FIREBASE_* ]]; then
            NEW_KEY=${key#VITE_}
            export ${NEW_KEY}=${value}
        fi
    done < "web/.env"
fi

# Run with hot reload
uvicorn dundra.api:app --reload --host 0.0.0.0 --port 8000
