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
from datetime import datetime
import logging

from backend.line_client import line_client
from backend.database import LineUserMapping
from backend.conversation_manager import ConversationManager
from backend.api_client import SenseChatClient
from backend.config import settings
from backend.text_cleaner import clean_for_line

logger = logging.getLogger(__name__)


class LineEventHandler:
    """Handles LINE webhook events"""

    def __init__(self, db: Session):
        """
        Initialize event handler

        Args:
            db: Database session
        """
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

            logger.info(f"User {line_user_id} ({display_name}) followed bot")

            # Check if user already exists (they might have unfollowed and re-followed)
            existing_mapping = self.db.query(LineUserMapping).filter(
                LineUserMapping.line_user_id == line_user_id
            ).first()

            if existing_mapping:
                # User re-followed (they unfollowed then followed again)
                logger.info(f"User {line_user_id} re-followed bot")
                line_client.push_message(
                    line_user_id,
                    f"歡迎回來 {display_name}！😊\n\n我們的專屬對話依然在這裡等你~ 繼續聊天吧！💕"
                )
            else:
                # New user - send welcome message with setup link
                logger.info(f"New user {line_user_id} - sending welcome message")
                line_client.send_welcome_message(line_user_id, display_name)

        except Exception as e:
            logger.error(f"Error handling follow event: {e}", exc_info=True)
            # Send generic welcome even if there's an error
            line_client.send_welcome_message(line_user_id, "朋友")

    def handle_unfollow(self, event: UnfollowEvent):
        """
        Handle when user unfollows (blocks) the bot

        Args:
            event: LINE UnfollowEvent
        """
        line_user_id = event.source.user_id
        logger.info(f"User {line_user_id} unfollowed bot")

        # Note: We don't delete user data when they unfollow
        # They might come back, and we want to preserve their character/history
        # Data cleanup can be done separately for inactive users

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
            # Get or create LINE user mapping
            mapping = self.db.query(LineUserMapping).filter(
                LineUserMapping.line_user_id == line_user_id
            ).first()

            if not mapping:
                # User hasn't started setup process yet
                logger.info(f"User {line_user_id} has no mapping - sending setup link")
                line_client.send_no_character_warning(line_user_id)
                return

            if not mapping.character_id:
                # User mapping exists but no character created yet
                logger.info(f"User {line_user_id} has no character - sending setup link")
                line_client.send_no_character_warning(line_user_id)
                return

            # Check if user can send message (daily limit)
            if not mapping.can_send_message():
                logger.info(f"User {line_user_id} reached daily limit")
                line_client.send_daily_limit_reached(line_user_id)
                return

            # User has character and can send - process conversation
            logger.info(f"Processing conversation for user {line_user_id}, character {mapping.character_id}")

            result = self.conversation_manager.send_message(
                user_id=mapping.user_id,
                character_id=mapping.character_id,
                user_message=user_message
            )

            if result["success"]:
                # Get AI response
                reply_text = result["reply"]

                # Add special event messages if any
                if result.get("special_messages"):
                    for special_msg in result["special_messages"]:
                        reply_text += f"\n\n{special_msg['message']}"

                # Clean response text (remove action tags and system artifacts)
                reply_text = clean_for_line(reply_text)

                # Send response via LINE
                line_client.reply_message(reply_token, reply_text)

                # Update message count for daily limit tracking
                mapping.daily_message_count += 1
                mapping.last_interaction = datetime.utcnow()
                self.db.commit()

                logger.info(f"Sent response to {line_user_id}. Daily count: {mapping.daily_message_count}")

            else:
                # Error occurred in conversation
                error = result.get('error', 'Unknown error')
                logger.error(f"Conversation error for {line_user_id}: {error}")

                line_client.reply_message(
                    reply_token,
                    "抱歉，處理訊息時發生錯誤，請稍後再試 😢\n\n如果問題持續，請聯繫客服。"
                )

        except Exception as e:
            logger.error(f"Error handling message from {line_user_id}: {e}", exc_info=True)

            # Try to send error message to user
            try:
                line_client.reply_message(
                    reply_token,
                    "系統發生錯誤，請稍後再試 🙏\n\n我們正在努力修復中！"
                )
            except Exception as reply_error:
                logger.error(f"Failed to send error message: {reply_error}")


def create_event_handler(db: Session) -> LineEventHandler:
    """
    Factory function to create event handler with database session

    Args:
        db: Database session

    Returns:
        LineEventHandler instance
    """
    return LineEventHandler(db)
