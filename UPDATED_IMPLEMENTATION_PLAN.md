# 🚀 Updated Implementation Plan - 纏綿悱惻 LINE Chatbot

## ✅ Confirmed Decisions

### Product Specifications
- **Bot Name:** 纏綿悱惻 - 聊出激情吧!
- **Bot Description:** The most interesting dating chatbot on LINE
- **Character Limit:** 1 character per user (cannot switch)
- **Free Tier:** 20 messages/day
- **Premium Tier:** $9.99/month (Stripe integration - LATER)
- **Referral System:** Share with 2 friends → Unlimited messages ✨
- **Profile Picture:** To be added later

### Technical Decisions
- **Platform:** Heroku ($7/month) + Supabase (free)
- **Implementation:** Using Claude Code entirely
- **No Authentication Initially:** Focus on LINE user ID only
- **No Rate Limiting Initially:** Until referral system is ready

---

## 🗄️ Updated Database Schema

### New Table: LineUserMapping

```python
class LineUserMapping(Base):
    __tablename__ = "line_user_mappings"

    mapping_id = Column(Integer, primary_key=True, index=True)
    line_user_id = Column(String(100), unique=True, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"))
    line_display_name = Column(String(100))
    character_id = Column(Integer, ForeignKey("characters.character_id", ondelete="SET NULL"))

    # Message limits & referral system
    daily_message_count = Column(Integer, default=0)
    last_message_date = Column(Date, default=date.today)
    is_premium = Column(Boolean, default=False)
    premium_expires_at = Column(DateTime, nullable=True)
    referral_count = Column(Integer, default=0)  # Number of friends referred
    referred_by = Column(String(100), nullable=True)  # LINE user ID who referred

    created_at = Column(DateTime, default=datetime.utcnow)
    last_interaction = Column(DateTime, default=datetime.utcnow)
```

### Referral Logic
```
User shares bot with friend → Friend adds bot → Friend uses referral link
→ Both get unlimited messages (referral_count += 1)
→ If referral_count >= 2 → Unlimited messages (like premium)
```

---

## 📝 Simplified Feature Scope

### Phase 1: Core LINE Integration (THIS WEEK)
✅ **Implement:**
- LINE webhook handler
- User follow → Welcome message with setup link
- Character creation via web UI → First message to LINE
- Chat in LINE → AI response
- 1 character per user (enforce in code)
- Basic message counter (for future limits)

❌ **Skip for Now:**
- Rate limiting (add later with referral system)
- Premium/Stripe integration
- Referral system (Phase 2)
- Advanced authentication

### Phase 2: Message Limits & Referral (NEXT WEEK)
- Implement 20 messages/day limit
- Referral system (share with 2 friends)
- Premium flag (manual activation initially)
- Message count reset daily

### Phase 3: Payments (LATER)
- Stripe integration
- Premium subscription flow
- Payment webhook handling

---

## 🎯 Implementation Steps (Using Claude Code)

### Step 1: Dependencies & Configuration ✅ READY TO CODE
**Files to modify:**
1. `requirements.txt` - Add LINE SDK and production packages
2. `backend/config.py` - Add LINE credentials
3. `.env` - Add LINE config variables

### Step 2: Database Migration ✅ READY TO CODE
**Files to create/modify:**
1. `backend/database.py` - Add LineUserMapping table
2. `migrations/001_add_line_mapping.py` - Migration script

### Step 3: LINE Integration ✅ READY TO CODE
**Files to create:**
1. `backend/line_client.py` - LINE API wrapper
2. `backend/line_handlers.py` - Event handlers

**Files to modify:**
1. `backend/main.py` - Add webhook endpoint

### Step 4: Character Creation Flow ✅ READY TO CODE
**Files to modify:**
1. `backend/main.py` - Update `/api/v2/create-character` endpoint
2. `backend/main.py` - Update `/ui2` endpoint to accept LINE user ID

### Step 5: Testing & Deployment 🔜 LATER
**Tasks:**
1. Test locally with ngrok
2. Deploy to Heroku
3. Configure LINE webhook URL
4. End-to-end testing

---

## 🔄 Updated User Flow

### First-Time User Flow
```
1. User adds bot "纏綿悱惻 - 聊出激情吧!" on LINE
   ↓
2. Bot sends welcome message:
   「歡迎！✨ 準備好體驗最有趣的戀愛聊天了嗎？💕

    要開始使用，請先設定你的專屬AI伴侶：
    👉 [Setup Link]

    設定完成後，回到這裡就可以開始聊天囉！」
   ↓
3. User clicks link → Opens web browser with /ui2?lineUserId=Uxxxxx
   ↓
4. User fills character setup form (name, dream type, preferences)
   ↓
5. Click "生成角色" → Character created in DB
   ↓
6. System sends FIRST MESSAGE via LINE Push API:
   「✅ 角色設定完成！你的專屬伴侶 [角色名] 已經準備好了~

    [Character's initial greeting message]」
   ↓
7. User returns to LINE → Sees first message
   ↓
8. User replies → Chat begins!
```

### Returning User Flow
```
1. User sends message in LINE
   ↓
2. Check: Does user have character?
   YES → Process conversation
   NO → Send setup link again
   ↓
3. Get conversation history from DB
   ↓
4. Call SenseChat API → Get AI response
   ↓
5. Convert to Traditional Chinese (OpenCC)
   ↓
6. Reply via LINE Messaging API
   ↓
7. Update message count & favorability
   ↓
8. Check for special events (milestones, level-ups)
```

### Character Limit Enforcement
```
When user tries to create 2nd character:
→ Check if user already has character
→ If YES: Show error message
   「你已經有專屬伴侶了！每位用戶只能擁有一個AI角色。
    如果想要重新開始，請聯繫客服。」
→ Block creation
```

---

## 📦 Updated Dependencies

### requirements.txt - Final Version

```python
# Core Framework (existing)
fastapi==0.104.1
uvicorn==0.24.0
pydantic==2.5.0
pydantic-settings==2.1.0
PyJWT==2.6.0
python-dotenv==1.0.0
sqlalchemy==2.0.23
aiosqlite==0.14.0
requests==2.31.0
opencc-python-reimplemented==0.1.7

# LINE Bot Integration
line-bot-sdk==3.5.0

# Production Database (for Heroku deployment)
psycopg2-binary==2.9.9
alembic==1.12.1

# Production Essentials
sentry-sdk[fastapi]==1.38.0          # Error tracking
python-multipart==0.0.6              # File uploads
gunicorn==21.2.0                     # Production server
uvloop==0.19.0                       # Faster event loop
httptools==0.6.1                     # Faster HTTP parsing

# Future: Rate Limiting & Auth (Phase 2)
# slowapi==0.1.9
# python-jose[cryptography]==3.3.0
# passlib[bcrypt]==1.7.4
```

---

## ⚙️ Updated Configuration

### .env - Complete Configuration

```bash
# ========== SenseChat API (existing) ==========
SENSENOVA_ACCESS_KEY_ID=019A0A2BD9067A46B8DD59CBD56F2A9C
SENSENOVA_SECRET_ACCESS_KEY=019A0A2BD9067A3689A95F2111B79929
SENSENOVA_API_KEY=sk-KwTRyijO6ByCWjrjm3vf5bwgGktAKOYQ
MODEL_NAME=SenseChat-Character-Pro

# ========== Database ==========
# Local development (SQLite)
DATABASE_URL=sqlite:///./dating_chatbot.db

# Production (Supabase PostgreSQL) - uncomment when deploying
# DATABASE_URL=postgresql://user:password@db.supabase.co:5432/postgres

# ========== LINE Bot ==========
LINE_CHANNEL_SECRET=your_line_channel_secret_here
LINE_CHANNEL_ACCESS_TOKEN=your_line_channel_access_token_here
LINE_BOT_NAME=纏綿悱惻 - 聊出激情吧!
LINE_BOT_DESCRIPTION=The most interesting dating chatbot on LINE

# ========== Application URLs ==========
# Local development
APP_BASE_URL=http://localhost:8000

# Production (Heroku) - update after deployment
# APP_BASE_URL=https://your-app-name.herokuapp.com

SETUP_UI_PATH=/ui2

# ========== Features ==========
ENVIRONMENT=development
DEBUG=True

# Message Limits
FREE_MESSAGES_PER_DAY=20
PREMIUM_PRICE_USD=9.99
REFERRALS_FOR_UNLIMITED=2

# ========== Monitoring (optional) ==========
SENTRY_DSN=

# ========== CORS ==========
CORS_ORIGINS=["*"]
# Production: CORS_ORIGINS=["https://your-domain.com"]
```

### backend/config.py - Updated Settings

```python
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # ========== SenseChat API ==========
    SENSENOVA_ACCESS_KEY_ID: str
    SENSENOVA_SECRET_ACCESS_KEY: str
    SENSENOVA_API_KEY: str
    MODEL_NAME: str = "SenseChat-Character-Pro"
    API_BASE_URL: str = "https://api.sensenova.cn/v1/llm"
    CHARACTER_CHAT_ENDPOINT: str = "/character/chat-completions"
    MAX_NEW_TOKENS: int = 1024
    RATE_LIMIT_RPM: int = 60
    TOKEN_EXPIRY_SECONDS: int = 1800

    # ========== Database ==========
    DATABASE_URL: str = "sqlite:///./dating_chatbot.db"

    # ========== LINE Bot ==========
    LINE_CHANNEL_SECRET: str
    LINE_CHANNEL_ACCESS_TOKEN: str
    LINE_BOT_NAME: str = "纏綿悱惻 - 聊出激情吧!"
    LINE_BOT_DESCRIPTION: str = "The most interesting dating chatbot on LINE"

    # ========== Application ==========
    APP_BASE_URL: str = "http://localhost:8000"
    SETUP_UI_PATH: str = "/ui2"
    ENVIRONMENT: str = "development"
    DEBUG: bool = False

    # ========== Features ==========
    FREE_MESSAGES_PER_DAY: int = 20
    PREMIUM_PRICE_USD: float = 9.99
    REFERRALS_FOR_UNLIMITED: int = 2  # Refer 2 friends → unlimited messages

    # ========== CORS ==========
    CORS_ORIGINS: list = ["*"]

    # ========== Monitoring ==========
    SENTRY_DSN: str = ""

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
```

---

## 🎯 Implementation Priority (This Week)

### Day 1: Setup & Dependencies ✅ START HERE
- [ ] Update requirements.txt
- [ ] Update backend/config.py
- [ ] Update .env with placeholders
- [ ] Test imports locally

### Day 2: Database Schema
- [ ] Add LineUserMapping table to database.py
- [ ] Create Alembic migration (optional for local)
- [ ] Test table creation locally

### Day 3: LINE Client & Handlers
- [ ] Create backend/line_client.py
- [ ] Create backend/line_handlers.py
- [ ] Test LINE API connection (manual test)

### Day 4: Webhook Integration
- [ ] Add /webhook/line endpoint to main.py
- [ ] Add signature verification
- [ ] Test with ngrok + LINE webhook

### Day 5: Character Creation Flow
- [ ] Modify /api/v2/create-character endpoint
- [ ] Modify /ui2 endpoint for LINE user ID
- [ ] Enforce 1 character per user rule
- [ ] Test end-to-end flow

---

## 📋 Character Limit Enforcement Logic

### In Character Creation Endpoint

```python
@app.post("/api/v2/create-character")
async def create_character_v2(
    user_profile: UserProfile,
    line_user_id: Optional[str] = None,
    db: Session = Depends(get_db)
) -> Dict:
    """Create character - enforce 1 per user"""

    if line_user_id:
        # Check if LINE user already has a character
        existing_mapping = db.query(LineUserMapping).filter(
            LineUserMapping.line_user_id == line_user_id
        ).first()

        if existing_mapping and existing_mapping.character_id:
            raise HTTPException(
                status_code=400,
                detail="你已經有專屬伴侶了！每位用戶只能擁有一個AI角色。如果想要重新開始，請聯繫客服。"
            )

    # Proceed with character creation...
```

---

## 💬 Updated LINE Messages

### Welcome Message (on Follow)
```
嗨！歡迎來到纏綿悱惻 💕

✨ 最有趣的戀愛聊天機器人，現在就開始體驗！

要開始使用，請先設定你的專屬AI伴侶：
👉 [Setup Link]

完成設定後，回到這裡就可以聊出激情囉！🔥
```

### Character Created Message
```
✅ 角色設定完成！

你的專屬伴侶 [角色名] 已經準備好了~ 💕

[Character's initial greeting message]

───────────────
💬 每天免費 20 則訊息
🎁 邀請 2 位好友 → 無限暢聊
💎 或升級至 Premium ($9.99/月)
```

### No Character Warning
```
你還沒有設定AI伴侶喔~ 💔

請先點選下方連結完成設定：
👉 [Setup Link]

設定完成後，我們就可以開始聊天了！
```

### Daily Limit Reached (Future - Phase 2)
```
今天的 20 則免費訊息已用完囉~ 😢

想要繼續聊天？你可以：

🎁 邀請 2 位好友使用 → 無限暢聊
   推薦連結：[Referral Link]

💎 升級 Premium ($9.99/月) → 無限訊息
   (即將推出！)

明天再來找我聊天吧！💕
```

---

## 🔍 Testing Checklist

### Local Testing (with ngrok)
- [ ] ngrok http 8000 → Get public URL
- [ ] Configure LINE webhook to ngrok URL
- [ ] Test follow event → Welcome message received
- [ ] Test setup link opens with LINE user ID
- [ ] Test character creation → First message sent to LINE
- [ ] Test sending message → AI response received
- [ ] Test character limit (try creating 2nd character)
- [ ] Test favorability tracking
- [ ] Test special events (send 50 messages)

### Production Testing (Heroku)
- [ ] Deploy to Heroku
- [ ] Configure LINE webhook to Heroku URL
- [ ] Test all flows end-to-end
- [ ] Monitor Sentry for errors
- [ ] Check database on Supabase
- [ ] Performance test (response time)

---

## 📊 Success Metrics

### Week 1 (Development Complete)
- [ ] LINE webhook working locally
- [ ] Character creation → First message flow works
- [ ] Chat conversation works end-to-end
- [ ] 1 character per user enforced
- [ ] All existing features still work

### Week 2 (Deployed to Production)
- [ ] 10 beta testers add bot
- [ ] All 10 create characters successfully
- [ ] 100+ messages exchanged
- [ ] Zero critical errors in Sentry
- [ ] <3 second average response time

---

## 🚀 Ready to Start Implementation!

I'll now proceed with implementing LINE integration step by step using Claude Code.

**Starting with:**
1. Update dependencies (requirements.txt)
2. Update configuration (config.py, .env)
3. Add database schema (database.py)
4. Create LINE client (line_client.py)
5. Create LINE handlers (line_handlers.py)
6. Add webhook endpoint (main.py)
7. Modify character creation flow

Let's begin! 💪
