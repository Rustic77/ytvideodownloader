# Railway Deployment Instructions

## Method 1: Automatic Deployment (Recommended)

1. **Push your code to GitHub:**
   ```bash
   git add .
   git commit -m "Setup YouTube downloader for Railway"
   git push
   ```

2. **Go to Railway:**
   - Visit: https://railway.app
   - Click "Login" → Login with GitHub

3. **Create New Project:**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository

4. **Configure Root Directory (IMPORTANT!):**
   - After deployment starts, click on your service
   - Go to "Settings" tab
   - Scroll to "Root Directory"
   - Set it to: `website`
   - Click "Save"

5. **Redeploy:**
   - Railway will automatically rebuild with the correct directory
   - Wait 2-3 minutes

6. **Get Your URL:**
   - Go to "Settings" → "Domains"
   - Click "Generate Domain"
   - Your URL: `https://your-app.up.railway.app`

## Method 2: Manual Configuration

If Railway doesn't detect the root directory automatically:

1. In Railway dashboard, go to your service
2. Click "Settings"
3. Find "Root Directory" and set to: `website`
4. Find "Install Command" and verify: `pip install -r backend/requirements.txt`
5. Find "Start Command" and verify: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Click "Deploy" to rebuild

## Verify Deployment

Once deployed, test these URLs:

- Homepage: `https://your-app.up.railway.app/`
- Health check: `https://your-app.up.railway.app/health`
- Privacy Policy: `https://your-app.up.railway.app/static/privacy.html`

## Troubleshooting

**Error: "Module not found"**
- Make sure Root Directory is set to `website`
- Check that requirements.txt path is `backend/requirements.txt`

**Error: "FFmpeg not found"**
- FFmpeg is included in nixpacks.toml
- Should install automatically

**Error: "Port already in use"**
- Railway sets $PORT automatically
- Don't hardcode port 8000

**Static files not loading:**
- Verify Root Directory = `website`
- Check that static/ folder is in website/ directory

## Environment Variables

No environment variables needed for basic deployment!
Railway automatically sets:
- `PORT` - Server port
- `RAILWAY_ENVIRONMENT` - Deployment environment

## File Structure for Railway

Railway will see:
```
website/               ← Root Directory
├── backend/
│   ├── main.py
│   ├── downloader.py
│   ├── file_manager.py
│   └── requirements.txt  ← Install from here
├── static/
│   ├── index.html
│   ├── css/
│   └── js/
└── downloads/         ← Temporary storage
```

## After Successful Deployment

1. Copy your Railway URL
2. Go to Google Analytics
3. Update your data stream URL
4. Start tracking visitors!

## Cost

- Free tier: $5 credit/month
- Your app should stay within free tier limits
- Monitor usage in Railway dashboard

---

**Need help?** Check the main README.md or Railway documentation.

