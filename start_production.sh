#!/bin/bash
# Simple production start script (if not using systemd)

cd "$(dirname "$0")"

# Create logs directory
mkdir -p logs

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Install gunicorn if not installed
pip install gunicorn 2>/dev/null || true

# Start with gunicorn
echo "Starting production server with gunicorn..."
gunicorn --config gunicorn_config.py api_server_production:app

