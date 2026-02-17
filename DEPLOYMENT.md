# Deploying ADK Agents to Google Cloud Run

This guide explains how to deploy the ADK agents to Google Cloud Run using the provided script.

## Prerequisites

1.  **Google Cloud SDK (`gcloud`)**: Ensure the `gcloud` CLI is installed and authenticated.
    ```bash
    gcloud auth login
    ```

2.  **Google Cloud Project**: You must have a Google Cloud Project with billing enabled.
    Set your project ID:
    ```bash
    gcloud config set project YOUR_PROJECT_ID
    ```

3.  **APIs Enabled**: Ensure the following APIs are enabled in your project:
    -   Cloud Build API (`cloudbuild.googleapis.com`)
    -   Cloud Run Admin API (`run.googleapis.com`)
    -   Artifact Registry API (`artifactregistry.googleapis.com`) or Container Registry

    Enable them using:
    ```bash
    gcloud services enable cloudbuild.googleapis.com run.googleapis.com artifactregistry.googleapis.com
    ```

## Deployment

To deploy the application, simply run the `deploy_cloud_run.sh` script:

```bash
./deploy_cloud_run.sh
```

This script will:
1.  Verify `gcloud` is installed.
2.  Check for the active Google Cloud Project ID.
3.  **Build** the Docker image using Google Cloud Build (no local Docker required).
4.  **Deploy** the image to a Cloud Run service named `dundra-adk-agent`.

### Configuration

You can customize the deployment by editing `deploy_cloud_run.sh`:
-   `SERVICE_NAME`: The name of the Cloud Run service.
-   `REGION`: The region to deploy to (default: `us-central1`).

## Troubleshooting

-   **Docker not found**: The script uses Cloud Build, so local Docker installation is **not** required.
-   **Permission Denied**: Ensure your user account has the `Cloud Build Editor` and `Cloud Run Admin` roles.
-   **Environment Variables**: The script sets `GCS_BUCKET_NAME` from your local environment. Ensure it is exported before running the script if needed:
    ```bash
    export GCS_BUCKET_NAME=your-bucket-name
    ./deploy_cloud_run.sh
    ```
