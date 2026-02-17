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
    except Exception as e:
        logger.error(f"Authentication error: {e}")
        raise HTTPException(status_code=401, detail="Authentication failed")

async def verify_user_query_token(request: Request):
    """
    Verifies the Firebase ID token from the 'token' query parameter.
    Used for iframes where custom headers cannot be set easily.
    """
    token = request.query_params.get("token")
    print(f"DEBUG: verify_user_query_token called. URL: {request.url}")
    print(f"DEBUG: verify_user_query_token query params: {request.query_params}")
    
    if not token:
        print("DEBUG: Token missing in query params")
        raise HTTPException(status_code=401, detail="Missing authentication token")
    
    # Create a dummy credentials object to reuse verify_user logic if possible,
    # or just call the logic directly. 
    # Let's just call the logic directly to avoid complexity.
    try:
        decoded_token = auth.verify_id_token(token)
        email = decoded_token.get("email")
        
        if not email:
             raise HTTPException(status_code=401, detail="Invalid token: No email found")

        if email != ALLOWED_EMAIL:
            logger.warning(f"Unauthorized access attempt by: {email}")
            raise HTTPException(status_code=403, detail=f"Access denied for {email}")

        return decoded_token
    except Exception as e:
        logger.error(f"Query token verification failed: {e}")
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
async def get_current_user_email(request: Request):
    # This is a helper if we just want the email and we aren't using the dependency directly in the route signature
    # for some reason, but usually we use verify_user
    pass
