# Render Troubleshooting Guide

## 502 Error - App Not Responding

### Step 1: Check Logs
1. Go to Render dashboard
2. Click your service
3. Click **"Logs"** tab
4. Scroll to see startup errors

### Step 2: Common Issues & Fixes

#### Issue: "Module not found"
**Fix:** Make sure build command uses `requirements.txt`:
```
pip install -r requirements.txt && bash bin/download_weights
```

#### Issue: "Port already in use" or port errors
**Fix:** Already handled - gunicorn_config.py uses PORT env var ✅

#### Issue: "File not found" or "yolov4.weights not found"
**Fix:** Check if download_weights script runs:
- Look for "YOLO weights downloaded" in logs
- If missing, the script might have failed

#### Issue: "Import error" or "No module named X"
**Fix:** 
1. Check `requirements.txt` has all dependencies
2. Verify build command installed them
3. Try: `pip install -r requirements.txt` manually in logs

#### Issue: App crashes immediately
**Fix:** Check if model loads:
- Look for "Loading YOLO model..." in logs
- Look for "YOLO model loaded successfully!"
- If missing, model loading failed

### Step 3: Verify Configuration

**In Render Dashboard → Settings:**

✅ **Build Command:**
```
pip install --upgrade pip && pip install -r requirements.txt && bash bin/download_weights
```

✅ **Start Command:**
```
gunicorn --config gunicorn_config.py api_server_production:app
```

✅ **Environment:** Python 3

✅ **Auto-Deploy:** Enabled (optional)

### Step 4: Manual Redeploy

1. Click **"Manual Deploy"**
2. Select **"Deploy latest commit"**
3. Or **"Clear build cache & deploy"** (if build issues)

### Step 5: Check Service Status

- **Live** = Running ✅
- **Sleeping** = Free tier, sleeping (first request will wake it)
- **Build Failed** = Check build logs ❌
- **Deploy Failed** = Check deploy logs ❌

## Quick Diagnostic Commands

### Check if service is running:
Look for "Live" status in Render dashboard

### Check build logs:
Look for:
- ✅ "Successfully installed..."
- ✅ "YOLO weights downloaded successfully"
- ❌ Any error messages

### Check runtime logs:
Look for:
- ✅ "API server startup"
- ✅ "Loading YOLO model..."
- ✅ "YOLO model loaded successfully!"
- ❌ Any Python errors

## Still Not Working?

1. **Copy the error from Render logs**
2. **Check which step fails:**
   - Build phase?
   - Deploy phase?
   - Runtime (after deploy)?

3. **Common fixes:**
   - Wrong requirements file → Use `requirements.txt`
   - Missing dependencies → Check requirements.txt
   - Port issues → Already fixed in code
   - Model loading → Check if weights downloaded

## Test After Fix

```bash
# Wait for deployment to complete
# Then test:
curl https://detection-api-7p4e.onrender.com/health

# Should return:
# {"status": "healthy", "message": "API is running", "model_status": "loaded"}
```

## Need More Help?

Share the error message from Render logs and I'll help fix it!

