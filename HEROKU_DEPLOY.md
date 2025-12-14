# Deploy to Heroku - Step by Step Guide

## Prerequisites

1. **GitHub account** (you already have this)
2. **Heroku account** - Sign up at https://signup.heroku.com (free)
3. **Heroku CLI** - Download from https://devcenter.heroku.com/articles/heroku-cli

---

## Step 1: Install Heroku CLI

### Windows:
1. Download installer: https://devcenter.heroku.com/articles/heroku-cli
2. Run the installer
3. Open PowerShell/Command Prompt

### Verify installation:
```bash
heroku --version
```

---

## Step 2: Login to Heroku

```bash
heroku login
```

This will open a browser window. Click "Log in" to authenticate.

---

## Step 3: Create Heroku App

```bash
# Navigate to your project directory (you're already there)
cd C:\Users\Korisnik\Downloads\pytgaw\vehicle-brand-recognition-yolov4-python

# Create a new Heroku app
heroku create your-app-name

# Example:
# heroku create object-detection-api
```

**Note:** Choose a unique app name (it will be `your-app-name.herokuapp.com`)

---

## Step 4: Download YOLO Weights (Important!)

Heroku has a 500MB slug size limit. The YOLO weights file (245MB) is too large for Git.

**Option A: Use buildpack to download weights (Recommended)**

Create `app.json`:
```json
{
  "buildpacks": [
    {
      "url": "heroku/python"
    }
  ]
}
```

Create `bin/download_weights`:
```bash
#!/bin/bash
echo "Downloading YOLOv4 weights..."
mkdir -p yolov4
cd yolov4
if [ ! -f "yolov4.weights" ]; then
    wget https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v3_optimal/yolov4.weights
fi
```

Make it executable and add to Procfile:
```
web: bin/download_weights && gunicorn --config gunicorn_config.py api_server_production:app
```

**Option B: Use external storage (Better for production)**

We'll modify the code to download weights if missing. Let me create that for you.

---

## Step 5: Add Files to Git

Make sure everything is committed:

```bash
git add .
git commit -m "Prepare for Heroku deployment"
```

---

## Step 6: Deploy to Heroku

```bash
# Push to Heroku
git push heroku master

# Or if you're on main branch:
git push heroku main
```

This will:
- Install all dependencies
- Build your app
- Deploy it

---

## Step 7: Verify Deployment

```bash
# Check if app is running
heroku ps

# View logs
heroku logs --tail

# Test health endpoint
heroku open
# Then add /health to the URL, or:
curl https://your-app-name.herokuapp.com/health
```

---

## Step 8: Test the API

```bash
# Test detection endpoint
curl -X POST https://your-app-name.herokuapp.com/detect \
  -F "image=@volkswagen.jpg" \
  -F "confidence=0.5"
```

Or use Python:
```python
import requests

url = "https://your-app-name.herokuapp.com/detect"
files = {'image': open('volkswagen.jpg', 'rb')}
response = requests.post(url, files=files)
print(response.json())
```

---

## Step 9: Update Your Mobile App

Change the API URL in your mobile app to:
```
https://your-app-name.herokuapp.com
```

---

## Troubleshooting

### App crashes on startup

**Check logs:**
```bash
heroku logs --tail
```

**Common issues:**

1. **YOLO weights missing:**
   - The weights file needs to be downloaded
   - See Step 4 above

2. **Memory limit:**
   - Free tier has 512MB RAM
   - YOLO needs ~400MB
   - Upgrade to Hobby ($7/month) for 512MB-1GB

3. **Build timeout:**
   - Free tier has 10min build limit
   - If build takes too long, upgrade

### View detailed logs:
```bash
heroku logs --tail --app your-app-name
```

### Restart app:
```bash
heroku restart
```

### Check app info:
```bash
heroku info
```

---

## Important Notes

1. **Free Tier Limitations:**
   - App sleeps after 30min of inactivity
   - First request after sleep takes ~30 seconds
   - 550-1000 hours/month free
   - 512MB RAM

2. **For Production:**
   - Upgrade to Hobby ($7/month) to prevent sleeping
   - Better performance and reliability

3. **YOLO Weights:**
   - Must be downloaded during build or at runtime
   - Can't be committed to Git (too large)

---

## Quick Commands Reference

```bash
# Login
heroku login

# Create app
heroku create app-name

# Deploy
git push heroku master

# View logs
heroku logs --tail

# Restart
heroku restart

# Open app
heroku open

# Check status
heroku ps

# Scale (if needed)
heroku ps:scale web=1
```

---

## Next Steps After Deployment

1. ✅ Test the API endpoints
2. ✅ Update mobile app with new URL
3. ✅ Monitor logs for errors
4. ✅ Consider upgrading to Hobby tier for production use

---

## Need Help?

- Heroku Docs: https://devcenter.heroku.com/articles/getting-started-with-python
- Check logs: `heroku logs --tail`
- Heroku Status: https://status.heroku.com

