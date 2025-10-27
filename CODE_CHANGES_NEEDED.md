# 📝 Required Code Changes for Production LINE Bot

## 🎯 Overview

This document details every code change needed to transform your current web-based chatbot into a production LINE bot.

**Current State:** Web UI → Character creation → Test chat
**Target State:** LINE bot → Web setup link → Chat in LINE

---

## 📦 1. New Dependencies to Add

### requirements.txt - Additions

```python
# Current dependencies (keep all):
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

# ========== ADD THESE ==========

# LINE Bot SDK
line-bot-sdk==3.5.0                    # Official LINE Messaging API SDK

# Production Database
psycopg2-binary==2.9.9                 # PostgreSQL driver (for Supabase)
alembic==1.12.1                        # Database migrations

# Authentication & Security
python-jose[cryptography]==3.3.0       # JWT token handling
passlib[bcrypt]==1.7.4                 # Password hashing
slowapi==0.1.9                         # Rate limiting

# Monitoring & Production
sentry-sdk[fastapi]==1.38.0           # Error tracking
python-multipart==0.0.6               # File upload support
gunicorn==21.2.0                       # Production WSGI server
uvloop==0.19.0                         # Faster event loop
httptools==0.6.1                       # Faster HTTP parsing

# Background Tasks
celery==5.3.4                          # Optional: For async task processing
redis==5.0.1                           # Optional: For Celery backend
```

---

## 🗄️ 2. Database Schema Changes

### backend/database.py - Add New Table

**Location in file:** After `UserPreference` class (around line 100)

```python
# ADD THIS NEW TABLE:
class LineUserMapping(Base):
    """Maps LINE User IDs to internal user IDs"""
    __tablename__ = "line_user_mappings"

    mapping_id = Column(Integer, primary_key=True, index=True)
    line_user_id = Column(String(100), unique=True, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    line_display_name = Column(String(100))  # Optional: store LINE display name
    active_character_id = Column(Integer, ForeignKey("characters.character_id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_interaction = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="line_mappings")
    active_character = relationship("Character", foreign_keys=[active_character_id])

    def __repr__(self):
        return f"<LineUserMapping(line_user_id='{self.line_user_id}', user_id={self.user_id})>"


# MODIFY User class to add relationship:
class User(Base):
    # ... existing code ...

    # ADD THIS LINE to relationships:
    line_mappings = relationship("LineUserMapping", back_populates="user", cascade="all, delete-orphan")
```

### Migration Script

**New file:** `migrations/001_add_line_mapping.py`

```python
"""Add LINE user mapping table

Revision ID: 001
Create Date: 2025-01-XX
"""

from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table(
        'line_user_mappings',
        sa.Column('mapping_id', sa.Integer(), nullable=False),
        sa.Column('line_user_id', sa.String(100), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('line_display_name', sa.String(100), nullable=True),
        sa.Column('active_character_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('last_interaction', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['active_character_id'], ['characters.character_id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('mapping_id')
    )
    op.create_index('ix_line_user_mappings_line_user_id', 'line_user_mappings', ['line_user_id'], unique=True)
    op.create_index('ix_line_user_mappings_mapping_id', 'line_user_mappings', ['mapping_id'])

def downgrade():
    op.drop_index('ix_line_user_mappings_mapping_id')
    op.drop_index('ix_line_user_mappings_line_user_id')
    op.drop_table('line_user_mappings')
```

---

## ⚙️ 3. Configuration Changes

### backend/config.py - Add LINE Credentials

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # ========== EXISTING (keep all) ==========
    SENSENOVA_ACCESS_KEY_ID: str
    SENSENOVA_SECRET_ACCESS_KEY: str
    SENSENOVA_API_KEY: str
    MODEL_NAME: str = "SenseChat-Character-Pro"
    API_BASE_URL: str = "https://api.sensenova.cn/v1/llm"
    CHARACTER_CHAT_ENDPOINT: str = "/character/chat-completions"
    DATABASE_URL: str = "sqlite:///./dating_chatbot.db"
    MAX_NEW_TOKENS: int = 1024
    RATE_LIMIT_RPM: int = 60
    TOKEN_EXPIRY_SECONDS: int = 1800

    # ========== ADD THESE ==========

    # LINE Bot Configuration
    LINE_CHANNEL_SECRET: str                    # From LINE Developers Console
    LINE_CHANNEL_ACCESS_TOKEN: str              # From LINE Developers Console
    LINE_LIFF_ID: str = ""                      # Optional: For LINE Front-end Framework

    # Application URLs
    APP_BASE_URL: str = "https://your-app.herokuapp.com"  # Will be your Heroku URL
    SETUP_UI_PATH: str = "/ui2"                 # Path to character setup page

    # Security
    JWT_SECRET_KEY: str = "CHANGE_THIS_IN_PRODUCTION_TO_RANDOM_STRING"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Rate Limiting
    RATE_LIMIT_PER_USER_PER_MINUTE: int = 5
    RATE_LIMIT_PER_USER_PER_DAY: int = 100      # Free tier message limit

    # Environment
    ENVIRONMENT: str = "development"            # development, staging, production
    DEBUG: bool = False

    # Monitoring
    SENTRY_DSN: str = ""                        # Optional: Sentry error tracking

    # CORS
    CORS_ORIGINS: list = ["*"]                  # In production: ["https://your-domain.com"]

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
```

### .env - Add New Variables

```bash
# ========== EXISTING (keep) ==========
SENSENOVA_ACCESS_KEY_ID=019A0A2BD9067A46B8DD59CBD56F2A9C
SENSENOVA_SECRET_ACCESS_KEY=019A0A2BD9067A3689A95F2111B79929
SENSENOVA_API_KEY=sk-KwTRyijO6ByCWjrjm3vf5bwgGktAKOYQ
MODEL_NAME=SenseChat-Character-Pro
DATABASE_URL=sqlite:///./dating_chatbot.db

# ========== ADD THESE ==========

# LINE Bot Credentials (get from LINE Developers Console)
LINE_CHANNEL_SECRET=your_channel_secret_here
LINE_CHANNEL_ACCESS_TOKEN=your_channel_access_token_here

# Application URLs
APP_BASE_URL=http://localhost:8000          # Local dev
# APP_BASE_URL=https://your-app.herokuapp.com  # Production

# Security (CHANGE IN PRODUCTION!)
JWT_SECRET_KEY=your-super-secret-key-change-this-in-production

# Environment
ENVIRONMENT=development
DEBUG=True

# Sentry (optional)
SENTRY_DSN=

# Database (for production - Supabase)
# DATABASE_URL=postgresql://user:password@db.supabase.co:5432/postgres
```

---

## 📄 4. New Files to Create

### File: backend/line_client.py

**Purpose:** Wrapper for LINE Messaging API

```python
"""
LINE Messaging API Client
Handles sending messages, push messages, and rich content to LINE users
"""

from linebot import LineBotApi, WebhookHandler
from linebot.models import (
    TextSendMessage,
    ImageSendMessage,
    TemplateSendMessage,
    ButtonsTemplate,
    MessageAction,
    URIAction,
    FlexSendMessage
)
from linebot.exceptions import LineBotApiError
import logging

from backend.config import settings

logger = logging.getLogger(__name__)


class LineClient:
    """Client for interacting with LINE Messaging API"""

    def __init__(self):
        self.line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
        self.handler = WebhookHandler(settings.LINE_CHANNEL_SECRET)

    def reply_message(self, reply_token: str, text: str) -> bool:
        """
        Reply to a message using reply token

        Args:
            reply_token: Reply token from LINE webhook event
            text: Message text to send

        Returns:
            True if successful, False otherwise
        """
        try:
            self.line_bot_api.reply_message(
                reply_token,
                TextSendMessage(text=text)
            )
            logger.info(f"Replied to message: {text[:50]}...")
            return True
        except LineBotApiError as e:
            logger.error(f"Failed to reply message: {e.status_code} - {e.error.message}")
            return False

    def push_message(self, user_id: str, text: str) -> bool:
        """
        Push a message to user (not a reply)

        Args:
            user_id: LINE user ID
            text: Message text to send

        Returns:
            True if successful, False otherwise
        """
        try:
            self.line_bot_api.push_message(
                user_id,
                TextSendMessage(text=text)
            )
            logger.info(f"Pushed message to {user_id}: {text[:50]}...")
            return True
        except LineBotApiError as e:
            logger.error(f"Failed to push message: {e.status_code} - {e.error.message}")
            return False

    def send_welcome_message(self, user_id: str, user_name: str = "朋友") -> bool:
        """
        Send welcome message with setup link

        Args:
            user_id: LINE user ID
            user_name: User's display name from LINE

        Returns:
            True if successful
        """
        setup_url = f"{settings.APP_BASE_URL}{settings.SETUP_UI_PATH}?lineUserId={user_id}"

        message = f"""嗨 {user_name}！✨ 歡迎使用戀愛聊天機器人 💕

要開始使用，請先設定你的專屬AI伴侶：
👉 {setup_url}

完成設定後，回到這裡就可以開始聊天囉！"""

        return self.push_message(user_id, message)

    def send_character_created_message(
        self,
        user_id: str,
        character_name: str,
        initial_message: str
    ) -> bool:
        """
        Send message when character is created

        Args:
            user_id: LINE user ID
            character_name: Created character's name
            initial_message: Character's first message

        Returns:
            True if successful
        """
        setup_complete_msg = f"✅ 角色設定完成！你的專屬伴侶 {character_name} 已經準備好了~\n\n"
        full_message = setup_complete_msg + initial_message

        return self.push_message(user_id, full_message)

    def send_buttons_template(
        self,
        user_id: str,
        title: str,
        text: str,
        actions: list
    ) -> bool:
        """
        Send a buttons template message (for menus, choices)

        Args:
            user_id: LINE user ID
            title: Template title
            text: Template text
            actions: List of actions (buttons)

        Returns:
            True if successful
        """
        try:
            buttons_template = ButtonsTemplate(
                title=title,
                text=text,
                actions=actions
            )
            template_message = TemplateSendMessage(
                alt_text=title,
                template=buttons_template
            )
            self.line_bot_api.push_message(user_id, template_message)
            return True
        except LineBotApiError as e:
            logger.error(f"Failed to send buttons template: {e}")
            return False

    def get_profile(self, user_id: str) -> dict:
        """
        Get LINE user profile

        Args:
            user_id: LINE user ID

        Returns:
            User profile dict with displayName, pictureUrl, statusMessage
        """
        try:
            profile = self.line_bot_api.get_profile(user_id)
            return {
                "display_name": profile.display_name,
                "picture_url": profile.picture_url,
                "status_message": profile.status_message
            }
        except LineBotApiError as e:
            logger.error(f"Failed to get profile: {e}")
            return {}


# Global instance
line_client = LineClient()
```

---

### File: backend/line_handlers.py

**Purpose:** Handle LINE webhook events

```python
"""
LINE Webhook Event Handlers
Processes events from LINE Messaging API
"""

from linebot.models import (
    MessageEvent,
    TextMessage,
    FollowEvent,
    UnfollowEvent
)
from sqlalchemy.orm import Session
import logging

from backend.line_client import line_client
from backend.database import LineUserMapping
from backend.conversation_manager import ConversationManager
from backend.api_client import SenseChatClient

logger = logging.getLogger(__name__)


class LineEventHandler:
    """Handles LINE webhook events"""

    def __init__(self, db: Session):
        self.db = db
        self.api_client = SenseChatClient()
        self.conversation_manager = ConversationManager(db, self.api_client)

    def handle_follow(self, event: FollowEvent):
        """
        Handle when user follows (adds) the bot

        Args:
            event: LINE FollowEvent
        """
        line_user_id = event.source.user_id

        try:
            # Get LINE user profile
            profile = line_client.get_profile(line_user_id)
            display_name = profile.get("display_name", "朋友")

            # Check if user already exists
            existing_mapping = self.db.query(LineUserMapping).filter(
                LineUserMapping.line_user_id == line_user_id
            ).first()

            if existing_mapping:
                # User re-followed (they unfollowed then followed again)
                logger.info(f"User {line_user_id} re-followed bot")
                line_client.push_message(
                    line_user_id,
                    f"歡迎回來 {display_name}！😊 繼續我們的對話吧~"
                )
            else:
                # New user
                logger.info(f"New user followed: {line_user_id}")
                line_client.send_welcome_message(line_user_id, display_name)

        except Exception as e:
            logger.error(f"Error handling follow event: {e}")

    def handle_unfollow(self, event: UnfollowEvent):
        """
        Handle when user unfollows (blocks) the bot

        Args:
            event: LINE UnfollowEvent
        """
        line_user_id = event.source.user_id
        logger.info(f"User unfollowed: {line_user_id}")

        # Optional: Mark user as inactive in database
        # Don't delete data - they might come back

    def handle_message(self, event: MessageEvent):
        """
        Handle text message from user

        Args:
            event: LINE MessageEvent with TextMessage
        """
        line_user_id = event.source.user_id
        reply_token = event.reply_token
        user_message = event.message.text

        logger.info(f"Message from {line_user_id}: {user_message}")

        try:
            # Check if user has a character
            mapping = self.db.query(LineUserMapping).filter(
                LineUserMapping.line_user_id == line_user_id
            ).first()

            if not mapping or not mapping.active_character_id:
                # User hasn't created a character yet
                line_client.reply_message(
                    reply_token,
                    "你還沒有設定角色喔~ 請先點選下方連結完成設定：\n" +
                    f"{settings.APP_BASE_URL}{settings.SETUP_UI_PATH}?lineUserId={line_user_id}"
                )
                return

            # User has a character - process conversation
            result = self.conversation_manager.send_message(
                user_id=mapping.user_id,
                character_id=mapping.active_character_id,
                user_message=user_message
            )

            if result["success"]:
                # Send AI response
                reply_text = result["reply"]

                # Add special event messages if any
                if result.get("special_messages"):
                    for special_msg in result["special_messages"]:
                        reply_text += f"\n\n{special_msg['message']}"

                line_client.reply_message(reply_token, reply_text)

                # Update last interaction time
                mapping.last_interaction = datetime.utcnow()
                self.db.commit()

            else:
                # Error occurred
                logger.error(f"Conversation error: {result.get('error')}")
                line_client.reply_message(
                    reply_token,
                    "抱歉，處理訊息時發生錯誤，請稍後再試 😢"
                )

        except Exception as e:
            logger.error(f"Error handling message: {e}", exc_info=True)
            line_client.reply_message(
                reply_token,
                "系統發生錯誤，請稍後再試 🙏"
            )
```

---

## 🔧 5. Modify Existing Files

### backend/main.py - Add LINE Webhook Endpoint

**Location:** After existing endpoints (around line 200)

```python
from fastapi import FastAPI, Request, HTTPException, BackgroundTasks
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, FollowEvent, UnfollowEvent
import hashlib
import hmac
import base64

from backend.line_client import line_client
from backend.line_handlers import LineEventHandler
from backend.config import settings

# ... existing imports and setup ...

# ========== ADD THIS ENDPOINT ==========

@app.post("/webhook/line")
async def line_webhook(
    request: Request,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    LINE Messaging API webhook endpoint
    Receives events from LINE platform
    """

    # Get request body and signature
    body = await request.body()
    signature = request.headers.get('X-Line-Signature', '')

    # Verify signature
    hash = hmac.new(
        settings.LINE_CHANNEL_SECRET.encode('utf-8'),
        body,
        hashlib.sha256
    ).digest()
    expected_signature = base64.b64encode(hash).decode('utf-8')

    if signature != expected_signature:
        logger.warning("Invalid LINE signature")
        raise HTTPException(status_code=400, detail="Invalid signature")

    # Parse events
    try:
        handler = line_client.handler
        events = handler.parser.parse(body.decode('utf-8'), signature)
    except Exception as e:
        logger.error(f"Failed to parse LINE webhook: {e}")
        raise HTTPException(status_code=400, detail="Invalid request")

    # Process events in background
    for event in events:
        background_tasks.add_task(process_line_event, event, db)

    return {"status": "ok"}


async def process_line_event(event, db: Session):
    """
    Process LINE event in background

    Args:
        event: LINE event object
        db: Database session
    """
    event_handler = LineEventHandler(db)

    if isinstance(event, FollowEvent):
        event_handler.handle_follow(event)
    elif isinstance(event, UnfollowEvent):
        event_handler.handle_unfollow(event)
    elif isinstance(event, MessageEvent) and isinstance(event.message, TextMessage):
        event_handler.handle_message(event)
    else:
        logger.info(f"Unhandled event type: {type(event)}")
```

---

### backend/main.py - Modify Character Creation Endpoint

**Find:** `/api/v2/create-character` endpoint (around line 188)

**Modify to accept LINE user ID and send first message:**

```python
from backend.models import UserProfile
from backend.line_client import line_client
from backend.database import LineUserMapping

@app.post("/api/v2/create-character")
async def create_character_v2(
    user_profile: UserProfile,
    line_user_id: Optional[str] = None,  # ADD THIS PARAMETER
    db: Session = Depends(get_db)
) -> Dict:
    """
    Generate and persist character to database
    If line_user_id is provided, send first message via LINE

    Args:
        user_profile: User profile with preferences
        line_user_id: Optional LINE user ID for LINE integration
        db: Database session

    Returns:
        Character data with initial message
    """
    try:
        # Get or create user
        user = conversation_manager.get_or_create_user(user_profile.user_name)

        # Generate character
        character_settings = character_generator.generate_character(user_profile)

        # Save to database
        character = conversation_manager.save_character(
            user_id=user.user_id,
            character_data=character_settings
        )

        # Generate initial message
        initial_message = character_generator.create_initial_message(
            character_settings["name"],
            user_profile,
            character_settings.get("gender", "女")
        )

        # Save initial message
        conversation_manager.save_message(
            user_id=user.user_id,
            character_id=character.character_id,
            speaker_name=character.name,
            content=initial_message,
            favorability_level=1
        )

        # ========== ADD THIS LINE INTEGRATION ==========
        if line_user_id:
            # Create or update LINE user mapping
            existing_mapping = db.query(LineUserMapping).filter(
                LineUserMapping.line_user_id == line_user_id
            ).first()

            if existing_mapping:
                # Update existing mapping
                existing_mapping.user_id = user.user_id
                existing_mapping.active_character_id = character.character_id
            else:
                # Create new mapping
                mapping = LineUserMapping(
                    line_user_id=line_user_id,
                    user_id=user.user_id,
                    active_character_id=character.character_id
                )
                db.add(mapping)

            db.commit()

            # Send first message via LINE Push API
            line_client.send_character_created_message(
                user_id=line_user_id,
                character_name=character.name,
                initial_message=initial_message
            )
        # ========== END LINE INTEGRATION ==========

        # Get character picture
        character_picture = picture_manager.get_random_picture(
            character_settings.get("gender", "女")
        )

        return {
            "success": True,
            "character_id": character.character_id,
            "user_id": user.user_id,
            "character": {
                "name": character.name,
                "gender": character.gender,
                "identity": character.identity,
                "nickname": character.nickname,
                "detail_setting": character.detail_setting,
                "other_setting": character.other_setting
            },
            "initial_message": initial_message,
            "character_picture": character_picture,
            "favorability_level": 1,
            "message": "角色生成並保存成功！"
        }

    except Exception as e:
        logger.error(f"Failed to create character: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"角色生成失敗: {str(e)}")
```

---

### backend/main.py - Modify Setup UI Endpoint

**Find:** `/ui2` endpoint (around line 1000+)

**Modify to accept LINE user ID as query parameter:**

```python
@app.get("/ui2")
async def ui2(lineUserId: Optional[str] = None):  # ADD PARAMETER
    """
    Phase 2 UI - Complete character creation and chat interface
    If lineUserId is provided, it's from LINE bot setup flow
    """

    # In the JavaScript section, modify the character generation:
    # Find the fetch call to /api/v2/create-character
    # Add lineUserId to the request if present

    # Example modification in the embedded HTML/JavaScript:
    html_content = f"""
    <script>
        const LINE_USER_ID = "{lineUserId or ''}";  // ADD THIS

        // In generateCharacter function, modify the fetch:
        async function generateCharacter() {{
            const formData = new FormData(form);
            const data = Object.fromEntries(formData);

            // ADD lineUserId if present
            if (LINE_USER_ID) {{
                data.line_user_id = LINE_USER_ID;
            }}

            const response = await fetch('/api/v2/create-character', {{
                method: 'POST',
                headers: {{'Content-Type': 'application/json'}},
                body: JSON.stringify(data)
            }});

            if (response.ok) {{
                if (LINE_USER_ID) {{
                    // Show success and redirect to LINE
                    alert('角色設定完成！請回到LINE查看第一則訊息 💕');
                    // Optionally: Close window or show "return to LINE" button
                    document.getElementById('setup-complete').style.display = 'block';
                }} else {{
                    // Normal web flow
                    displayCharacter(data);
                }}
            }}
        }}
    </script>

    <!-- ADD this success div -->
    <div id="setup-complete" style="display:none; text-align:center; padding:40px;">
        <h2>✅ 設定完成！</h2>
        <p>你的專屬AI伴侶已經準備好了~</p>
        <p><strong>請回到LINE開始聊天吧！💕</strong></p>
        <button onclick="window.close()">關閉視窗</button>
    </div>
    """

    return HTMLResponse(content=html_content)
```

---

## 🔒 6. Security & Middleware Changes

### backend/middleware.py - NEW FILE

```python
"""
Middleware for authentication, rate limiting, and security
"""

from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import time

from backend.config import settings

# Rate limiter
limiter = Limiter(key_func=get_remote_address)

def setup_middleware(app):
    """
    Setup all middleware for the FastAPI app

    Args:
        app: FastAPI application instance
    """

    # Rate limiting
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    # Request timing middleware
    @app.middleware("http")
    async def add_process_time_header(request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response

    # Security headers
    @app.middleware("http")
    async def add_security_headers(request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        if settings.ENVIRONMENT == "production":
            response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        return response
```

### backend/main.py - Add Middleware

```python
from backend.middleware import setup_middleware, limiter

# After creating FastAPI app:
app = FastAPI(title="Dating Chatbot API", version="2.0.0")

# ADD THIS:
setup_middleware(app)

# Apply rate limits to endpoints:
@app.post("/api/v2/send-message")
@limiter.limit("10/minute")  # Max 10 messages per minute
async def send_message(
    request: Request,  # ADD THIS for rate limiter
    user_id: int,
    character_id: int,
    message: str,
    db: Session = Depends(get_db)
):
    # ... existing code ...
```

---

## 🚀 7. Production Configuration Files

### Procfile - NEW FILE (for Heroku)

```
web: gunicorn backend.main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
```

### runtime.txt - NEW FILE (for Heroku)

```
python-3.11.6
```

### .gitignore - UPDATE

```
# Add these:
*.db
*.sqlite3
.env
__pycache__/
*.pyc
.DS_Store
venv/
.vscode/
.idea/
*.log
```

---

## 📊 8. Summary of Changes

### New Files (7):
1. `backend/line_client.py` - LINE API wrapper
2. `backend/line_handlers.py` - Event handlers
3. `backend/middleware.py` - Security middleware
4. `migrations/001_add_line_mapping.py` - Database migration
5. `Procfile` - Heroku deployment
6. `runtime.txt` - Python version
7. `.gitignore` updates

### Modified Files (5):
1. `requirements.txt` - Add 11 new dependencies
2. `backend/config.py` - Add LINE & security config
3. `backend/database.py` - Add LineUserMapping table
4. `backend/main.py` - Add webhook endpoint, modify character creation
5. `.env` - Add LINE credentials and config

### Database Changes:
- ✅ Add `LineUserMapping` table
- ✅ Add relationship to `User` table
- ✅ Migration script for PostgreSQL

### Code Statistics:
- **Lines Added:** ~800 lines
- **Lines Modified:** ~100 lines
- **New Dependencies:** 11 packages
- **Estimated Dev Time:** 8-12 hours

---

## ✅ Testing Checklist

After implementing all changes:

- [ ] LINE webhook signature verification works
- [ ] New user follow → Welcome message sent
- [ ] Setup link opens web UI with LINE user ID
- [ ] Character creation → First message sent to LINE
- [ ] User message → AI response in LINE
- [ ] Favorability tracking still works
- [ ] Special events (milestones) still trigger
- [ ] Rate limiting prevents spam
- [ ] Error tracking with Sentry works
- [ ] Database migration successful
- [ ] All existing tests pass
- [ ] New LINE integration tests pass

---

## 🎯 Implementation Priority

### Phase 1: Core LINE Integration (Days 1-3)
1. Add LINE dependencies
2. Create line_client.py
3. Create line_handlers.py
4. Add webhook endpoint
5. Test with ngrok locally

### Phase 2: Database (Days 4-5)
1. Add LineUserMapping table
2. Create migration script
3. Test locally with PostgreSQL
4. Modify character creation endpoint

### Phase 3: Security (Day 6)
1. Add middleware
2. Implement rate limiting
3. Add signature verification
4. Update CORS configuration

### Phase 4: Production (Days 7-8)
1. Add Procfile & runtime.txt
2. Deploy to Heroku
3. Configure environment variables
4. Test end-to-end

**Total Estimated Time: 8-10 days of focused work**
