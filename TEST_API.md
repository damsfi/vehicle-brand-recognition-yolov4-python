# Test Your Railway API

## Quick Test Commands

### 1. Health Check (Test if API is running)

**Using curl:**
```bash
curl https://your-app.up.railway.app/health
```

**Using Python:**
```python
import requests
response = requests.get("https://your-app.up.railway.app/health")
print(response.json())
```

**Expected response:**
```json
{
  "status": "healthy",
  "message": "API is running",
  "model_status": "loaded"
}
```

---

### 2. Test Detection Endpoint

**Using curl:**
```bash
curl -X POST https://your-app.up.railway.app/detect \
  -F "image=@volkswagen.jpg" \
  -F "confidence=0.5"
```

**Using Python:**
```python
import requests

url = "https://your-app.up.railway.app/detect"
files = {'image': open('volkswagen.jpg', 'rb')}
data = {'confidence': 0.5}

response = requests.post(url, files=files, data=data)
print(response.json())
# Expected: {"count": 1} or similar
```

**Using the test script:**
```bash
python test_railway_api.py https://your-app.up.railway.app
```

---

### 3. Test from Mobile App

Update your mobile app to use:
```
https://your-app.up.railway.app/detect
```

---

## What to Check

✅ **Health endpoint returns 200** - API is running
✅ **Model status is "loaded"** - YOLO model loaded successfully
✅ **Detection returns count** - API can process images
✅ **No errors in logs** - Check Railway logs if issues

---

## Troubleshooting

### API returns 500 error
- Check Railway logs: View logs in Railway dashboard
- Model might not have loaded
- Check if weights downloaded successfully

### API times out
- First request after deployment can be slow (downloading weights)
- Wait 1-2 minutes and try again

### Can't connect
- Check if service is running in Railway dashboard
- Verify the URL is correct
- Check if port is exposed

---

## Railway Logs

View logs in Railway dashboard:
1. Go to your project
2. Click on your service
3. Click "Logs" tab
4. Look for errors or startup messages

---

## Success Indicators

✅ Health check returns 200
✅ Model status shows "loaded"
✅ Detection returns a number (count)
✅ No errors in logs

If all these pass, your API is working! 🎉

