# Complete Deployment Guide

This guide will help you deploy the Object Detection API so it's always available for your mobile app.

## Option 1: Deploy to a Cloud Server (Recommended)

### A. Using a Linux VPS (DigitalOcean, AWS EC2, Linode, etc.)

#### Step 1: Set up your server

1. Create a Ubuntu 22.04 LTS server (minimum 2GB RAM, 2 CPU cores)
2. SSH into your server:
   ```bash
   ssh root@your-server-ip
   ```

#### Step 2: Install dependencies

```bash
# Update system
apt update && apt upgrade -y

# Install Python and pip
apt install -y python3 python3-pip python3-venv git

# Install OpenCV dependencies
apt install -y libopencv-dev python3-opencv
```

#### Step 3: Upload your code

**Option A: Using Git (Recommended)**
```bash
# On your local machine, commit and push to GitHub/GitLab
# Then on server:
cd /opt
git clone your-repo-url object-detection-api
cd object-detection-api
```

**Option B: Using SCP**
```bash
# On your local machine:
scp -r . root@your-server-ip:/opt/object-detection-api/
```

#### Step 4: Deploy

```bash
cd /opt/object-detection-api
chmod +x deploy.sh
sudo ./deploy.sh
```

#### Step 5: Configure firewall

```bash
# Allow port 5000
ufw allow 5000/tcp
ufw enable
```

#### Step 6: Test

```bash
curl http://localhost:5000/health
```

### B. Using Heroku (Easiest for beginners)

1. Install Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli

2. Create `Procfile`:
   ```
   web: gunicorn --config gunicorn_config.py api_server_production:app
   ```

3. Deploy:
   ```bash
   heroku login
   heroku create your-app-name
   git push heroku main
   ```

4. Your API will be at: `https://your-app-name.herokuapp.com`

### C. Using Railway.app

1. Sign up at https://railway.app
2. Create new project
3. Connect your GitHub repo
4. Set start command: `gunicorn --config gunicorn_config.py api_server_production:app`
5. Deploy!

## Option 2: Deploy on Windows Server

### Using NSSM (Non-Sucking Service Manager)

1. Download NSSM: https://nssm.cc/download

2. Install the service:
   ```cmd
   nssm install ObjectDetectionAPI
   ```
   
3. Configure:
   - Path: `C:\Python\python.exe` (or your Python path)
   - Startup directory: `C:\path\to\your\api`
   - Arguments: `api_server_production.py`

4. Start service:
   ```cmd
   nssm start ObjectDetectionAPI
   ```

## Option 3: Simple Production Start (No systemd)

If you just want to run it manually:

```bash
chmod +x start_production.sh
./start_production.sh
```

Or with gunicorn directly:
```bash
gunicorn --config gunicorn_config.py api_server_production:app
```

## Making it Accessible from Internet

### 1. Get a Domain Name (Optional but Recommended)

- Buy from Namecheap, GoDaddy, etc.
- Point DNS A record to your server IP

### 2. Set up Nginx Reverse Proxy (Recommended)

Install Nginx:
```bash
apt install nginx
```

Create `/etc/nginx/sites-available/object-detection-api`:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    client_max_body_size 16M;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable site:
```bash
ln -s /etc/nginx/sites-available/object-detection-api /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx
```

### 3. Set up SSL with Let's Encrypt (Free HTTPS)

```bash
apt install certbot python3-certbot-nginx
certbot --nginx -d your-domain.com
```

## Monitoring & Maintenance

### Check if service is running:
```bash
systemctl status object-detection-api
```

### View logs:
```bash
# Service logs
journalctl -u object-detection-api -f

# Application logs
tail -f /opt/object-detection-api/logs/api.log
tail -f /opt/object-detection-api/logs/error.log
```

### Restart service:
```bash
systemctl restart object-detection-api
```

### Stop service:
```bash
systemctl stop object-detection-api
```

## Updating the API

1. Pull latest code or upload new files
2. Restart service:
   ```bash
   systemctl restart object-detection-api
   ```

## Troubleshooting

### Service won't start
- Check logs: `journalctl -u object-detection-api -n 50`
- Verify YOLO weights file exists: `ls yolov4/yolov4.weights`
- Check permissions: `ls -la /opt/object-detection-api`

### API returns errors
- Check application logs: `tail -f logs/api.log`
- Verify model loaded: `curl http://localhost:5000/health`
- Check disk space: `df -h`

### Can't access from mobile app
- Check firewall: `ufw status`
- Verify server is listening: `netstat -tlnp | grep 5000`
- Test from server: `curl http://localhost:5000/health`
- Check if using correct IP/domain in mobile app

## Security Recommendations

1. **Use HTTPS** (Let's Encrypt is free)
2. **Add API key authentication** (modify api_server_production.py)
3. **Rate limiting** (use Flask-Limiter)
4. **Keep system updated**: `apt update && apt upgrade`
5. **Use firewall**: Only open necessary ports

## Cost Estimates

- **DigitalOcean Droplet**: $12-24/month (2-4GB RAM)
- **AWS EC2 t3.medium**: ~$30/month
- **Heroku**: Free tier available, then $7-25/month
- **Railway**: Free tier, then pay-as-you-go

## Quick Start Checklist

- [ ] Server/VPS set up
- [ ] Code uploaded to server
- [ ] Dependencies installed
- [ ] YOLO weights file present
- [ ] Service installed and running
- [ ] Firewall configured
- [ ] Tested with curl
- [ ] Domain/SSL configured (optional)
- [ ] Mobile app updated with server URL

## Support

If you encounter issues:
1. Check logs first
2. Verify all files are present
3. Test health endpoint
4. Check system resources (RAM, CPU)

