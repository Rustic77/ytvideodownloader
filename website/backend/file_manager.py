"""
File manager for handling temporary downloads with expiring links.
"""
import os
import time
import uuid
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime, timedelta
import asyncio


class FileManager:
    """Manages temporary download files with token-based access and expiration."""
    
    def __init__(self, download_dir: str = "downloads", expiry_hours: int = 1):
        """
        Initialize the file manager.
        
        Args:
            download_dir: Directory for temporary downloads
            expiry_hours: Hours until files/tokens expire
        """
        self.download_dir = download_dir
        self.expiry_hours = expiry_hours
        self.expiry_seconds = expiry_hours * 3600
        
        # Token storage: token -> {filepath, created_at, downloaded, original_filename}
        self.tokens: Dict[str, Dict] = {}
        
        # Job storage: job_id -> {status, progress, filepath, error, token}
        self.jobs: Dict[str, Dict] = {}
        
        # Create download directory
        os.makedirs(download_dir, exist_ok=True)
        
    def create_job(self) -> str:
        """
        Create a new download job.
        
        Returns:
            Job ID
        """
        job_id = str(uuid.uuid4())
        self.jobs[job_id] = {
            'status': 'pending',  # pending, processing, completed, failed
            'progress': 0,
            'filepath': None,
            'error': None,
            'token': None,
            'created_at': time.time(),
        }
        return job_id
    
    def update_job(self, job_id: str, **kwargs):
        """Update job status and information."""
        if job_id in self.jobs:
            self.jobs[job_id].update(kwargs)
    
    def get_job(self, job_id: str) -> Optional[Dict]:
        """Get job information."""
        return self.jobs.get(job_id)
    
    def create_token(self, filepath: str, original_filename: str) -> str:
        """
        Create a download token for a file.
        
        Args:
            filepath: Path to the downloaded file
            original_filename: Original video title for download
        
        Returns:
            Download token
        """
        token = str(uuid.uuid4())
        self.tokens[token] = {
            'filepath': filepath,
            'created_at': time.time(),
            'downloaded': False,
            'original_filename': original_filename,
        }
        return token
    
    def get_file_by_token(self, token: str) -> Optional[Dict]:
        """
        Get file information by token.
        
        Args:
            token: Download token
        
        Returns:
            File info dict or None if token invalid/expired
        """
        if token not in self.tokens:
            return None
        
        token_info = self.tokens[token]
        
        # Check if token expired
        if time.time() - token_info['created_at'] > self.expiry_seconds:
            self.invalidate_token(token)
            return None
        
        # Check if already downloaded (one-time use)
        if token_info['downloaded']:
            return None
        
        # Check if file exists
        if not os.path.exists(token_info['filepath']):
            self.invalidate_token(token)
            return None
        
        return token_info
    
    def mark_downloaded(self, token: str):
        """Mark a token as used (downloaded)."""
        if token in self.tokens:
            self.tokens[token]['downloaded'] = True
    
    def invalidate_token(self, token: str):
        """Remove a token from valid tokens."""
        if token in self.tokens:
            del self.tokens[token]
    
    def cleanup_old_files(self):
        """Remove expired files and tokens."""
        current_time = time.time()
        
        # Clean up expired tokens
        expired_tokens = []
        for token, info in self.tokens.items():
            if current_time - info['created_at'] > self.expiry_seconds:
                expired_tokens.append(token)
                # Delete the file
                try:
                    if os.path.exists(info['filepath']):
                        os.remove(info['filepath'])
                except Exception as e:
                    print(f"Error deleting file {info['filepath']}: {e}")
        
        for token in expired_tokens:
            del self.tokens[token]
        
        # Clean up old jobs (keep for 24 hours)
        job_expiry = 24 * 3600
        expired_jobs = []
        for job_id, job_info in self.jobs.items():
            if current_time - job_info['created_at'] > job_expiry:
                expired_jobs.append(job_id)
        
        for job_id in expired_jobs:
            del self.jobs[job_id]
        
        # Clean up orphaned files in download directory
        try:
            for filename in os.listdir(self.download_dir):
                filepath = os.path.join(self.download_dir, filename)
                if os.path.isfile(filepath):
                    file_age = current_time - os.path.getctime(filepath)
                    if file_age > self.expiry_seconds:
                        try:
                            os.remove(filepath)
                        except Exception as e:
                            print(f"Error deleting orphaned file {filepath}: {e}")
        except Exception as e:
            print(f"Error cleaning up download directory: {e}")
        
        print(f"Cleanup complete: Removed {len(expired_tokens)} expired tokens, {len(expired_jobs)} old jobs")
    
    async def start_cleanup_task(self):
        """Background task to periodically clean up old files."""
        while True:
            await asyncio.sleep(900)  # Run every 15 minutes
            self.cleanup_old_files()


# Global file manager instance
file_manager = FileManager()

