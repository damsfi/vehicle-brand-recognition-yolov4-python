# Heroku Quick Start - 5 Minutes

## Step 1: Install Heroku CLI

Download and install: https://devcenter.heroku.com/articles/heroku-cli

## Step 2: Login

```bash
heroku login
```

## Step 3: Create App

```bash
heroku create your-app-name
```

**Example:**
```bash
heroku create object-detection-api
```

## Step 4: Deploy

```bash
git push heroku master
```

**Or if you're on main branch:**
```bash
git push heroku main
```

## Step 5: Test

```bash
# Check if it's running
heroku ps

# View logs
heroku logs --tail

# Test the API
curl https://your-app-name.herokuapp.com/health
```

## Done! 🎉

Your API is now live at: `https://your-app-name.herokuapp.com`

Update your mobile app to use this URL!

---

## Common Issues

### App crashes?
```bash
heroku logs --tail
```

### Need to restart?
```bash
heroku restart
```

### Out of memory?
- Free tier: 512MB RAM
- Upgrade to Hobby ($7/month) for more

---

## Full Guide

See `HEROKU_DEPLOY.md` for detailed instructions.

