# Render Quick Start - 5 Minutes

## Super Simple Steps:

### 1. Push to GitHub ✅
```bash
git push origin master
```

### 2. Go to Render
- Visit: **https://render.com**
- Sign up with GitHub

### 3. Create Web Service
- Click **"New +"** → **"Web Service"**
- Connect your GitHub repo
- Select: `vehicle-brand-recognition-yolov4-python`

### 4. Configure (Copy/Paste):

**Build Command:**
```
pip install -r requirements.txt && bash bin/download_weights
```

**Start Command:**
```
gunicorn --config gunicorn_config.py api_server_production:app
```

### 5. Deploy!
- Click **"Create Web Service"**
- Wait 5-10 minutes
- Done! 🎉

---

## Your API URL:
```
https://your-app-name.onrender.com
```

## Test It:
```bash
curl https://your-app-name.onrender.com/health
```

## Use in Mobile App:
```
https://your-app-name.onrender.com/detect
```

---

## That's It!

**Total time: ~5 minutes**

See `RENDER_DEPLOY.md` for detailed instructions.

