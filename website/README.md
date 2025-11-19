# YouTube Video Downloader Website

A modern web application for downloading YouTube videos in various quality options (up to 4K). Built with FastAPI backend and vanilla JavaScript frontend, featuring temporary download links and Google AdSense integration.

## Features

- 🎬 **HD Quality Downloads**: Support for 4K, 2K, 1080p, 720p, 480p
- ⚡ **Fast Processing**: Parallel fragment downloads for maximum speed
- 🔒 **Secure**: Temporary download links that expire after use or 1 hour
- 📱 **Responsive Design**: Works perfectly on desktop and mobile
- 💰 **Ad Ready**: Pre-integrated Google AdSense placeholder units
- 🗑️ **Auto Cleanup**: Automatic file deletion to save storage space

## Architecture

### Backend (FastAPI)
- **main.py** - FastAPI application with API endpoints
- **downloader.py** - YouTube video download logic using yt-dlp
- **file_manager.py** - Temporary file and token management

### Frontend (Vanilla JS)
- **index.html** - Main page with AdSense placeholders
- **style.css** - Modern, responsive styling
- **app.js** - Frontend logic for API interactions

### API Endpoints
- `POST /api/info` - Fetch video metadata
- `POST /api/download` - Start download job
- `GET /api/status/{job_id}` - Check download status
- `GET /api/file/{token}` - Download file with temporary token

## Prerequisites

- Python 3.11+
- FFmpeg (required for video processing)
- Git

## Local Development

### 1. Install Dependencies

```bash
cd website
pip install -r backend/requirements.txt
```

### 2. Install FFmpeg

**Windows:**
```bash
winget install ffmpeg
```

**Mac:**
```bash
brew install ffmpeg
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install ffmpeg
```

### 3. Run the Application

```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Visit http://localhost:8000 in your browser.

## Deployment

### Option 1: Railway.app (Recommended for Beginners)

Railway.app offers a generous free tier and is very easy to deploy.

**Steps:**

1. **Create Railway Account**
   - Go to https://railway.app
   - Sign up with GitHub

2. **Deploy from GitHub**
   - Push your code to GitHub
   - In Railway dashboard, click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository
   - Railway will auto-detect Python and deploy

3. **Configure Environment**
   - Railway automatically detects the `Procfile` or `railway.json`
   - No additional configuration needed
   - Your app will be live at `https://your-app.railway.app`

4. **Custom Domain (Optional)**
   - In Railway project settings, add your custom domain
   - Update DNS records as instructed

**Limitations:**
- Free tier: 500 hours/month, $5 credit
- Ephemeral storage (files deleted on restart)
- Aggressive cleanup recommended

### Option 2: Render.com

Render.com also offers a free tier with automatic deployments.

**Steps:**

1. **Create Render Account**
   - Go to https://render.com
   - Sign up with GitHub

2. **Create New Web Service**
   - Click "New +"
   - Select "Web Service"
   - Connect your GitHub repository

3. **Configure Build Settings**
   - **Build Command:** `pip install -r backend/requirements.txt`
   - **Start Command:** `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Environment:** Python 3

4. **Deploy**
   - Click "Create Web Service"
   - Render will build and deploy automatically
   - Your app will be live at `https://your-app.onrender.com`

**Limitations:**
- Free tier: Services spin down after 15 minutes of inactivity
- Cold starts can take 30+ seconds
- 750 hours/month free

### Option 3: Heroku

Heroku is reliable but no longer offers a completely free tier ($5/month minimum).

**Steps:**

1. Install Heroku CLI
2. Login: `heroku login`
3. Create app: `heroku create your-app-name`
4. Deploy: `git push heroku main`
5. Set buildpack: `heroku buildpacks:set heroku/python`

### Important Deployment Notes

#### Storage Considerations
All free hosting platforms use **ephemeral storage**:
- Downloaded files are deleted when the server restarts
- This is why the app uses aggressive cleanup (1-hour expiration)
- For production/high-traffic use, consider using AWS S3 or similar cloud storage

#### FFmpeg Installation
Most Python hosting platforms include FFmpeg by default. If not:
- Railway/Render: Use a `nixpacks.toml` or `Aptfile` to install FFmpeg
- Create `Aptfile` in root directory:
  ```
  ffmpeg
  ```

#### Environment Variables
No environment variables are required for basic functionality. Optional:
- `DOWNLOAD_EXPIRY_HOURS` - Hours until files expire (default: 1)
- `PORT` - Port number (automatically set by hosting platforms)

## Google AdSense Integration

The website includes placeholder ad units that you need to replace with your actual AdSense code.

### Setup Steps:

1. **Apply for Google AdSense**
   - Go to https://www.google.com/adsense
   - Apply for an account (requires domain and content)
   - Wait for approval (can take days to weeks)

2. **Create Ad Units**
   - In AdSense dashboard, go to "Ads" → "By ad unit"
   - Create three ad units:
     - **Header Banner**: Display ad (728x90 or responsive)
     - **Sidebar**: Display ad (160x600 or responsive)
     - **In-content**: Display ad (300x250 or responsive)

3. **Replace Placeholder Code**
   - Open `website/static/index.html`
   - Find all instances of `ca-pub-XXXXXXXXXXXXXXXX`
   - Replace with your actual AdSense publisher ID
   - Replace `data-ad-slot="XXXXXXXXXX"` with your actual ad slot IDs

4. **Example AdSense Code:**
   ```html
   <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-1234567890123456"
        crossorigin="anonymous"></script>
   
   <ins class="adsbygoogle"
        style="display:block"
        data-ad-client="ca-pub-1234567890123456"
        data-ad-slot="9876543210"
        data-ad-format="auto"
        data-full-width-responsive="true"></ins>
   <script>
        (adsbygoogle = window.adsbygoogle || []).push({});
   </script>
   ```

### Ad Placement Best Practices:
- Header ad: High visibility, first thing users see
- Sidebar ad: Visible during interaction
- In-content ad: Natural placement after main content
- Don't use too many ads (can hurt user experience and SEO)

### Testing Ads:
- AdSense won't show real ads on localhost
- Deploy to production to see actual ads
- Use AdSense "Test Mode" during development

## Legal & Compliance

### Important Warnings:

⚠️ **YouTube Terms of Service**
- Downloading YouTube videos may violate YouTube's Terms of Service
- This tool is for educational purposes and personal use only
- Use at your own risk

⚠️ **Copyright**
- Respect copyright laws
- Only download content you have rights to
- Consider adding a DMCA takedown policy if publicly hosted

⚠️ **Privacy Policy & Terms**
- If monetizing with ads, you'll need:
  - Privacy Policy (required by AdSense)
  - Terms of Service
  - Cookie notice (GDPR compliance)

### Recommended Legal Pages:
Create these pages before AdSense approval:
- Privacy Policy (use generators like https://www.privacypolicygenerator.info/)
- Terms of Service
- DMCA Policy (if in the US)
- Contact page

## Rate Limiting & Abuse Prevention

For production, consider adding:
- Rate limiting (e.g., using `slowapi`)
- CAPTCHA for download requests
- User authentication for premium features
- File size limits
- IP-based throttling

Example rate limiting:
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/api/download")
@limiter.limit("5/minute")  # 5 downloads per minute per IP
async def start_download(...):
    ...
```

## Scaling Considerations

As your site grows, you'll need:

1. **Paid Hosting**
   - Railway Pro: $20/month
   - Render Standard: $7/month
   - DigitalOcean Droplet: $6/month
   - AWS EC2: Variable

2. **Cloud Storage**
   - AWS S3 for temporary file storage
   - Cloudflare R2 (S3-compatible, cheaper)

3. **CDN**
   - Cloudflare for caching static assets
   - Reduces bandwidth costs

4. **Database**
   - PostgreSQL for job persistence
   - Redis for caching and queues

5. **Job Queue**
   - Celery + Redis for background processing
   - Handles multiple simultaneous downloads

## Monitoring & Analytics

Consider adding:
- Google Analytics (for traffic monitoring)
- Sentry (for error tracking)
- Custom logging for download statistics

## Troubleshooting

### FFmpeg Not Found
```
Error: FFmpeg not detected
Solution: Install FFmpeg (see Prerequisites section)
```

### Videos Failing to Download
```
Common causes:
- Age-restricted videos (require authentication)
- Private/unlisted videos
- Region-restricted content
- yt-dlp needs updating: pip install --upgrade yt-dlp
```

### Server Crashes on Large Videos
```
Solution:
- Increase server memory
- Add file size limits in downloader.py
- Implement streaming downloads instead of full download
```

### Files Not Cleaning Up
```
Check:
- Cleanup task is running (check logs)
- File permissions are correct
- Disk space is available
```

## Updating yt-dlp

YouTube frequently changes their API. Keep yt-dlp updated:

```bash
pip install --upgrade yt-dlp
```

For production, update regularly via your deployment pipeline.

## Support & Contributing

This is a personal project for educational purposes. Use responsibly and respect copyright laws.

## License

This project is for educational purposes only. The user assumes all legal responsibility for their use of this software.

---

**Happy Downloading! 🎬**

