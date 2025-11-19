# Google Analytics & AdSense Setup Guide

Quick guide to add Google Analytics and AdSense to your YouTube downloader website.

## 📊 STEP 1: Google Analytics Setup

Google Analytics is FREE and helps you track visitors, traffic sources, and user behavior.

### A. Create Google Analytics Account

1. **Go to Google Analytics**
   - Visit: https://analytics.google.com
   - Click "Start measuring" or "Sign in"
   - Use your Google account

2. **Create a Property**
   - Click "Admin" (bottom left gear icon)
   - Click "Create Property"
   - **Property name**: "YouTube Downloader" (or your site name)
   - **Reporting time zone**: Your timezone
   - **Currency**: Your currency
   - Click "Next"

3. **About Your Business**
   - **Industry**: Technology or Internet & Telecom
   - **Business size**: Small (or appropriate size)
   - Click "Next"

4. **Business Objectives**
   - Select "Generate leads" or "Examine user behavior"
   - Click "Create"

5. **Accept Terms of Service**
   - Check the boxes
   - Click "I Accept"

### B. Set Up Data Stream

1. **Choose Platform**
   - Click "Web"

2. **Set Up Web Stream**
   - **Website URL**: Your deployed URL (e.g., `https://your-app.railway.app`)
   - **Stream name**: "Main Website"
   - Click "Create stream"

3. **Copy Your Measurement ID**
   - You'll see: `G-XXXXXXXXXX` (like `G-ABC123DEF4`)
   - **Copy this ID** - you'll need it next

### C. Add Analytics Code to Your Site

1. **Open**: `website/static/index.html`

2. **Find this section** (near the top):
   ```html
   <!-- Google Analytics - Replace G-XXXXXXXXXX with your Measurement ID -->
   <script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
   <script>
       window.dataLayer = window.dataLayer || [];
       function gtag(){dataLayer.push(arguments);}
       gtag('js', new Date());
       gtag('config', 'G-XXXXXXXXXX');
   </script>
   ```

3. **Replace BOTH instances** of `G-XXXXXXXXXX` with your actual Measurement ID

   Example:
   ```html
   <!-- Google Analytics -->
   <script async src="https://www.googletagmanager.com/gtag/js?id=G-ABC123DEF4"></script>
   <script>
       window.dataLayer = window.dataLayer || [];
       function gtag(){dataLayer.push(arguments);}
       gtag('js', new Date());
       gtag('config', 'G-ABC123DEF4');
   </script>
   ```

4. **Save the file**

5. **Deploy your changes** (push to GitHub if using Railway/Render)

### D. Verify It's Working

1. **Visit your website**
2. **In Google Analytics**:
   - Go to Reports → Realtime
   - You should see yourself as "1 user right now"
   - May take 5-10 minutes to show up

✅ **Google Analytics is now tracking your site!**

---

## 💰 STEP 2: Google AdSense Setup

AdSense requires more steps and approval. This is where you'll make money from ads.

### A. Prerequisites (IMPORTANT!)

Before applying for AdSense, you MUST have:
- ✅ **Custom domain** (AdSense rejects free subdomains like `.railway.app`)
  - Buy domain: Namecheap, GoDaddy, etc. ($10-15/year)
  - Point it to your Railway/Render app
- ✅ **Privacy Policy page** (legally required)
- ✅ **Terms of Service page**
- ✅ **About/Contact page**
- ✅ **Original content** (your downloader counts)
- ✅ **Site is live and accessible**

### B. Create Legal Pages (Required)

You need to add these pages before applying:

**1. Create Privacy Policy**

Create file: `website/static/privacy.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Privacy Policy - YouTube Downloader</title>
    <link rel="stylesheet" href="/static/css/style.css">
</head>
<body>
    <div style="max-width: 800px; margin: 50px auto; padding: 20px;">
        <h1>Privacy Policy</h1>
        <p><strong>Last updated: November 2024</strong></p>
        
        <h2>Information We Collect</h2>
        <p>We collect analytics data through Google Analytics including IP addresses, browser type, and usage patterns.</p>
        
        <h2>How We Use Cookies</h2>
        <p>We use cookies for Google Analytics and Google AdSense advertising. These help us improve our service and show relevant ads.</p>
        
        <h2>Third-Party Services</h2>
        <p>We use Google AdSense which may collect data for personalized advertising. You can opt out at https://www.google.com/settings/ads</p>
        
        <h2>Data Retention</h2>
        <p>Downloaded videos are automatically deleted within 1 hour or after download. We do not store your videos permanently.</p>
        
        <h2>Contact</h2>
        <p>Email: your-email@example.com</p>
        
        <p><a href="/">Back to Home</a></p>
    </div>
</body>
</html>
```

Use a generator for a complete policy: https://www.privacypolicygenerator.info/

**2. Create Terms of Service**

Create file: `website/static/terms.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Terms of Service - YouTube Downloader</title>
    <link rel="stylesheet" href="/static/css/style.css">
</head>
<body>
    <div style="max-width: 800px; margin: 50px auto; padding: 20px;">
        <h1>Terms of Service</h1>
        
        <h2>Acceptable Use</h2>
        <p>This service is for downloading videos you have rights to. You are responsible for ensuring you have permission to download any content.</p>
        
        <h2>Copyright</h2>
        <p>You must respect copyright laws. Do not download copyrighted content without permission.</p>
        
        <h2>Disclaimer</h2>
        <p>This service is provided "as is" without warranties. We are not responsible for how you use downloaded content.</p>
        
        <h2>Service Availability</h2>
        <p>We do not guarantee uninterrupted service. Downloads may fail due to various technical reasons.</p>
        
        <p><a href="/">Back to Home</a></p>
    </div>
</body>
</html>
```

**3. Update Footer to Link Pages**

In `index.html`, find the footer and update it:

```html
<footer class="footer">
    <p>&copy; 2024 YouTube Downloader. For personal use only.</p>
    <p class="disclaimer">This tool is for downloading videos you have rights to. Please respect copyright laws.</p>
    <p style="margin-top: 15px;">
        <a href="/static/privacy.html" style="color: #6b7280; margin: 0 10px;">Privacy Policy</a> |
        <a href="/static/terms.html" style="color: #6b7280; margin: 0 10px;">Terms of Service</a> |
        <a href="mailto:your-email@example.com" style="color: #6b7280; margin: 0 10px;">Contact</a>
    </p>
</footer>
```

### C. Apply for Google AdSense

**1. Go to AdSense**
   - Visit: https://www.google.com/adsense
   - Click "Get Started"
   - Sign in with Google account

**2. Enter Your Information**
   - **Website URL**: Your custom domain (e.g., `https://ytdownloader.com`)
   - **Email**: Your contact email
   - Click "Save and continue"

**3. Connect Your Site to AdSense**
   - AdSense will provide a verification code
   - Add it to the `<head>` section of your HTML
   - Wait for verification (can take 24-48 hours)

**4. Review & Submit**
   - Google will review your site
   - Can take 1 day to several weeks
   - Check email for approval/rejection

### D. After AdSense Approval

Once approved, you'll get your Publisher ID and can create ad units:

**1. Get Your Publisher ID**
   - Format: `ca-pub-1234567890123456`
   - Found in AdSense → Account → Account Information

**2. Create Ad Units**
   - Go to: Ads → By ad unit → Display ads
   - Create 3 ad units:
     * **Header Banner** (Responsive or 728x90)
     * **Sidebar** (Responsive or 160x600)  
     * **In-Content** (Responsive or 300x250)
   - Copy each ad code

**3. Replace Placeholder Codes**

In `index.html`, find and replace ALL instances of:
- `ca-pub-XXXXXXXXXXXXXXXX` → Your actual publisher ID
- `data-ad-slot="XXXXXXXXXX"` → Your actual ad slot IDs

There are 3 ad units to replace:
1. Header banner (top of page)
2. Sidebar ad (left side)
3. In-content ad (below features)

**4. Deploy Changes**
   - Save your HTML file
   - Push to GitHub (auto-deploys on Railway/Render)
   - Wait 10-30 minutes for ads to appear

---

## 📈 What You Can Track

### Google Analytics Dashboard

**Realtime Report:**
- Current active users
- Pages being viewed right now
- Traffic sources

**Acquisition Report:**
- Where visitors come from (Google, Reddit, Twitter, etc.)
- Organic search vs direct vs referral

**Engagement Report:**
- Most viewed pages
- Average session duration
- Bounce rate

**Tech Report:**
- Browser/device breakdown
- Mobile vs desktop usage
- Geographic location

### Google AdSense Dashboard

**Overview:**
- Estimated earnings (today, yesterday, this month)
- Page views and clicks
- Click-through rate (CTR)
- Cost per click (CPC)

**Reports:**
- Earnings by date
- Top performing ad units
- Geographic earnings

---

## 🎯 Custom Event Tracking (Optional)

Track specific user actions in Google Analytics:

Add this to your `app.js` file:

```javascript
// Track video info requests
function handleGetInfo() {
    // ... existing code ...
    
    // Track event
    if (typeof gtag !== 'undefined') {
        gtag('event', 'video_info_request', {
            'event_category': 'engagement',
            'event_label': url
        });
    }
}

// Track download starts
function handleDownload() {
    // ... existing code ...
    
    if (typeof gtag !== 'undefined') {
        gtag('event', 'download_start', {
            'event_category': 'conversion',
            'event_label': quality
        });
    }
}

// Track successful downloads
function showDownloadReady(token) {
    // ... existing code ...
    
    if (typeof gtag !== 'undefined') {
        gtag('event', 'download_complete', {
            'event_category': 'conversion',
            'value': 1
        });
    }
}
```

---

## ✅ Checklist

### Google Analytics:
- [ ] Created Google Analytics account
- [ ] Got Measurement ID (G-XXXXXXXXXX)
- [ ] Replaced placeholder in index.html
- [ ] Deployed changes
- [ ] Verified tracking works (Realtime report)

### Google AdSense:
- [ ] Bought custom domain
- [ ] Created Privacy Policy page
- [ ] Created Terms of Service page
- [ ] Added footer links
- [ ] Applied for AdSense
- [ ] Waited for approval
- [ ] Got Publisher ID and ad codes
- [ ] Replaced all placeholders
- [ ] Deployed and verified ads show

---

## 💡 Tips

**For Analytics:**
- Check daily to see traffic patterns
- Use data to optimize your site
- Track which traffic sources work best

**For AdSense:**
- Don't click your own ads (will get banned!)
- Experiment with ad placement
- Mobile users = more ad revenue usually
- Keep ads but don't overwhelm users

**For Growth:**
- Share on Reddit, Twitter
- SEO optimization (keywords, meta tags)
- Fast site = better rankings
- Good user experience = more shares

---

## 🆘 Troubleshooting

**Analytics not showing data:**
- Wait 24 hours for data to appear
- Check Measurement ID is correct
- Clear browser cache
- Visit site in incognito mode

**AdSense rejected:**
- Add more content (blog posts, FAQs)
- Ensure legal pages exist
- Wait 1-2 weeks, reapply
- Consider alternative ad networks

**Ads not showing:**
- Check AdSense dashboard for errors
- Wait 30-60 minutes after adding code
- Verify ad codes are correct
- Check browser console for errors

---

**You're all set! 🎉**

Start with Google Analytics today (free, instant).
Work on AdSense approval (takes time but worth it).

