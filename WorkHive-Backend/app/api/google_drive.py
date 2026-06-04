from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import uuid
import logging
from jose import jwt
from datetime import datetime, timedelta, timezone
from app.core.database import get_db
from app.core.config import settings
from app.models.user import User
from app.api.auth import get_current_user
from google_auth_oauthlib.flow import Flow

router = APIRouter(prefix="/api/v1/google-drive", tags=["google-drive"])
logger = logging.getLogger(__name__)


@router.get("/auth-url")
async def get_auth_url(current_user: User = Depends(get_current_user)):
    """Generate Google OAuth URL for Drive access with a signed state parameter"""
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [settings.GOOGLE_REDIRECT_URI]
            }
        },
        scopes=['https://www.googleapis.com/auth/drive.file']
    )
    
    flow.redirect_uri = settings.GOOGLE_REDIRECT_URI
    
    # Generate secure, signed state containing user ID and expiration
    state_payload = {
        "user_id": str(current_user.id),
        "nonce": uuid.uuid4().hex,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=10)
    }
    signed_state = jwt.encode(state_payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    
    authorization_url, state = flow.authorization_url(
        state=signed_state,
        access_type='offline',
        include_granted_scopes='true',
        prompt='consent'
    )
    
    return {"auth_url": authorization_url, "state": state}


@router.post("/callback")
async def oauth_callback(
    code: str,
    state: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Handle Google OAuth callback, validate state, and store tokens"""
    # Validate the state parameter to prevent CSRF
    try:
        payload = jwt.decode(state, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        if payload.get("user_id") != str(current_user.id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="OAuth state verification failed: user mismatch"
            )
    except Exception as e:
        logger.warning(f"OAuth state validation failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="OAuth state verification failed: invalid or expired state"
        )

    try:
        flow = Flow.from_client_config(
            {
                "web": {
                    "client_id": settings.GOOGLE_CLIENT_ID,
                    "client_secret": settings.GOOGLE_CLIENT_SECRET,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "redirect_uris": [settings.GOOGLE_REDIRECT_URI]
                }
            },
            scopes=['https://www.googleapis.com/auth/drive.file']
        )
        
        flow.redirect_uri = settings.GOOGLE_REDIRECT_URI
        flow.fetch_token(code=code)
        
        credentials = flow.credentials
        
        # Store tokens in database
        current_user.google_drive_token = credentials.token
        current_user.google_drive_refresh_token = credentials.refresh_token
        
        db.commit()
        
        return {"message": "Google Drive connected successfully"}
    except Exception as e:
        logger.error(f"Failed to connect Google Drive: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to connect Google Drive. Please try again."
        )


@router.post("/disconnect")
async def disconnect_drive(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Disconnect Google Drive account"""
    current_user.google_drive_token = None
    current_user.google_drive_refresh_token = None
    
    db.commit()
    
    return {"message": "Google Drive disconnected successfully"}


@router.get("/status")
async def get_drive_status(current_user: User = Depends(get_current_user)):
    """Check if Google Drive is connected"""
    return {
        "connected": bool(current_user.google_drive_token)
    }
