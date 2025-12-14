# Quick Start - Deploy Your API

## 🚀 Fastest Way: Heroku (5 minutes)

1. **Install Heroku CLI**: https://devcenter.heroku.com/articles/heroku-cli

2. **Login and create app**:
   ```bash
   heroku login
   heroku create your-app-name
   ```

3. **Deploy**:
   ```bash
   git add .
   git commit -m "Deploy API"
   git push heroku main
   ```

4. **Your API is live at**: `https://your-app-name.herokuapp.com`

5. **Test it**:
   ```bash
   curl https://your-app-name.herokuapp.com/health
   ```

6. **Update your mobile app** to use: `https://your-app-name.herokuapp.com/detect`

---

## 🖥️ Production Server (Linux VPS)

### Step 1: Get a server
- DigitalOcean: https://www.digitalocean.com ($12/month)
- AWS EC2: https://aws.amazon.com/ec2
- Linode: https://www.linode.com

### Step 2: Connect and deploy

```bash
# SSH into your server
ssh root@your-server-ip

# Install dependencies
apt update && apt install -y python3 python3-pip python3-venv git

# Upload your code (use SCP or Git)
# If using SCP from your local machine:
# scp -r . root@your-server-ip:/opt/object-detection-api/

# On server, go to app directory
cd /opt/object-detection-api

# Run deployment script
chmod +x deploy.sh
sudo ./deploy.sh
```

### Step 3: Configure firewall
```bash
ufw allow 5000/tcp
ufw enable
```

### Step 4: Test
```bash
curl http://your-server-ip:5000/health
```

---

## 📱 Update Your Mobile App

Change the API URL in your mobile app to:
- Heroku: `https://your-app-name.herokuapp.com`
- VPS: `http://your-server-ip:5000`

---

## ✅ Verify It's Working

```bash
# Test health endpoint
curl http://your-server-ip:5000/health

# Test detection (from your local machine)
curl -X POST http://your-server-ip:5000/detect \
  -F "image=@test_image.jpg" \
  -F "confidence=0.5"
```

---

## 🔧 Troubleshooting

**Service not running?**
```bash
systemctl status object-detection-api
systemctl restart object-detection-api
```

**Check logs:**
```bash
tail -f /opt/object-detection-api/logs/api.log
journalctl -u object-detection-api -f
```

**Can't access from mobile?**
- Check firewall: `ufw status`
- Verify port is open: `netstat -tlnp | grep 5000`
- Test from server: `curl http://localhost:5000/health`

---

## 📚 Full Documentation

See `DEPLOYMENT_GUIDE.md` for detailed instructions.

