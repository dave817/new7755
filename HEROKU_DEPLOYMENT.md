# 🚀 Heroku Deployment Guide - 纏綿悱惻

## ✅ Pre-Deployment Checklist

- [x] Procfile ready
- [x] runtime.txt ready (Python 3.11.6)
- [x] requirements.txt complete
- [x] .gitignore configured (.env excluded)
- [x] LINE integration tested locally
- [x] Git repository initialized

---

## 📦 Step 1: Install Heroku CLI (If Not Already Installed)

### Download & Install:
https://devcenter.heroku.com/articles/heroku-cli

Or use command:
```bash
# Windows (via installer)
# Download from URL above and run installer
```

### Verify Installation:
```bash
heroku --version
```

---

## 🔑 Step 2: Login to Heroku

```bash
heroku login
```

This will open a browser window for you to login.

---

## 🆕 Step 3: Create Heroku App

```bash
# Create app with a unique name
heroku create chanmianfeice-bot

# Or let Heroku generate a random name:
# heroku create
```

**Note the app URL:** `https://chanmianfeice-bot-xxxxx.herokuapp.com`

---

## ⚙️ Step 4: Set Environment Variables

```bash
# SenseChat API
heroku config:set SENSENOVA_ACCESS_KEY_ID=019A0A2BD9067A46B8DD59CBD56F2A9C
heroku config:set SENSENOVA_SECRET_ACCESS_KEY=019A0A2BD9067A3689A95F2111B79929
heroku config:set SENSENOVA_API_KEY=sk-KwTRyijO6ByCWjrjm3vf5bwgGktAKOYQ
heroku config:set MODEL_NAME=SenseChat-Character-Pro

# LINE Bot
heroku config:set LINE_CHANNEL_SECRET=e4e1f836bf472c818f1fd19ac01ab279
heroku config:set LINE_CHANNEL_ACCESS_TOKEN=bSZWwJkozYrBrLyD/DmgRGaKJDBJBHYm6x6jogOX5q+zSzHjkZky08Xyj+DkfYlQTRN+hRUaJOcQQHEx3Z+cFLnx7AdCse2zRR13OKdVkWRCK5KrDqwauP4W0DGknp3/e7BHrbrUfmfOqEq/r8zizQdB04t89/1O/w1cDnyilFU=
heroku config:set LINE_BOT_NAME="纏綿悱惻 - 聊出激情吧!"
heroku config:set LINE_BOT_DESCRIPTION="The most interesting dating chatbot on LINE"

# Application URLs (REPLACE WITH YOUR ACTUAL HEROKU URL)
heroku config:set APP_BASE_URL=https://YOUR-APP-NAME.herokuapp.com
heroku config:set SETUP_UI_PATH=/ui2

# Environment
heroku config:set ENVIRONMENT=production
heroku config:set DEBUG=False

# Feature Settings
heroku config:set FREE_MESSAGES_PER_DAY=20
heroku config:set PREMIUM_PRICE_USD=9.99
heroku config:set REFERRALS_FOR_UNLIMITED=2

# Database (SQLite for now - will auto-create)
heroku config:set DATABASE_URL=sqlite:///./dating_chatbot.db

# CORS
heroku config:set CORS_ORIGINS='["*"]'
```

### Verify Configuration:
```bash
heroku config
```

---

## 📤 Step 5: Deploy to Heroku

```bash
# Make sure all changes are committed
git status
git add .
git commit -m "Prepare for Heroku deployment with LINE integration"

# Deploy to Heroku
git push heroku main

# Or if your branch is named 'master':
# git push heroku master
```

### If you get branch errors:
```bash
# Push current branch to Heroku's main
git push heroku HEAD:main
```

---

## 🔍 Step 6: Check Deployment

```bash
# View logs
heroku logs --tail

# Open app in browser
heroku open

# Check if server is running
curl https://YOUR-APP-NAME.herokuapp.com/health
```

You should see: `{"status":"healthy"}`

---

## 📡 Step 7: Update LINE Webhook URL

1. Go to LINE Developers Console: https://developers.line.biz/console/
2. Select your channel: **纏綿悱惻 - 聊出激情吧!**
3. Go to **"Messaging API"** tab
4. Update **Webhook URL** to: `https://YOUR-APP-NAME.herokuapp.com/webhook/line`
5. Click **"Verify"** - should show "Success" ✅
6. Make sure **"Use webhook"** is enabled

---

## 🧪 Step 8: Test Production

1. **Block and re-add your LINE bot** (to get fresh welcome message)
2. **Click setup link** (should now use Heroku URL)
3. **Create character**
4. **Verify:**
   - Character picture received in LINE
   - Welcome message received
   - Can chat with character
   - Web UI shows "go back to LINE" message

---

## 🐛 Troubleshooting

### Issue: App crashed
```bash
heroku logs --tail
# Look for errors in the logs
```

### Issue: Database errors
Heroku uses ephemeral filesystem. For production, consider:
- Using Heroku Postgres addon (recommended)
- Using Supabase (free tier available)

**To add Heroku Postgres:**
```bash
heroku addons:create heroku-postgresql:mini
# This will automatically set DATABASE_URL
```

### Issue: Pictures not loading
Make sure `APP_BASE_URL` is set correctly:
```bash
heroku config:set APP_BASE_URL=https://YOUR-ACTUAL-APP.herokuapp.com
```

### Issue: LINE webhook verification failed
- Check logs: `heroku logs --tail`
- Make sure LINE credentials are correct
- Verify webhook URL has `/webhook/line` at the end

---

## 📊 Monitor Your App

```bash
# View logs
heroku logs --tail

# Check app status
heroku ps

# Restart app if needed
heroku restart

# Open dashboard
heroku open
```

---

## 💰 Heroku Costs

**Current Setup:**
- **Free Tier:** 550-1000 free dyno hours/month (with credit card)
- **No credit card:** 550 hours/month (app sleeps after 30 min inactivity)

**Production Ready:**
- **Eco Dyno:** $5/month (never sleeps)
- **Basic Dyno:** $7/month (better for production)

**Recommendation:** Start with free tier for testing, upgrade to Eco/Basic when launching publicly.

---

## 🎯 Post-Deployment Checklist

- [ ] App deployed successfully
- [ ] Health check endpoint working
- [ ] LINE webhook verified
- [ ] Tested character creation
- [ ] Tested chat in LINE
- [ ] Pictures loading correctly
- [ ] Web UI shows correct success message

---

## 📝 Important Notes

1. **Database:** Current SQLite database will reset on Heroku dyno restart. For production, use Heroku Postgres or Supabase.

2. **Environment Variables:** Never commit `.env` to git. Always set via `heroku config:set`.

3. **Pictures:** Make sure pictures directory is committed to git (should be in the repo).

4. **ngrok:** You can stop ngrok after Heroku deployment! 🎉

---

## 🆘 Need Help?

```bash
# View detailed logs
heroku logs --tail --app YOUR-APP-NAME

# Check configuration
heroku config --app YOUR-APP-NAME

# SSH into dyno (for debugging)
heroku run bash --app YOUR-APP-NAME
```

---

**Your Heroku deployment is ready! Let's deploy! 🚀**
