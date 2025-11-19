"""
YouTube video downloader core functionality using yt-dlp.
Adapted from the original youtube_downloader.py for web usage.
"""
import yt_dlp
import os
import uuid
from pathlib import Path
from typing import Dict, Optional, Tuple
import asyncio
from concurrent.futures import ThreadPoolExecutor


# Thread pool for running blocking yt-dlp operations
executor = ThreadPoolExecutor(max_workers=4)


def get_format_string(quality: str) -> str:
    """
    Get the format string based on selected quality.
    
    Args:
        quality: Quality setting (e.g., '1080p', '720p', '480p', 'best')
    
    Returns:
        Format string for yt-dlp
    """
    quality_map = {
        "2160p": 2160,
        "1440p": 1440,
        "1080p": 1080,
        "720p": 720,
        "480p": 480,
        "best": 9999
    }
    
    height = quality_map.get(quality.lower(), 1080)
    
    if height == 9999:
        return 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best'
    else:
        return f'bestvideo[height<={height}][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<={height}]+bestaudio/best[height<={height}]/best'


def _sync_get_video_info(url: str) -> Dict:
    """
    Synchronous function to get video information.
    
    Args:
        url: YouTube video URL
    
    Returns:
        Dictionary with video metadata
    """
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            return {
                'success': True,
                'title': info.get('title', 'Unknown'),
                'duration': info.get('duration', 0),
                'thumbnail': info.get('thumbnail', ''),
                'uploader': info.get('uploader', 'Unknown'),
                'view_count': info.get('view_count', 0),
                'upload_date': info.get('upload_date', ''),
            }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


async def get_video_info(url: str) -> Dict:
    """
    Get video information without downloading.
    
    Args:
        url: YouTube video URL
    
    Returns:
        Dictionary with video metadata or error
    """
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, _sync_get_video_info, url)


def _sync_download_video(url: str, output_path: str, quality: str, job_id: str) -> Tuple[bool, str, Optional[str]]:
    """
    Synchronous function to download video.
    
    Args:
        url: YouTube video URL
        output_path: Directory to save video
        quality: Quality setting
        job_id: Unique job identifier
    
    Returns:
        Tuple of (success, message, filepath)
    """
    try:
        # Create output directory if it doesn't exist
        os.makedirs(output_path, exist_ok=True)
        
        # Generate unique filename
        filename = f"{job_id}.mp4"
        output_template = os.path.join(output_path, filename)
        
        ydl_opts = {
            'format': get_format_string(quality),
            'outtmpl': output_template,
            'merge_output_format': 'mp4',
            
            # Speed optimizations
            'concurrent_fragment_downloads': 8,
            'http_chunk_size': 10485760,  # 10MB chunks
            'retries': 10,
            'fragment_retries': 10,
            'buffersize': 1024 * 1024 * 2,  # 2MB buffer
            
            'prefer_free_formats': False,
            
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            }],
            
            'quiet': True,
            'no_warnings': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        # Find the actual output file (yt-dlp might have added extra extensions)
        output_file = output_template
        if not os.path.exists(output_file):
            # Check for common variations
            possible_files = [
                output_template,
                output_template.replace('.mp4', '.mp4.mp4'),
                output_template.replace('.mp4', '.webm'),
            ]
            for pf in possible_files:
                if os.path.exists(pf):
                    output_file = pf
                    break
        
        if os.path.exists(output_file):
            return True, "Download completed successfully", output_file
        else:
            return False, "Download completed but file not found", None
            
    except Exception as e:
        return False, f"Download failed: {str(e)}", None


async def download_video(url: str, output_path: str, quality: str, job_id: str) -> Tuple[bool, str, Optional[str]]:
    """
    Download video asynchronously.
    
    Args:
        url: YouTube video URL
        output_path: Directory to save video
        quality: Quality setting
        job_id: Unique job identifier
    
    Returns:
        Tuple of (success, message, filepath)
    """
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, _sync_download_video, url, output_path, quality, job_id)

