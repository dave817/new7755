"""
Database setup and models for the dating chatbot
Phase 2: Conversation persistence and history management
"""
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Date, ForeignKey, Text, JSON, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime, date
from backend.config import settings

# Create database engine
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Database Models

class User(Base):
    """User model"""
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_active = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    characters = relationship("Character", back_populates="user", cascade="all, delete-orphan")
    preferences = relationship("UserPreference", back_populates="user", cascade="all, delete-orphan")
    messages = relationship("Message", back_populates="user", cascade="all, delete-orphan")
    line_mappings = relationship("LineUserMapping", back_populates="user", cascade="all, delete-orphan")


class Character(Base):
    """AI Character model"""
    __tablename__ = "characters"

    character_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    name = Column(String(50), nullable=False)
    gender = Column(String(50), nullable=False)
    identity = Column(String(200))
    nickname = Column(String(50))
    detail_setting = Column(Text)  # Up to 500 chars
    other_setting = Column(JSON)  # JSON stored as text
    knowledge_base_id = Column(String(100))  # SenseChat knowledge base ID
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="characters")
    messages = relationship("Message", back_populates="character", cascade="all, delete-orphan")
    favorability = relationship(
        "FavorabilityTracking",
        back_populates="character",
        uselist=False,
        cascade="all, delete-orphan"
    )


class Message(Base):
    """Conversation message model"""
    __tablename__ = "messages"

    message_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    character_id = Column(Integer, ForeignKey("characters.character_id"), nullable=False)
    speaker_name = Column(String(50), nullable=False)  # Who said this message
    message_content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    favorability_level = Column(Integer, default=1)  # 1, 2, or 3

    # Relationships
    user = relationship("User", back_populates="messages")
    character = relationship("Character", back_populates="messages")


class UserPreference(Base):
    """User custom memory/preferences model"""
    __tablename__ = "user_preferences"

    preference_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    category = Column(String(50), nullable=False)  # likes, dislikes, habits, background
    content = Column(JSON, nullable=False)  # JSON content
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="preferences")


class FavorabilityTracking(Base):
    """Favorability level tracking model"""
    __tablename__ = "favorability_tracking"

    tracking_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    character_id = Column(Integer, ForeignKey("characters.character_id"), nullable=False, unique=True)
    current_level = Column(Integer, default=1)  # 1, 2, or 3
    message_count = Column(Integer, default=0)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    character = relationship("Character", back_populates="favorability")


class LineUserMapping(Base):
    """Maps LINE User IDs to internal user IDs for LINE integration"""
    __tablename__ = "line_user_mappings"

    mapping_id = Column(Integer, primary_key=True, index=True)
    line_user_id = Column(String(100), unique=True, nullable=False, index=True)  # LINE's user ID (Uxxxxx)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    line_display_name = Column(String(100))  # User's display name from LINE
    character_id = Column(Integer, ForeignKey("characters.character_id", ondelete="SET NULL"))  # Active character

    # Message limits & premium features
    daily_message_count = Column(Integer, default=0)  # Reset daily
    last_message_date = Column(Date, default=date.today)  # Track daily reset
    is_premium = Column(Boolean, default=False)  # Premium subscription status
    premium_expires_at = Column(DateTime, nullable=True)  # Premium expiry date

    # Referral system
    referral_count = Column(Integer, default=0)  # Number of friends referred
    referred_by = Column(String(100), nullable=True)  # LINE user ID who referred this user

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    last_interaction = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="line_mappings")
    character = relationship("Character", foreign_keys=[character_id])

    def __repr__(self):
        return f"<LineUserMapping(line_user_id='{self.line_user_id}', user_id={self.user_id})>"

    def is_unlimited(self):
        """Check if user has unlimited messages (premium or referrals)"""
        from backend.config import settings
        return self.is_premium or self.referral_count >= settings.REFERRALS_FOR_UNLIMITED

    def can_send_message(self):
        """Check if user can send a message today"""
        from backend.config import settings

        # Check if it's a new day - reset counter
        today = date.today()
        if self.last_message_date != today:
            self.daily_message_count = 0
            self.last_message_date = today

        # Unlimited users can always send
        if self.is_unlimited():
            return True

        # Free tier users check daily limit
        return self.daily_message_count < settings.FREE_MESSAGES_PER_DAY


# Create all tables
def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")


if __name__ == "__main__":
    init_db()
