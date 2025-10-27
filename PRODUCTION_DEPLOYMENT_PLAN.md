# 🚀 Production Deployment Plan - LINE Chatbot Dating App

## 📊 Project Analysis Summary

### Current State ✅
- **Backend**: FastAPI with 22 RESTful endpoints
- **Database**: SQLite with 5 tables (Users, Characters, Messages, FavorabilityTracking, UserPreference)
- **Features**: Character generation, conversation management, favorability tracking, Chinese text conversion
- **Authentication**: ⚠️ Username-based only (no security)
- **Frontend**: Embedded HTML in FastAPI endpoints
- **Hosting**: Local development only

### Target Architecture 🎯
- **User Flow**: LINE Bot → Web Setup (one-time) → LINE Chat (ongoing)
- **Expected Users**: 1,000 users
- **Revenue**: Free initially → Stripe premium later
- **Budget**: <$20/month
- **Deployment**: Vercel (frontend) + Heroku (backend)

---

## 🏗️ Recommended Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      LINE Platform                          │
│  (User sends message via LINE app)                          │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │  LINE Messaging API   │
         │  (Webhook sends msg)  │
         └───────────┬───────────┘
                     │
                     ▼
    ┌────────────────────────────────────────┐
    │    Heroku - Backend API Server         │
    │    (FastAPI + Python)                  │
    │                                        │
    │  Endpoints:                            │
    │  • POST /webhook/line    [NEW]        │
    │  • GET  /setup?lineId=xxx [MODIFIED]  │
    │  • POST /api/v2/create-character      │
    │  • POST /api/v2/send-message          │
    │  • GET  /health                        │
    └────────┬────────────────────┬──────────┘
             │                    │
             ▼                    ▼
    ┌─────────────────┐   ┌──────────────────┐
    │  Supabase       │   │  SenseChat API   │
    │  PostgreSQL     │   │  (AI Response)   │
    │  (User Data)    │   └──────────────────┘
    └─────────────────┘
             │
             │ (Optional: Static hosting)
             ▼
    ┌─────────────────┐
    │  Vercel         │
    │  (Setup UI)     │
    │  (Static HTML)  │
    └─────────────────┘
```

---

## 🎯 Deployment Strategy Analysis

### Option A: Vercel-Only Deployment ❌ **NOT RECOMMENDED**

**Why NOT Vercel for Backend:**
- ❌ Vercel is optimized for **serverless functions** with 10-second timeout
- ❌ Your SenseChat API calls can take longer (multiple messages in history)
- ❌ No persistent file storage (can't use SQLite)
- ❌ Cold starts would make first message slow
- ❌ WebSocket/long-running connections not ideal
- ❌ Limited background processing

**Vercel is ONLY suitable for:**
- ✅ Static character setup UI
- ✅ Landing page
- ✅ Documentation

---

### Option B: Heroku-Only Deployment ✅ **RECOMMENDED**

**Why Heroku is PERFECT for your use case:**

#### Pricing (within budget):
```
Eco Dyno Plan: $5/month (sleeps after 30min inactivity)
Basic Dyno Plan: $7/month (never sleeps) ✅ RECOMMENDED
  - 512MB RAM
  - Can handle ~1000 concurrent users easily
  - 24/7 uptime
  - Custom domain support

Heroku Postgres Mini: $5/month ✅ RECOMMENDED
  - 10,000 rows (enough for MVP)
  - 1GB storage
  - 20 connections

TOTAL: $12/month (within $20 budget)
```

#### Why Heroku Wins:
- ✅ You're already comfortable with it
- ✅ Simple `git push heroku main` deployment
- ✅ Built-in PostgreSQL addon
- ✅ No cold starts with Basic dyno
- ✅ Environment variables management
- ✅ Free SSL certificates
- ✅ Easy scaling (just upgrade dyno)
- ✅ Logging & monitoring built-in
- ✅ Perfect for FastAPI + LINE webhooks
- ✅ Can handle long-running SenseChat API calls

#### Heroku Limitations to Know:
- ⚠️ Eco dyno sleeps after 30min → use Basic ($7/month)
- ⚠️ Limited to 512MB RAM on Basic → sufficient for 1000 users
- ⚠️ File system is ephemeral → use Supabase for database

---

### Option C: Hybrid (Vercel + Heroku) 🤔 **OPTIONAL**

```
Frontend (Vercel Free):           Backend (Heroku $12/month):
- Character setup UI              - LINE webhook handler
- Landing page                    - API endpoints
- Documentation                   - Database connections
- Static assets                   - SenseChat API calls
```

**Pros:**
- ✅ Separate concerns (frontend/backend)
- ✅ Vercel free tier for static content
- ✅ Better caching for static assets

**Cons:**
- ❌ More complex (2 deployments)
- ❌ CORS configuration needed
- ❌ Your UI is currently embedded in FastAPI

**Verdict:** **NOT worth the complexity for MVP**. Heroku can serve static HTML just fine.

---

## 📋 Recommended Tech Stack for Production

### Backend (Heroku)
```
Current:                          Production:
✅ FastAPI                        ✅ FastAPI (keep)
✅ SQLite                         ❌ → Supabase PostgreSQL
✅ Requests                       ✅ Requests (keep)
✅ OpenCC                         ✅ OpenCC (keep)
❌ No auth                        ✅ Add JWT auth
❌ No LINE SDK                    ✅ Add line-bot-sdk
❌ No rate limiting               ✅ Add slowapi
❌ No monitoring                  ✅ Add Sentry (error tracking)
```

### Database (Supabase)
```
Why Supabase over Heroku Postgres:
✅ Free tier: 500MB database (vs Heroku Mini $5/month)
✅ Realtime features (for future admin dashboard)
✅ Built-in backups
✅ Row Level Security (RLS)
✅ RESTful API auto-generated
✅ pgAdmin-like interface
✅ Better for long-term scaling

Cost: FREE for MVP → $25/month when you grow
```

### Frontend (Embedded in Heroku)
```
Current: HTML embedded in main.py ✅ Keep for MVP
Future: Separate React/Vue app (when you have budget)
```

---

## 🎬 User Flow in Production

### First-Time User Journey

```
1. User adds LINE Bot
   ↓
2. LINE sends "Follow Event" to your webhook
   ↓
3. Bot checks: Does user have character? → NO
   ↓
4. Bot sends welcome message via LINE:
   「歡迎！✨ 要開始使用，請先設定你的專屬角色：
    👉 https://your-app.herokuapp.com/setup?lineId=Uxxxxx」
   ↓
5. User clicks link → Opens web browser
   ↓
6. User fills character setup form (dream type, preferences)
   ↓
7. Click "生成角色" → POST /api/v2/create-character
   ↓
8. System creates character, saves to DB with LINE User ID mapping
   ↓
9. System sends FIRST MESSAGE via LINE Push API
   「嗨！我是小雨~ 很高興認識你 💕」
   ↓
10. User returns to LINE app → sees first message
    ↓
11. User replies → All future chats in LINE interface
```

### Returning User Journey

```
1. User sends message in LINE
   ↓
2. LINE webhook → POST /webhook/line
   ↓
3. Bot checks: Does user have character? → YES
   ↓
4. Extract message text → Call conversation_manager.send_message()
   ↓
5. Call SenseChat API → Get AI response
   ↓
6. Convert to Traditional Chinese (OpenCC)
   ↓
7. Reply via LINE Messaging API
   ↓
8. Update favorability tracking
```

---

## 🔧 Required Code Changes

### Critical Changes (Must Have)

#### 1. **LINE User ID Mapping**
**New Database Table:**
```python
class LineUserMapping(Base):
    __tablename__ = "line_user_mappings"

    mapping_id = Column(Integer, primary_key=True)
    line_user_id = Column(String(100), unique=True, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
```

#### 2. **LINE Webhook Handler**
**New Endpoint:**
```python
@app.post("/webhook/line")
async def line_webhook(request: Request):
    # Verify LINE signature
    # Parse LINE events (MessageEvent, FollowEvent, etc.)
    # Route to appropriate handler
    # Return 200 OK within 3 seconds
```

#### 3. **LINE Message Sender**
**New Module: `backend/line_client.py`**
```python
class LineClient:
    def send_reply(reply_token, message)
    def send_push(user_id, message)
    def send_flex_message(user_id, flex_json)
```

#### 4. **Modified Character Setup Endpoint**
**Update: `/api/v2/create-character`**
- Accept `line_user_id` parameter
- Create LineUserMapping entry
- Send first message via LINE Push API (not return in response)

#### 5. **PostgreSQL Migration**
**Tool: Alembic**
- Generate migration scripts from current SQLite schema
- Add new LineUserMapping table
- Migrate existing data (if any)

#### 6. **Authentication System**
**New Endpoints:**
```python
POST /api/auth/register
POST /api/auth/login
POST /api/auth/refresh
GET  /api/auth/me

Middleware: JWT token verification on protected endpoints
```

#### 7. **Rate Limiting**
```python
# Using slowapi
@limiter.limit("5/minute")  # 5 requests per minute per user
async def send_message(...)
```

---

## 📦 New Dependencies

```python
# requirements.txt additions:

# LINE Bot SDK
line-bot-sdk==3.5.0                    # Official LINE SDK

# Database
psycopg2-binary==2.9.9                 # PostgreSQL driver
alembic==1.12.1                        # Database migrations

# Authentication
python-jose[cryptography]==3.3.0       # JWT handling
passlib[bcrypt]==1.7.4                 # Password hashing

# Production essentials
slowapi==0.1.9                         # Rate limiting
sentry-sdk[fastapi]==1.38.0           # Error tracking
python-multipart==0.0.6               # Form data handling

# Deployment
gunicorn==21.2.0                       # Production WSGI server
```

---

## 🗂️ New File Structure

```
backend/
├── main.py                           # FastAPI app (existing)
├── database.py                       # Add LineUserMapping table
├── config.py                         # Add LINE credentials
├── line_client.py                    # [NEW] LINE API wrapper
├── line_handlers.py                  # [NEW] LINE event handlers
├── auth.py                           # [NEW] JWT authentication
├── middleware.py                     # [NEW] Auth & rate limiting
└── migrations/                       # [NEW] Alembic migrations
    ├── env.py
    └── versions/
        └── 001_initial_migration.py

.env (production)
├── DATABASE_URL=postgresql://...supabase.co:5432/postgres
├── LINE_CHANNEL_SECRET=...
├── LINE_CHANNEL_ACCESS_TOKEN=...
├── JWT_SECRET_KEY=...
├── SENTRY_DSN=...
└── (existing SenseChat credentials)
```

---

## 🚦 Deployment Roadmap

### Phase 0: Preparation (Day 1-2)
- [ ] Create Supabase account → Get PostgreSQL connection string
- [ ] Create Heroku account → Install Heroku CLI
- [ ] Create LINE Developers account → Get Channel Secret & Access Token
- [ ] Create Sentry account → Get DSN for error tracking
- [ ] Review & understand current codebase thoroughly

### Phase 1: Database Migration (Day 3-4)
- [ ] Install Alembic
- [ ] Generate migration from SQLite schema
- [ ] Add LineUserMapping table
- [ ] Test migration locally with PostgreSQL (Docker)
- [ ] Verify all queries work with PostgreSQL

### Phase 2: LINE Integration (Day 5-7)
- [ ] Install line-bot-sdk
- [ ] Create line_client.py wrapper
- [ ] Create line_handlers.py for events
- [ ] Implement webhook endpoint
- [ ] Test locally with ngrok (LINE webhook → local server)
- [ ] Implement LINE User ID mapping logic
- [ ] Modify character creation to send first message via LINE

### Phase 3: Security Hardening (Day 8-9)
- [ ] Implement JWT authentication
- [ ] Add password hashing for future user accounts
- [ ] Add rate limiting (slowapi)
- [ ] Restrict CORS to production domain
- [ ] Add request validation
- [ ] Add webhook signature verification

### Phase 4: Production Setup (Day 10-11)
- [ ] Create Heroku app
- [ ] Configure environment variables on Heroku
- [ ] Deploy to Heroku
- [ ] Configure Supabase connection
- [ ] Run database migrations on production
- [ ] Configure LINE webhook URL to Heroku app
- [ ] Test end-to-end flow

### Phase 5: Monitoring & Testing (Day 12-13)
- [ ] Integrate Sentry for error tracking
- [ ] Test with real LINE accounts
- [ ] Load testing (simulate 100 concurrent users)
- [ ] Fix bugs found during testing
- [ ] Setup automated backups on Supabase

### Phase 6: Soft Launch (Day 14)
- [ ] Private beta with 10-20 friends
- [ ] Monitor errors & performance
- [ ] Gather feedback
- [ ] Iterate quickly

### Phase 7: Public Launch (Day 15+)
- [ ] Public announcement
- [ ] Monitor server metrics
- [ ] Scale if needed (upgrade Heroku dyno)

**Total Time Estimate: 2-3 weeks of focused work**

---

## 💰 Cost Breakdown

### MVP (Free Tier + Minimal Paid)

```
Service              Plan                Cost/Month    Notes
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Heroku Dyno          Basic               $7           Never sleeps
Supabase             Free Tier           $0           500MB, 2GB bandwidth
LINE Platform        Free                $0           Free messaging API
SenseChat API        Free Tier*          $0           Check usage limits
Sentry               Free Tier           $0           5K errors/month
Domain (optional)    Namecheap           $1-2/year    Optional

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL                                    $7/month     ✅ Well under budget!
```

*Note: Verify SenseChat API pricing - your current plan shows 60 RPM limit

### Scaling Plan (When You Hit Limits)

```
1000+ Active Users:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Heroku Dyno          Standard-1X         $25          Better performance
Supabase             Pro                 $25          8GB, better support
Sentry               Team                $26          50K errors/month (optional)

TOTAL                                    $50-76/month
```

### Premium Features (Future)

```
Stripe Integration:
- Transaction fee: 2.9% + $0.30 per successful charge
- No monthly fee for basic plan
- Example: $5 premium feature → You keep ~$4.50
```

---

## 🛡️ Security Checklist

### Must Have Before Launch
- [ ] Environment variables stored securely (not in code)
- [ ] LINE webhook signature verification
- [ ] HTTPS enabled (Heroku provides free SSL)
- [ ] Rate limiting on all endpoints (prevent abuse)
- [ ] Input validation on all user inputs
- [ ] SQL injection prevention (SQLAlchemy handles this)
- [ ] CORS restricted to production domains only
- [ ] Secrets rotation capability

### Should Have
- [ ] JWT token with short expiry (15min access, 7day refresh)
- [ ] User authentication for web UI
- [ ] Database connection pooling
- [ ] Error messages don't leak sensitive info
- [ ] Logging excludes sensitive data (passwords, tokens)

### Nice to Have
- [ ] Two-factor authentication (2FA)
- [ ] IP-based blocking for abusive users
- [ ] Honeypot endpoints for bot detection
- [ ] Regular security audits

---

## 📊 Monitoring & Analytics

### Essential Metrics to Track

```
User Metrics:
- Daily Active Users (DAU)
- Monthly Active Users (MAU)
- New user signups per day
- Character creation rate
- Average messages per user
- Retention rate (Day 1, Day 7, Day 30)

Technical Metrics:
- API response time (p50, p95, p99)
- Error rate (4xx, 5xx)
- SenseChat API success rate
- Database query performance
- Webhook response time (must be <3s)

Business Metrics:
- Conversion rate (followers → character creators)
- Cost per user (server cost / active users)
- SenseChat API usage per user
```

### Tools
```
Free Tier:
- Heroku Metrics (built-in)
- Sentry (error tracking)
- Supabase Dashboard (DB metrics)
- LINE Official Account Manager (messaging stats)

Paid (when needed):
- Datadog / New Relic (APM)
- Mixpanel / Amplitude (user analytics)
```

---

## 🎯 Key Technical Challenges & Solutions

### Challenge 1: LINE 3-Second Timeout
**Problem:** SenseChat API can take 5-10 seconds for long conversations

**Solution:**
```python
# Option A: Immediate acknowledgment + Push API
@app.post("/webhook/line")
async def webhook(request: Request):
    # Respond immediately
    background_tasks.add_task(process_message_async, event)
    return JSONResponse({"status": "ok"}, status_code=200)

async def process_message_async(event):
    # Process in background
    response = await conversation_manager.send_message(...)
    # Send via Push API
    line_client.send_push(user_id, response)

# Option B: Typing indicator
line_client.send_typing_animation(user_id)  # Shows "..." in LINE
# Then process and send real message
```

### Challenge 2: User Identification
**Problem:** LINE User IDs are opaque (Uxxxxx), need to map to your users

**Solution:**
```python
# Store mapping in database
LINE User ID (Uxxxxx) ←→ Internal User ID (integer)
                      ↓
              Linked to Characters
```

### Challenge 3: Character Selection
**Problem:** Users might create multiple characters, which one to use in LINE?

**Solution:**
```python
# Option A: One character per user (simplest)
- When user creates 2nd character, replace the first
- Show warning: "This will replace your current character"

# Option B: Active character system
- User can create multiple, select "active" one
- Use LINE Rich Menu with "Switch Character" button

# Recommendation: Start with Option A for MVP
```

### Challenge 4: Database Migration
**Problem:** SQLite → PostgreSQL without data loss

**Solution:**
```bash
# Use pgloader (automated migration)
pgloader sqlite://dating_chatbot.db postgresql://user:pass@supabase.co/db

# Or manual export/import
sqlite3 dating_chatbot.db .dump > backup.sql
# Edit SQL for PostgreSQL compatibility
psql -h supabase.co -U user -d db -f backup.sql
```

### Challenge 5: Cost Control
**Problem:** SenseChat API costs could spike with 1000 users

**Solution:**
```python
# Rate limiting per user
- Max 20 messages per day per user (free tier)
- Premium users: unlimited

# Conversation caching
- Cache common responses
- Reuse character descriptions

# Usage monitoring
@app.middleware("http")
async def track_api_usage(request, call_next):
    # Log SenseChat API calls
    # Alert if approaching limits
```

---

## 🚨 Risk Assessment

### High Risk
| Risk | Impact | Mitigation |
|------|--------|------------|
| SenseChat API rate limit (60 RPM) | Can't serve users | Cache responses, queue requests, upgrade plan |
| Heroku dyno crash | Service down | Health checks, auto-restart, monitoring alerts |
| Database corruption | Data loss | Daily automated backups, point-in-time recovery |
| LINE webhook downtime | Messages lost | Retry mechanism, queue system |

### Medium Risk
| Risk | Impact | Mitigation |
|------|--------|------------|
| Unexpected costs | Budget overrun | Set billing alerts, monitor usage daily |
| Character quality issues | User dissatisfaction | A/B test prompts, gather feedback |
| Slow response time | Poor UX | Optimize queries, upgrade dyno if needed |

### Low Risk
| Risk | Impact | Mitigation |
|------|--------|------------|
| UI bugs | Minor UX issues | Testing, beta launch first |
| Translation errors | Confusion | Use OpenCC (already implemented) |

---

## ✅ Success Criteria

### MVP Launch (Week 3)
- [ ] 10 beta users successfully create characters
- [ ] 100+ messages exchanged via LINE
- [ ] <2 second average response time
- [ ] 99% uptime over 1 week
- [ ] Zero data loss incidents
- [ ] <3 critical bugs

### Month 1 Goals
- [ ] 100 active users
- [ ] 80% user retention (Day 7)
- [ ] <$20/month operational cost
- [ ] Positive user feedback (survey)
- [ ] Plan for premium features

### Month 3 Goals
- [ ] 500 active users
- [ ] Revenue from premium features
- [ ] Feature parity with competitors
- [ ] Scaling plan documented

---

## 📚 Required Learning Resources

### For You to Study (if not familiar):
1. **LINE Messaging API Docs**: https://developers.line.biz/en/docs/messaging-api/
2. **Heroku FastAPI Deployment**: https://devcenter.heroku.com/articles/python-gunicorn
3. **Supabase + Python**: https://supabase.com/docs/reference/python
4. **Alembic (DB migrations)**: https://alembic.sqlalchemy.org/en/latest/tutorial.html
5. **FastAPI JWT Auth**: https://fastapi.tiangolo.com/tutorial/security/

### Estimated Learning Time:
- LINE API: 4-6 hours (read docs + examples)
- Heroku deployment: 2-3 hours (if first time)
- Supabase setup: 1-2 hours
- Alembic migrations: 2-3 hours
- **Total: ~10-14 hours of learning**

---

## 🎓 Next Steps (In Order)

### Immediate (This Week)
1. **Review this plan thoroughly** - Ask questions, clarify doubts
2. **Sign up for accounts**:
   - Supabase (free)
   - Heroku (add credit card for Basic dyno)
   - LINE Developers Console
   - Sentry (free)

3. **Local testing setup**:
   - Install PostgreSQL locally (or use Docker)
   - Test database migration SQLite → PostgreSQL
   - Ensure all tests pass with PostgreSQL

### Week 1: Development
1. Implement LINE webhook handler
2. Test with ngrok (local development)
3. Implement LINE User ID mapping
4. Test character creation → LINE first message flow

### Week 2: Deployment
1. Deploy to Heroku
2. Configure production database (Supabase)
3. Set up monitoring (Sentry)
4. End-to-end testing

### Week 3: Launch
1. Private beta (10 users)
2. Fix critical bugs
3. Public soft launch
4. Monitor & iterate

---

## 🤔 Open Questions for You

1. **LINE Bot Name & Description**: What will your bot be called?
2. **Character Limits**:
   - How many characters can one user create? (Recommend: 1 for MVP)
   - Should users be able to switch characters? (Recommend: Not for MVP)
3. **Premium Features**:
   - What would you charge for? (More messages/day? Multiple characters?)
   - Price point? ($2-5/month typical)
4. **Language**: Traditional Chinese only, or support other languages later?
5. **Age Restriction**: Any age verification needed? (Dating content)
6. **Terms of Service**: Need legal review? (Data privacy, user content)

---

## 📞 Support & Assistance

When you're ready to proceed, I can help you with:

1. ✅ **LINE webhook implementation** - Complete code with explanations
2. ✅ **Database migration script** - SQLite → PostgreSQL with data preservation
3. ✅ **Heroku deployment config** - Procfile, runtime.txt, environment setup
4. ✅ **Authentication system** - JWT-based API security
5. ✅ **Testing scripts** - Automated tests for LINE integration
6. ✅ **Monitoring setup** - Sentry integration, logging configuration
7. ✅ **Cost optimization** - Tips to stay under budget

**Just let me know when you want to start coding!** 🚀

---

## 📝 Summary

**Recommended Stack:**
- **Backend**: Heroku Basic Dyno ($7/month)
- **Database**: Supabase Free Tier ($0/month)
- **LINE Bot**: Free
- **Monitoring**: Sentry Free Tier ($0/month)
- **Total**: **$7/month** ✅

**Timeline**: 2-3 weeks to production
**Risk**: Low (proven stack, no vendor lock-in)
**Scalability**: Can easily handle 1000 users, upgrade path clear
**Your Comfort**: High (Heroku familiarity, straightforward deployment)

**Next Action**: Review plan → Ask questions → Get approval → Start implementation 🎯
