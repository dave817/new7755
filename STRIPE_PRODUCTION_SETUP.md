# Stripe Production Setup Guide

## ✅ Step 1: Switch to Live API Key (DONE)

Update your `.env` file to use your **live** Stripe API key (starts with `sk_live_`):
```
STRIPE_API_KEY=<your_live_key_from_stripe_dashboard>
```
Find your actual live key in Stripe Dashboard → API keys (Live mode)

## 🔔 Step 2: Create Production Webhook

### 2.1 Go to Stripe Dashboard
1. Visit: https://dashboard.stripe.com/webhooks
2. Make sure you're in **LIVE MODE** (toggle in top-right should say "Viewing live data")

### 2.2 Create New Webhook
1. Click **"Add endpoint"**
2. **Endpoint URL:** `https://chanmianfeice-bot-a31829354d1b.herokuapp.com/webhook/stripe`
3. **Description:** "LINE Bot Payment Webhook"
4. **Events to send:** Select these events:
   - `checkout.session.completed` ✅ (This is the main one)
   - `customer.subscription.created` (optional)
   - `customer.subscription.updated` (optional)
   - `customer.subscription.deleted` (optional)

5. Click **"Add endpoint"**

### 2.3 Get Webhook Signing Secret
After creating the webhook, you'll see a page with webhook details.

1. Click **"Reveal"** next to "Signing secret"
2. Copy the secret (starts with `whsec_...`)
3. Update your `.env` file:
   ```bash
   STRIPE_WEBHOOK_SECRET=whsec_YOUR_SECRET_HERE
   ```

## 🚀 Step 3: Update Heroku Configuration

### 3.1 Set Heroku Environment Variables
Run these commands in **Windows Command Prompt or PowerShell**:

```bash
cd C:\Users\Administrator\Desktop\7755_clone\Desktop\7755

# Set live Stripe API key (starts with sk_live_)
heroku config:set STRIPE_API_KEY="<paste_your_live_key_here>"

# Set webhook secret (starts with whsec_)
heroku config:set STRIPE_WEBHOOK_SECRET="<paste_your_webhook_secret_here>"
```

### 3.2 Verify Configuration
```bash
heroku config:get STRIPE_API_KEY
heroku config:get STRIPE_WEBHOOK_SECRET
```

## 🧪 Step 4: Test Production Payment

### 4.1 Test with Real Card
**⚠️ WARNING: This will charge your card! Use a small amount for testing.**

1. Create a test character in LINE
2. Send 21 messages to trigger payment prompt
3. Click the payment link
4. Use a **REAL credit card** (test cards won't work in live mode)
5. Complete payment ($9.99 USD)

### 4.2 Verify Payment Worked
1. Check Stripe Dashboard → Payments (should show the transaction)
2. Send a message in LINE → should not show daily limit
3. Check Heroku logs: `heroku logs --tail`
   - Should see: "Webhook verified successfully"
   - Should see: "User upgraded to premium"

### 4.3 Test Webhook Delivery
1. Go to Stripe Dashboard → Webhooks
2. Click on your webhook endpoint
3. Check "Recent events" - should show `checkout.session.completed`
4. Status should be **"Succeeded"** (not "Failed")

## 🔐 Security Checklist

- ✅ Live API key is set (starts with `sk_live_`)
- ✅ Payment link is for live mode (not test mode)
- ✅ Webhook secret is set (starts with `whsec_`)
- ✅ Webhook endpoint is HTTPS (Heroku provides this)
- ✅ ENVIRONMENT should be set to "production" in Heroku

### Update Environment Variable (Optional but Recommended)
```bash
heroku config:set ENVIRONMENT=production
heroku config:set DEBUG=False
```

## 🚨 Important Notes

### Real Payments
- All payments will be **REAL** charges to customers
- Money will go to your Stripe account
- Refunds must be processed through Stripe Dashboard

### Test Cards Won't Work
In production mode, Stripe test cards (like 4242 4242 4242 4242) will be **REJECTED**.
Only real credit cards will work.

### Webhook Failures
If webhook fails:
1. Check Heroku logs: `heroku logs --tail | grep stripe`
2. Check Stripe Dashboard → Webhooks → "Recent events"
3. Common issues:
   - Wrong webhook secret
   - Webhook endpoint not deployed
   - Heroku app is down

## 📊 Monitor Payments

### Stripe Dashboard
- Payments: https://dashboard.stripe.com/payments
- Customers: https://dashboard.stripe.com/customers
- Webhooks: https://dashboard.stripe.com/webhooks

### Heroku Logs
```bash
# Watch all logs
heroku logs --tail

# Filter for Stripe events
heroku logs --tail | grep -i stripe

# Filter for webhook events
heroku logs --tail | grep webhook
```

## 🔙 Rollback to Test Mode (If Needed)

If something goes wrong, you can switch back to test mode:

```bash
# In .env file - use your test API key (starts with sk_test_)
STRIPE_API_KEY=<your_test_key_from_dashboard>

# Update Heroku
heroku config:set STRIPE_API_KEY="<your_test_key_here>"
```

Then use test webhook endpoint and test cards again.

## ✅ Production Checklist

- [ ] Switched `.env` to live API key
- [ ] Created production webhook in Stripe Dashboard
- [ ] Copied webhook secret to `.env`
- [ ] Updated Heroku config with `STRIPE_API_KEY`
- [ ] Updated Heroku config with `STRIPE_WEBHOOK_SECRET`
- [ ] Set `ENVIRONMENT=production` on Heroku
- [ ] Tested payment with real card
- [ ] Verified webhook receives events
- [ ] Verified premium status activates after payment
- [ ] Verified unlimited messages work

---

**Need Help?**
- Stripe Webhook Docs: https://docs.stripe.com/webhooks
- Stripe Testing Guide: https://docs.stripe.com/testing
- Your Stripe Dashboard: https://dashboard.stripe.com
