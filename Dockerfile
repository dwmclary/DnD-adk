# Build Frontend
FROM node:18-alpine as frontend-build
WORKDIR /app/web
COPY web/package*.json ./
RUN npm ci
COPY web/ ./
RUN npm run build

# Build Backend
FROM python:3.11-slim

# Install system dependencies if needed (e.g. for some python packages)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY dundra/ dundra/
# Copy built frontend from previous stage
COPY --from=frontend-build /app/web/dist web/dist

# Expose port (Cloud Run uses 8080 by default, but we can configure it)
ENV PORT=8080
EXPOSE 8080

# Run the application
CMD exec uvicorn dundra.api:app --host 0.0.0.0 --port $PORT
