# Fix 502 Error on Render

## The Problem
502 error means the app is crashing on startup. Common causes:
1. Port configuration
2. Build command issues
3. Missing files
4. Model loading failures

## Check Render Logs First

1. Go to Render dashboard
2. Click your service: `detection-api-7p4e`
3. Click **"Logs"** tab
4. Look for errors

**Common errors to look for:**
- Port binding errors
- Import errors
- File not found
- Model loading failures

## Quick Fixes

### Fix 1: Verify Build Command

In Render dashboard → Settings → Build Command:
```
pip install -r requirements.txt && bash bin/download_weights
```

Make sure it's exactly this (not `requirements_api.txt`)

### Fix 2: Verify Start Command

In Render dashboard → Settings → Start Command:
```
gunicorn --config gunicorn_config.py api_server_production:app
```

### Fix 3: Check Environment Variables

Render automatically sets `PORT` - our code already handles this ✅

### Fix 4: Check if Weights Downloaded

Look in logs for:
- "YOLO weights downloaded successfully" ✅
- "Failed to download weights" ❌

If download fails, the app will crash.

## Manual Fix Steps

1. **Check Render Logs** - See what error is happening
2. **Verify Build Command** - Should use `requirements.txt`
3. **Check Start Command** - Should use gunicorn
4. **Redeploy** - Click "Manual Deploy" → "Deploy latest commit"

## If Still Failing

Share the error from Render logs and I'll help fix it!

The most common issue is the build command using wrong requirements file.

