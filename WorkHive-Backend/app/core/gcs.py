"""
Google Drive storage integration for WorkHive.
Files are stored in users' Google Drive accounts via OAuth.
This module is the storage abstraction layer — swap DriveService for a
GCS service account implementation in the future without touching the API layer.
"""
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload   # Fixed: was missing
import io
from app.core.config import settings


class DriveService:
    """
    Manages file storage using per-user Google Drive OAuth tokens.
    Each user authorises WorkHive to access their Drive; files are stored
    in a dedicated 'WorkHive' folder within that user's Drive.
    """
    SCOPES = ['https://www.googleapis.com/auth/drive.file']

    def _get_service(self, access_token: str, refresh_token: str = None, db = None, user = None):
        """Build an authenticated Drive service from stored OAuth tokens."""
        credentials = Credentials(
            token=access_token,
            refresh_token=refresh_token,
            token_uri="https://oauth2.googleapis.com/token",
            client_id=settings.GOOGLE_CLIENT_ID,
            client_secret=settings.GOOGLE_CLIENT_SECRET,
            scopes=self.SCOPES
        )
        
        # If token is invalid/expired and refresh token is present, refresh it explicitly and cache it
        if not credentials.valid and credentials.refresh_token:
            try:
                from google.auth.transport.requests import Request
                credentials.refresh(Request())
                if db and user:
                    user.google_drive_token = credentials.token
                    if credentials.refresh_token:
                        user.google_drive_refresh_token = credentials.refresh_token
                    db.commit()
            except Exception:
                pass
                
        return build('drive', 'v3', credentials=credentials)

    def upload_file(
        self,
        file_data: bytes,
        filename: str,
        content_type: str,
        access_token: str,
        refresh_token: str = None,
        folder_id: str = None,
        db = None,
        user = None
    ) -> str:
        """Upload bytes to Google Drive; return the Drive file ID."""
        service = self._get_service(access_token, refresh_token, db, user)

        file_metadata = {'name': filename}
        if folder_id:
            file_metadata['parents'] = [folder_id]

        media = MediaIoBaseUpload(
            io.BytesIO(file_data),
            mimetype=content_type,
            resumable=True
        )

        result = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()

        return result.get('id')

    def get_download_url(
        self,
        file_id: str,
        access_token: str,
        refresh_token: str = None,
        db = None,
        user = None
    ) -> str:
        """Return a direct download link for a Drive file."""
        service = self._get_service(access_token, refresh_token, db, user)
        file = service.files().get(
            fileId=file_id,
            fields='webContentLink'
        ).execute()
        return file.get('webContentLink', '')

    def delete_file(
        self,
        file_id: str,
        access_token: str,
        refresh_token: str = None,
        db = None,
        user = None
    ) -> None:
        """Permanently delete a file from Google Drive."""
        service = self._get_service(access_token, refresh_token, db, user)
        service.files().delete(fileId=file_id).execute()

    def create_workhive_folder(
        self,
        access_token: str,
        refresh_token: str = None,
        db = None,
        user = None
    ) -> str:
        """Create (or locate) a 'WorkHive' folder in the user's Drive; return folder ID."""
        service = self._get_service(access_token, refresh_token, db, user)

        # Search for existing folder first to avoid duplicates
        query = "name='WorkHive' and mimeType='application/vnd.google-apps.folder' and trashed=false"
        results = service.files().list(q=query, fields='files(id)').execute()
        existing = results.get('files', [])
        if existing:
            return existing[0]['id']

        # Create new folder
        folder_metadata = {
            'name': 'WorkHive',
            'mimeType': 'application/vnd.google-apps.folder'
        }
        folder = service.files().create(
            body=folder_metadata,
            fields='id'
        ).execute()
        return folder.get('id')


drive_service = DriveService()
