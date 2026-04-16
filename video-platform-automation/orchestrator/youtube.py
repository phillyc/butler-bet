"""
YouTube API wrapper for video upload.
"""

import logging
import os
from pathlib import Path
from typing import Optional, Dict, Any

# Import YouTube API client
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

logger = logging.getLogger(__name__)


class YouTubeUploader:
    """Upload videos to YouTube via API."""
    
    SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
    
    def __init__(self, credentials_path: str = None):
        """
        Initialize YouTube uploader.
        
        Args:
            credentials_path: Path to OAuth credentials JSON
        """
        self.credentials_path = credentials_path or 'credentials.json'
        self._service = None
        logger.info("YouTubeUploader initialized")
    
    @property
    def service(self):
        """Lazy load YouTube API service."""
        if self._service is None:
            logger.info("Authenticating with YouTube API...")
            self._service = self._get_authenticated_service()
            logger.info("YouTube API authenticated")
        
        return self._service
    
    def _get_authenticated_service(self):
        """Get authenticated YouTube API service."""
        creds = None
        
        # Try token first
        if os.path.exists('token.json'):
            creds = None  # Would load from token.json
        
        # If no valid credentials, get new ones
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                # Use OAuth flow (requires credentials.json in Google Cloud Console)
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, self.SCOPES
                )
                creds = flow.run_local_server(port=0)
            
            # Save credentials
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        
        return build('youtube', 'v3', credentials=creds)
    
    def upload(
        self,
        video_path: str,
        title: str,
        description: str,
        tags: list,
        privacy_status: str = 'private',
        category_id: str = '22'
    ) -> Dict[str, Any]:
        """
        Upload video to YouTube.
        
        Args:
            video_path: Path to video file
            title: Video title
            description: Video description
            tags: List of tags
            privacy_status: 'private', 'unlisted', or 'public'
            category_id: YouTube category ID
            
        Returns:
            Upload result dict with video_id and url
        """
        logger.info(f"Uploading video: {title}")
        
        # Prepare video metadata
        video_file = Path(video_path)
        
        # Create upload request
        request_body = {
            'snippet': {
                'title': title,
                'description': description,
                'tags': tags,
                'categoryId': category_id
            },
            'status': {
                'privacyStatus': privacy_status,
                'madeForKids': False
            }
        }
        
        # Upload video
        media = MediaFileUpload(str(video_file), chunksize=1024*1024, resumable=True)
        
        response = self.service.videos().insert(
            part='snippet,status',
            body=request_body,
            media_body=media
        )
        
        # Handle resumable upload
        upload_response = None
        while upload_response is None:
            status, upload_response = response.next_chunk()
            if status:
                logger.info(f"Uploaded {int(status.progress() * 100)}%")
        
        # Extract video info
        video_id = upload_response['id']
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        
        logger.info(f"Upload successful: {video_url}")
        
        return {
            'video_id': video_id,
            'url': video_url,
            'title': title,
            'privacy_status': privacy_status
        }
