# Test API Locally - Quick Guide

## Option 1: Run Locally (Easiest)

### Step 1: Start the server
```bash
python run_local.py
```

The server will start on `http://localhost:5000`

### Step 2: Test it (in another terminal)
```bash
# Health check
curl http://localhost:5000/health

# Or use the test script
python test_local_api.py
```

### Step 3: Test from your mobile app
Use: `http://YOUR_COMPUTER_IP:5000`

**Find your IP:**
- Windows: `ipconfig` (look for IPv4 Address)
- Mac/Linux: `ifconfig` or `ip addr`

**Example:** If your IP is `192.168.1.100`, use:
```
http://192.168.1.100:5000/detect
```

---

## Option 2: Use ngrok (Expose Local Server to Internet)

### Why ngrok?
- ✅ Test from your phone even when not on same network
- ✅ Get a public URL instantly
- ✅ No deployment needed
- ✅ Perfect for quick testing

### Setup:

1. **Download ngrok**: https://ngrok.com/download
2. **Extract and run:**
   ```bash
   # Start your local server first
   python run_local.py
   
   # In another terminal, expose it
   ngrok http 5000
   ```
3. **Copy the URL** ngrok gives you (e.g., `https://abc123.ngrok.io`)
4. **Use in your mobile app:**
   ```
   https://abc123.ngrok.io/detect
   ```

**That's it!** Your local server is now accessible from anywhere.

---

## Option 3: Quick Deploy to Render (Simpler than Railway)

1. Go to: https://render.com
2. Sign up (free)
3. New → Web Service
4. Connect GitHub repo
5. Settings:
   - Build: `pip install -r requirements.txt && bash bin/download_weights`
   - Start: `gunicorn --config gunicorn_config.py api_server_production:app`
6. Deploy!

**Free tier available** (sleeps after 15min but works great for testing)

---

## Quick Comparison

| Method | Speed | Ease | Internet Access |
|--------|-------|------|-----------------|
| **Local** | ⚡ Instant | ⭐⭐⭐⭐⭐ | ❌ Same network only |
| **ngrok** | ⚡ Instant | ⭐⭐⭐⭐ | ✅ Yes (public URL) |
| **Render** | 🐢 5 min | ⭐⭐⭐ | ✅ Yes (always on) |
| **Railway** | 🐢 5 min | ⭐⭐ | ✅ Yes (always on) |

---

## Recommended: Start with Local + ngrok

1. Test locally first: `python run_local.py`
2. If it works, use ngrok to test from your phone
3. Once confirmed working, deploy to Render/Railway

This way you catch issues early! 🚀

---

## Troubleshooting Local Server

### Port already in use?
```bash
# Change port
PORT=8000 python run_local.py
```

### Can't connect from phone?
- Make sure both devices on same WiFi
- Check firewall allows port 5000
- Use ngrok instead (easier!)

### Model not loading?
- Make sure `yolov4/yolov4.weights` exists
- Check logs for errors

---

## Test Commands

```bash
# Start server
python run_local.py

# Test health (in another terminal)
curl http://localhost:5000/health

# Test detection
curl -X POST http://localhost:5000/detect \
  -F "image=@volkswagen.jpg" \
  -F "confidence=0.5"

# Or use test script
python test_local_api.py
```

