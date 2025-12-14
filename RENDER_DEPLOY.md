# Deploy to Render - Step by Step Guide

## Why Render?
- ✅ **Simpler** than Railway
- ✅ **Free tier** available
- ✅ **Auto-deploys** from GitHub
- ✅ **Auto HTTPS** included
- ✅ **Easy setup** - just connect GitHub

---

## Step 1: Push Code to GitHub

Make sure your code is on GitHub:

```bash
git add .
git commit -m "Ready for Render deployment"
git push origin master
```

---

## Step 2: Sign Up on Render

1. Go to: **https://render.com**
2. Click **"Get Started for Free"**
3. Sign up with **GitHub** (easiest way)

---

## Step 3: Create New Web Service

1. Click **"New +"** button (top right)
2. Select **"Web Service"**
3. Click **"Connect GitHub"** (if not already connected)
4. Authorize Render to access your repositories
5. Select your repository: `vehicle-brand-recognition-yolov4-python`

---

## Step 4: Configure Service

Fill in these settings:

### Basic Settings:
- **Name**: `object-detection-api` (or any name you want)
- **Region**: Choose closest to you (e.g., `Oregon (US West)`)
- **Branch**: `master` (or `main`)

### Build & Deploy:
- **Runtime**: `Python 3`
- **Build Command**: 
  ```
  pip install -r requirements.txt && bash bin/download_weights
  ```
- **Start Command**: 
  ```
  gunicorn --config gunicorn_config.py api_server_production:app
  ```

### Environment:
- **Environment**: `Docker` (optional, but recommended)
- Or leave as **Python** (simpler)

### Advanced (Optional):
- **Auto-Deploy**: `Yes` (deploys on every push)

---

## Step 5: Deploy!

1. Scroll down and click **"Create Web Service"**
2. Render will:
   - Clone your repo
   - Install dependencies
   - Download YOLO weights
   - Start your API
3. Wait 5-10 minutes for first deployment

---

## Step 6: Get Your URL

1. Once deployed, you'll see a URL like:
   ```
   https://object-detection-api.onrender.com
   ```
2. Copy this URL

---

## Step 7: Test It

```bash
# Health check
curl https://your-app.onrender.com/health

# Should return:
# {"status": "healthy", "message": "API is running", "model_status": "loaded"}
```

---

## Step 8: Update Your Mobile App

Use this URL in your mobile app:
```
https://your-app.onrender.com/detect
```

---

## Important Notes

### Free Tier Limitations:
- ⚠️ **Sleeps after 15 minutes** of inactivity
- ⚠️ **First request** after sleep takes ~30 seconds (wake up time)
- ✅ **Free forever** - no credit card needed
- ✅ **512MB RAM** - enough for YOLO

### For Production:
- Upgrade to **Starter** ($7/month) to prevent sleeping
- Better performance and reliability

---

## Troubleshooting

### Build Fails?

**Check build logs:**
1. Go to your service in Render
2. Click **"Logs"** tab
3. Look for errors

**Common issues:**
- Missing `requirements.txt` → Make sure it exists
- Download weights fails → Check internet in build
- Port issues → Already handled in code

### App Crashes?

**Check runtime logs:**
1. Click **"Logs"** tab
2. Look for Python errors
3. Check if model loaded successfully

**Common fixes:**
- Verify `yolov4/yolov4.weights` downloaded
- Check if all dependencies installed
- Verify PORT is being used (already fixed in code)

### Can't Access?

- Wait for deployment to complete (green checkmark)
- Check if service is "Live" (not "Sleeping")
- Verify URL is correct

---

## Quick Reference

### Render Dashboard:
- **Services**: https://dashboard.render.com
- **Logs**: Click service → Logs tab
- **Settings**: Click service → Settings tab

### Update Your App:
1. Push changes to GitHub
2. Render auto-deploys (if enabled)
3. Or manually click "Manual Deploy" → "Deploy latest commit"

### Restart Service:
- Click service → "Manual Deploy" → "Clear build cache & deploy"

---

## Success Checklist

- [ ] Code pushed to GitHub
- [ ] Render account created
- [ ] Web service created
- [ ] Build completed successfully
- [ ] Health check returns 200
- [ ] Detection endpoint works
- [ ] Mobile app updated with URL

---

## That's It! 🎉

Your API is now live on Render!

**URL format:** `https://your-app-name.onrender.com`

**Endpoints:**
- Health: `https://your-app-name.onrender.com/health`
- Detect: `https://your-app-name.onrender.com/detect`

---

## Need Help?

- Render Docs: https://render.com/docs
- Check logs in Render dashboard
- Render Status: https://status.render.com

