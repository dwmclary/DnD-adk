import os
import logging
import firebase_admin
from firebase_admin import credentials, auth
from fastapi import HTTPException, Security, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# Initialize logging
logger = logging.getLogger(__name__)

# Initialize Firebase Admin
# We assume ADC (Application Default Credentials) or GOOGLE_APPLICATION_CREDENTIALS
# are set up, which is standard for Cloud Run or local dev with gcloud auth application-default login.
try:
    if not firebase_admin._apps:
        firebase_admin.initialize_app()
    logger.info("Firebase Admin initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Firebase Admin: {e}")

security = HTTPBearer()

ALLOWED_EMAIL = "dan.mcclary@gmail.com"

async def verify_user(credentials: HTTPAuthorizationCredentials = Security(security)):
    """
    Verifies the Firebase ID token and ensures the user is allowed.
    """
    token = credentials.credentials
    try:
        decoded_token = auth.verify_id_token(token)
        email = decoded_token.get("email")
        
        if not email:
             raise HTTPException(status_code=401, detail="Invalid token: No email found")

        if email != ALLOWED_EMAIL:
            logger.warning(f"Unauthorized access attempt by: {email}")
            raise HTTPException(status_code=403, detail=f"Access denied for {email}")

        return decoded_token
    except ValueError as e:
        logger.error(f"Token verification failed: {e}")
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    except Exception as e:
        logger.error(f"Authentication error: {e}")
        raise HTTPException(status_code=401, detail="Authentication failed")

async def get_current_user_email(request: Request):
    # This is a helper if we just want the email and we aren't using the dependency directly in the route signature
    # for some reason, but usually we use verify_user
    pass
