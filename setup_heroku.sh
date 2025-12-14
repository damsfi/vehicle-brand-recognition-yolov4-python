#!/bin/bash
# Quick setup script for Heroku deployment

echo "=== Heroku Deployment Setup ==="
echo ""

# Check if Heroku CLI is installed
if ! command -v heroku &> /dev/null; then
    echo "❌ Heroku CLI not found!"
    echo "Please install from: https://devcenter.heroku.com/articles/heroku-cli"
    exit 1
fi

echo "✓ Heroku CLI found"
echo ""

# Check if logged in
if ! heroku auth:whoami &> /dev/null; then
    echo "Please login to Heroku:"
    heroku login
else
    echo "✓ Already logged in as: $(heroku auth:whoami)"
fi

echo ""
echo "Next steps:"
echo "1. Create Heroku app: heroku create your-app-name"
echo "2. Deploy: git push heroku master"
echo ""
echo "See HEROKU_DEPLOY.md for detailed instructions"

