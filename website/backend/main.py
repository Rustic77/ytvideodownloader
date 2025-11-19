"""
FastAPI backend for YouTube video downloader web application.
"""
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
from typing import Optional
import os
import uvicorn
from contextlib import asynccontextmanager

from file_manager import file_manager
from downloader import get_video_info, download_video


# Lifespan context manager for startup/shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Start cleanup task
    import asyncio
    cleanup_task = asyncio.create_task(file_manager.start_cleanup_task())
    yield
    # Shutdown: Cancel cleanup task
    cleanup_task.cancel()
    try:
        await cleanup_task
    except asyncio.CancelledError:
        pass


# Initialize FastAPI app
app = FastAPI(
    title="YouTube Video Downloader",
    description="Download YouTube videos with temporary expiring links",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
static_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
app.mount("/static", StaticFiles(directory=static_path), name="static")


# Request/Response models
class VideoInfoRequest(BaseModel):
    url: str


class DownloadRequest(BaseModel):
    url: str
    quality: str = "1080p"


class VideoInfoResponse(BaseModel):
    success: bool
    title: Optional[str] = None
    duration: Optional[int] = None
    thumbnail: Optional[str] = None
    uploader: Optional[str] = None
    error: Optional[str] = None


class DownloadResponse(BaseModel):
    success: bool
    job_id: Optional[str] = None
    message: Optional[str] = None
    error: Optional[str] = None


class JobStatusResponse(BaseModel):
    status: str  # pending, processing, completed, failed
    progress: int
    token: Optional[str] = None
    error: Optional[str] = None


# Routes
@app.get("/")
async def root():
    """Serve the main HTML page."""
    html_path = os.path.join(static_path, "index.html")
    return FileResponse(html_path)


@app.post("/api/info", response_model=VideoInfoResponse)
async def get_info(request: VideoInfoRequest):
    """
    Get video information without downloading.
    
    Args:
        request: Video URL
    
    Returns:
        Video metadata
    """
    try:
        info = await get_video_info(request.url)
        
        if info['success']:
            return VideoInfoResponse(
                success=True,
                title=info['title'],
                duration=info['duration'],
                thumbnail=info['thumbnail'],
                uploader=info['uploader']
            )
        else:
            return VideoInfoResponse(
                success=False,
                error=info['error']
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/download", response_model=DownloadResponse)
async def start_download(request: DownloadRequest, background_tasks: BackgroundTasks):
    """
    Start a video download job.
    
    Args:
        request: Download request with URL and quality
        background_tasks: FastAPI background tasks
    
    Returns:
        Job ID for tracking download progress
    """
    try:
        # Create a new job
        job_id = file_manager.create_job()
        
        # Start download in background
        background_tasks.add_task(
            process_download,
            request.url,
            request.quality,
            job_id
        )
        
        return DownloadResponse(
            success=True,
            job_id=job_id,
            message="Download started"
        )
    except Exception as e:
        return DownloadResponse(
            success=False,
            error=str(e)
        )


async def process_download(url: str, quality: str, job_id: str):
    """
    Background task to process video download.
    
    Args:
        url: YouTube video URL
        quality: Video quality
        job_id: Job identifier
    """
    try:
        # Update job status
        print(f"[{job_id}] Starting download for: {url}")
        file_manager.update_job(job_id, status='processing', progress=10)
        
        # Get video info first
        print(f"[{job_id}] Fetching video info...")
        info = await get_video_info(url)
        if not info['success']:
            error_msg = info['error']
            print(f"[{job_id}] Failed to get video info: {error_msg}")
            file_manager.update_job(
                job_id,
                status='failed',
                error=error_msg
            )
            return
        
        video_title = info['title']
        print(f"[{job_id}] Video: {video_title}")
        file_manager.update_job(job_id, progress=25)
        
        # Download video
        print(f"[{job_id}] Starting download (quality: {quality})...")
        success, message, filepath = await download_video(
            url,
            file_manager.download_dir,
            quality,
            job_id
        )
        
        if success and filepath:
            print(f"[{job_id}] Download successful: {filepath}")
            # Create download token
            token = file_manager.create_token(filepath, video_title)
            file_manager.update_job(
                job_id,
                status='completed',
                progress=100,
                filepath=filepath,
                token=token
            )
            print(f"[{job_id}] Token created: {token}")
        else:
            print(f"[{job_id}] Download failed: {message}")
            file_manager.update_job(
                job_id,
                status='failed',
                error=message
            )
    except Exception as e:
        error_msg = str(e)
        print(f"[{job_id}] Exception occurred: {error_msg}")
        import traceback
        traceback.print_exc()
        file_manager.update_job(
            job_id,
            status='failed',
            error=error_msg
        )


@app.get("/api/status/{job_id}", response_model=JobStatusResponse)
async def get_job_status(job_id: str):
    """
    Get the status of a download job.
    
    Args:
        job_id: Job identifier
    
    Returns:
        Job status and download token if completed
    """
    job = file_manager.get_job(job_id)
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return JobStatusResponse(
        status=job['status'],
        progress=job['progress'],
        token=job.get('token'),
        error=job.get('error')
    )


@app.get("/api/file/{token}")
async def download_file(token: str):
    """
    Download a file using a temporary token.
    
    Args:
        token: Download token
    
    Returns:
        File for download
    """
    file_info = file_manager.get_file_by_token(token)
    
    if not file_info:
        raise HTTPException(
            status_code=404,
            detail="File not found or link expired"
        )
    
    filepath = file_info['filepath']
    original_filename = file_info['original_filename']
    
    # Mark as downloaded (one-time use)
    file_manager.mark_downloaded(token)
    
    # Generate safe filename
    safe_filename = "".join(c for c in original_filename if c.isalnum() or c in (' ', '-', '_')).rstrip()
    safe_filename = safe_filename[:200]  # Limit length
    if not safe_filename.endswith('.mp4'):
        safe_filename += '.mp4'
    
    return FileResponse(
        filepath,
        media_type='video/mp4',
        filename=safe_filename,
        headers={
            "Content-Disposition": f'attachment; filename="{safe_filename}"'
        }
    )


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

