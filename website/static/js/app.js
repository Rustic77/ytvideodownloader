// YouTube Downloader Frontend Logic

const API_BASE = '';  // Empty string uses same origin
let currentJobId = null;
let currentVideoUrl = null;
let pollingInterval = null;

// DOM Elements
const videoUrlInput = document.getElementById('video-url');
const qualitySelect = document.getElementById('quality');
const getInfoBtn = document.getElementById('get-info-btn');
const downloadBtn = document.getElementById('download-btn');
const newDownloadBtn = document.getElementById('new-download-btn');
const retryBtn = document.getElementById('retry-btn');

const videoInfoSection = document.getElementById('video-info');
const progressSection = document.getElementById('progress-section');
const downloadReadySection = document.getElementById('download-ready');
const errorSection = document.getElementById('error-section');

const videoThumbnail = document.getElementById('video-thumbnail');
const videoTitle = document.getElementById('video-title');
const videoUploader = document.getElementById('video-uploader');
const videoDuration = document.getElementById('video-duration');

const progressFill = document.getElementById('progress-fill');
const progressText = document.getElementById('progress-text');
const errorMessage = document.getElementById('error-message');
const downloadLink = document.getElementById('download-link');

// Event Listeners
getInfoBtn.addEventListener('click', handleGetInfo);
downloadBtn.addEventListener('click', handleDownload);
newDownloadBtn.addEventListener('click', resetForm);
retryBtn.addEventListener('click', resetForm);

// Allow Enter key in URL input to trigger get info
videoUrlInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        e.preventDefault();
        handleGetInfo();
    }
});

// Format duration (seconds to MM:SS)
function formatDuration(seconds) {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
}

// Show error
function showError(message) {
    hideAllSections();
    errorSection.classList.remove('hidden');
    errorMessage.textContent = message;
}

// Hide all dynamic sections
function hideAllSections() {
    videoInfoSection.classList.add('hidden');
    progressSection.classList.add('hidden');
    downloadReadySection.classList.add('hidden');
    errorSection.classList.add('hidden');
}

// Reset form
function resetForm() {
    hideAllSections();
    videoUrlInput.value = '';
    currentJobId = null;
    currentVideoUrl = null;
    if (pollingInterval) {
        clearInterval(pollingInterval);
        pollingInterval = null;
    }
    getInfoBtn.disabled = false;
    getInfoBtn.classList.remove('loading');
}

// Handle Get Info
async function handleGetInfo() {
    const url = videoUrlInput.value.trim();
    
    if (!url) {
        showError('Please enter a YouTube video URL');
        return;
    }
    
    // Basic URL validation
    if (!url.includes('youtube.com') && !url.includes('youtu.be')) {
        showError('Please enter a valid YouTube URL');
        return;
    }
    
    currentVideoUrl = url;
    hideAllSections();
    
    // Show loading state
    getInfoBtn.disabled = true;
    getInfoBtn.classList.add('loading');
    getInfoBtn.textContent = 'Fetching info...';
    
    try {
        const response = await fetch(`${API_BASE}/api/info`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url: url })
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Display video info
            videoThumbnail.src = data.thumbnail;
            videoTitle.textContent = data.title;
            videoUploader.textContent = data.uploader;
            videoDuration.textContent = formatDuration(data.duration);
            
            videoInfoSection.classList.remove('hidden');
        } else {
            showError(data.error || 'Failed to fetch video information');
        }
    } catch (error) {
        showError(`Network error: ${error.message}`);
    } finally {
        getInfoBtn.disabled = false;
        getInfoBtn.classList.remove('loading');
        getInfoBtn.textContent = 'Get Video Info';
    }
}

// Handle Download
async function handleDownload() {
    const quality = qualitySelect.value;
    
    hideAllSections();
    progressSection.classList.remove('hidden');
    
    progressFill.style.width = '0%';
    progressText.textContent = 'Starting download...';
    
    downloadBtn.disabled = true;
    
    try {
        // Start download job
        const response = await fetch(`${API_BASE}/api/download`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                url: currentVideoUrl,
                quality: quality
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            currentJobId = data.job_id;
            // Start polling for status
            startPolling();
        } else {
            showError(data.error || 'Failed to start download');
            downloadBtn.disabled = false;
        }
    } catch (error) {
        showError(`Network error: ${error.message}`);
        downloadBtn.disabled = false;
    }
}

// Start polling for job status
function startPolling() {
    pollingInterval = setInterval(async () => {
        try {
            const response = await fetch(`${API_BASE}/api/status/${currentJobId}`);
            const data = await response.json();
            
            updateProgress(data);
            
            if (data.status === 'completed') {
                clearInterval(pollingInterval);
                pollingInterval = null;
                showDownloadReady(data.token);
            } else if (data.status === 'failed') {
                clearInterval(pollingInterval);
                pollingInterval = null;
                showError(data.error || 'Download failed');
                downloadBtn.disabled = false;
            }
        } catch (error) {
            console.error('Polling error:', error);
        }
    }, 2000);  // Poll every 2 seconds
}

// Update progress display
function updateProgress(data) {
    const progress = data.progress || 0;
    progressFill.style.width = `${progress}%`;
    
    const statusMessages = {
        'pending': 'Waiting to start...',
        'processing': `Processing video... ${progress}%`,
        'completed': 'Download complete!',
        'failed': 'Download failed'
    };
    
    progressText.textContent = statusMessages[data.status] || 'Processing...';
}

// Show download ready with token
function showDownloadReady(token) {
    hideAllSections();
    downloadReadySection.classList.remove('hidden');
    
    // Set download link
    downloadLink.href = `${API_BASE}/api/file/${token}`;
    
    // Track click on download link to show message
    downloadLink.addEventListener('click', () => {
        setTimeout(() => {
            alert('Your download should start shortly. The link will expire after this download.');
        }, 500);
    });
}

// Initial state
hideAllSections();

