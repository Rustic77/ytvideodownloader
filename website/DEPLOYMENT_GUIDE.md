# Quick Deployment Guide

This guide will get your YouTube downloader website live in under 10 minutes.

## Prerequisites Checklist
- [ ] GitHub account
- [ ] Code pushed to a GitHub repository
- [ ] (Optional) Custom domain for AdSense

## Option 1: Railway.app (Easiest - Recommended)

### Step-by-Step Deployment

**1. Create Railway Account (1 minute)**
- Go to https://railway.app
- Click "Login with GitHub"
- Authorize Railway to access your repositories

**2. Create New Project (2 minutes)**
- Click "New Project"
- Select "Deploy from GitHub repo"
- Choose your youtube-downloader repository
- Railway will automatically detect it's a Python project

**3. Configure (1 minute)**
- Railway reads `Procfile` automatically
- No configuration needed!
- Wait for build to complete (~2-3 minutes)

**4. Get Your URL (1 minute)**
- Click on your service
- Go to "Settings" tab
- Under "Domains", click "Generate Domain"
- You'll get a URL like: `https://your-app.up.railway.app`

**5. Test Your Site**
- Visit your Railway URL
- Try downloading a video
- Check if everything works

**Total Time: ~5-7 minutes**

### Railway Free Tier Limits
- $5 credit per month
- ~500 hours of usage
- 512 MB RAM
- Ephemeral storage (files deleted on restart)

### Custom Domain on Railway (Optional)
1. Go to your service → Settings → Domains
2. Click "Custom Domain"
3. Enter your domain (e.g., `ytdownloader.com`)
4. Add CNAME record in your DNS:
   ```
   CNAME @ your-app.up.railway.app
   ```
5. Wait for DNS propagation (5-30 minutes)

---

## Option 2: Render.com

### Step-by-Step Deployment

**1. Create Render Account**
- Go to https://render.com
- Sign up with GitHub

**2. Create Web Service**
- Click "New +"
- Select "Web Service"
- Connect your repository

**3. Configure Build**
- **Name**: youtube-downloader
- **Region**: Choose closest to your users
- **Branch**: main
- **Root Directory**: (leave blank)
- **Build Command**: `pip install -r backend/requirements.txt`
- **Start Command**: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`

**4. Deploy**
- Click "Create Web Service"
- Wait 3-5 minutes for build
- Your URL: `https://youtube-downloader.onrender.com`

**Total Time: ~8-10 minutes**

### Render Free Tier Limits
- Services spin down after 15 min inactivity
- 750 hours/month
- Cold starts take 30-50 seconds

---

## Option 3: Manual VPS Deployment (Advanced)

For those who want full control on a VPS (DigitalOcean, Linode, etc.):

### Quick Setup Script

```bash
# SSH into your VPS
ssh user@your-server-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3 python3-pip python3-venv ffmpeg git -y

# Clone your repository
git clone https://github.com/yourusername/youtube-downloader.git
cd youtube-downloader/website

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r backend/requirements.txt

# Install process manager
pip install gunicorn

# Run with Gunicorn (production server)
cd backend
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Run as Background Service

Create systemd service `/etc/systemd/system/ytdownloader.service`:

```ini
[Unit]
Description=YouTube Downloader Web Service
After=network.target

[Service]
User=www-data
WorkingDirectory=/path/to/youtube-downloader/website/backend
Environment="PATH=/path/to/youtube-downloader/website/venv/bin"
ExecStart=/path/to/venv/bin/gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable ytdownloader
sudo systemctl start ytdownloader
```

### Setup Nginx Reverse Proxy

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## Post-Deployment Checklist

After deployment, verify:
- [ ] Homepage loads correctly
- [ ] "Get Video Info" button works
- [ ] Video download completes successfully
- [ ] Download link works (file downloads)
- [ ] Mobile responsive design works
- [ ] No console errors (F12 DevTools)

## Common Issues & Fixes

### Issue: "Module not found" error
**Fix**: Make sure `requirements.txt` is in the correct location and all packages are listed

### Issue: FFmpeg not found
**Fix**: Most platforms include FFmpeg. If not, add `Aptfile`:
```
ffmpeg
```

### Issue: Port already in use
**Fix**: Use `$PORT` environment variable (automatically set by hosting platforms)

### Issue: Files not downloading
**Fix**: 
1. Check server logs for errors
2. Verify yt-dlp is up to date
3. Test with different YouTube videos
4. Check if video is age-restricted or private

### Issue: Website loads slowly
**Fix**:
1. Enable gzip compression
2. Use a CDN (Cloudflare)
3. Optimize images
4. Minimize CSS/JS

### Issue: Downloads stop working after a while
**Fix**: YouTube changes their API frequently
```bash
# Update yt-dlp
pip install --upgrade yt-dlp
```

## Monitoring Your Site

### Railway Logs
```
Dashboard → Your Service → Deployments → View Logs
```

### Render Logs
```
Dashboard → Your Service → Logs tab
```

### Health Check
Both platforms auto-detect health via the `/health` endpoint.

## Updating Your Site

### Push to Git (Auto-Deploy)
```bash
# Make changes locally
git add .
git commit -m "Update feature"
git push

# Railway/Render will auto-deploy in 2-3 minutes
```

### Manual Redeploy
- **Railway**: Dashboard → Redeploy
- **Render**: Dashboard → Manual Deploy → Deploy latest commit

## Environment Variables (Optional)

If needed, set these in your hosting dashboard:

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | Auto-set | Server port (auto by platform) |
| `DOWNLOAD_EXPIRY_HOURS` | 1 | Hours until files expire |
| `PYTHON_VERSION` | 3.11.0 | Python version |

## Cost Estimates

### Railway.app
- **Free**: $5 credit/month
- **Developer**: $20/month (more resources)
- Best for: Starting out, low-medium traffic

### Render.com
- **Free**: 750 hours/month (with spin-down)
- **Starter**: $7/month (always on)
- Best for: Starting out, can handle spin-down

### VPS (DigitalOcean)
- **Basic Droplet**: $6/month
- **With backups**: $7/month
- Best for: Full control, consistent performance

### Scaling Costs (High Traffic)
- 10k users/day: ~$20-50/month
- 100k users/day: ~$200-500/month
- 1M users/day: ~$2000+/month (need CDN, load balancing)

## Next Steps

1. ✅ **Deploy your site** (using Railway or Render)
2. ✅ **Test thoroughly** (multiple videos, different qualities)
3. ✅ **Buy custom domain** ($10-15/year) - Required for AdSense
4. ✅ **Add legal pages** (Privacy Policy, Terms of Service)
5. ✅ **Apply for AdSense** (see ADSENSE_SETUP.md)
6. ✅ **Promote your site** (Reddit, Twitter, forums)
7. ✅ **Monitor performance** (check logs, fix issues)

## Getting Help

- **Railway Support**: https://help.railway.app
- **Render Support**: https://render.com/docs
- **yt-dlp Issues**: https://github.com/yt-dlp/yt-dlp/issues
- **FastAPI Docs**: https://fastapi.tiangolo.com

## Security Recommendations

Before going public:
1. Add rate limiting (prevent abuse)
2. Add CAPTCHA for downloads
3. Monitor bandwidth usage
4. Set file size limits
5. Add DMCA takedown policy
6. Consider user authentication for heavy users

---

**You're ready to go live! 🚀**

Questions? Check the main README.md for detailed information.

