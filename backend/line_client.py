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
)
from linebot.exceptions import LineBotApiError
import logging

from backend.config import settings

logger = logging.getLogger(__name__)


class LineClient:
    """Client for interacting with LINE Messaging API"""

    def __init__(self):
        """Initialize LINE Bot API and Webhook Handler"""
        self.line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
        self.handler = WebhookHandler(settings.LINE_CHANNEL_SECRET)
        logger.info("LINE client initialized")

    def reply_message(self, reply_token: str, text: str) -> bool:
        """
        Reply to a message using reply token (can only be used once)

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
        Push a message to user (not a reply, can be used anytime)

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
        Send welcome message with setup link when user follows bot

        Args:
            user_id: LINE user ID
            user_name: User's display name from LINE

        Returns:
            True if successful
        """
        setup_url = f"{settings.APP_BASE_URL}{settings.SETUP_UI_PATH}?lineUserId={user_id}"

        message = f"""嗨 {user_name}！歡迎來到{settings.LINE_BOT_NAME} 💕

✨ 最有趣的戀愛聊天機器人，現在就開始體驗！

要開始使用，請先設定你的專屬AI伴侶：
👉 {setup_url}

完成設定後，回到這裡就可以聊出激情囉！🔥"""

        return self.push_message(user_id, message)

    def send_character_created_message(
        self,
        user_id: str,
        character_name: str,
        initial_message: str,
        picture_url: str = None
    ) -> bool:
        """
        Send message when character is created successfully, with character picture

        Args:
            user_id: LINE user ID
            character_name: Created character's name
            initial_message: Character's first greeting message
            picture_url: Full URL to character picture

        Returns:
            True if successful
        """
        try:
            messages = []

            # Add picture if provided
            if picture_url:
                messages.append(ImageSendMessage(
                    original_content_url=picture_url,
                    preview_image_url=picture_url
                ))

            # Add text message
            setup_complete_msg = f"""✅ 角色設定完成！

你的專屬伴侶 {character_name} 已經準備好了~ 💕

{initial_message}

───────────────
💬 每天免費 {settings.FREE_MESSAGES_PER_DAY} 則訊息
🎁 邀請 {settings.REFERRALS_FOR_UNLIMITED} 位好友 → 無限暢聊
💎 或升級至 Premium (${settings.PREMIUM_PRICE_USD}/月)"""

            messages.append(TextSendMessage(text=setup_complete_msg))

            # Send all messages
            self.line_bot_api.push_message(user_id, messages)
            logger.info(f"Sent character created message with picture to {user_id}")
            return True

        except LineBotApiError as e:
            logger.error(f"Failed to send character created message: {e}")
            return False

    def send_no_character_warning(self, user_id: str) -> bool:
        """
        Send warning when user hasn't created a character yet

        Args:
            user_id: LINE user ID

        Returns:
            True if successful
        """
        setup_url = f"{settings.APP_BASE_URL}{settings.SETUP_UI_PATH}?lineUserId={user_id}"

        message = f"""你還沒有設定AI伴侶喔~ 💔

請先點選下方連結完成設定：
👉 {setup_url}

設定完成後，我們就可以開始聊天了！"""

        return self.push_message(user_id, message)

    def send_daily_limit_reached(self, user_id: str, referral_link: str = "") -> bool:
        """
        Send message when daily message limit is reached

        Args:
            user_id: LINE user ID
            referral_link: Referral link for inviting friends

        Returns:
            True if successful
        """
        if not referral_link:
            referral_link = f"{settings.APP_BASE_URL}/referral?lineUserId={user_id}"

        message = f"""今天的 {settings.FREE_MESSAGES_PER_DAY} 則免費訊息已用完囉~ 😢

想要繼續聊天？你可以：

🎁 邀請 {settings.REFERRALS_FOR_UNLIMITED} 位好友使用 → 無限暢聊
   推薦連結：{referral_link}

💎 升級 Premium (${settings.PREMIUM_PRICE_USD}/月) → 無限訊息
   (即將推出！)

明天再來找我聊天吧！💕"""

        return self.push_message(user_id, message)

    def send_character_limit_error(self, user_id: str) -> bool:
        """
        Send error when user tries to create a second character

        Args:
            user_id: LINE user ID

        Returns:
            True if successful
        """
        message = """你已經有專屬伴侶了！💕

每位用戶只能擁有一個AI角色。
如果想要重新開始，請聯繫客服。"""

        return self.push_message(user_id, message)

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
            logger.info(f"Sent buttons template to {user_id}: {title}")
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
            Empty dict if failed
        """
        try:
            profile = self.line_bot_api.get_profile(user_id)
            return {
                "display_name": profile.display_name,
                "picture_url": profile.picture_url,
                "status_message": profile.status_message or ""
            }
        except LineBotApiError as e:
            logger.error(f"Failed to get profile: {e}")
            return {}


# Global instance
line_client = LineClient()
