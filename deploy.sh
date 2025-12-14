#!/bin/bash
# Deployment script for Linux servers

set -e

echo "=== Object Detection API Deployment Script ==="

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "Please run as root or with sudo"
    exit 1
fi

# Configuration
APP_DIR="/opt/object-detection-api"
SERVICE_USER="www-data"
PYTHON_VERSION="python3"

echo "1. Creating application directory..."
mkdir -p $APP_DIR
mkdir -p $APP_DIR/logs

echo "2. Copying files..."
# Copy all necessary files (adjust paths as needed)
cp -r . $APP_DIR/ 2>/dev/null || true

echo "3. Setting up Python virtual environment..."
cd $APP_DIR
$PYTHON_VERSION -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements_api.txt
pip install gunicorn

echo "4. Setting permissions..."
chown -R $SERVICE_USER:$SERVICE_USER $APP_DIR
chmod +x $APP_DIR/deploy.sh

echo "5. Installing systemd service..."
cp object-detection-api.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable object-detection-api
systemctl restart object-detection-api

echo "6. Checking service status..."
sleep 2
systemctl status object-detection-api --no-pager

echo ""
echo "=== Deployment Complete ==="
echo "Service is running. Check status with: systemctl status object-detection-api"
echo "View logs with: journalctl -u object-detection-api -f"
echo "API should be available at: http://your-server-ip:5000"

