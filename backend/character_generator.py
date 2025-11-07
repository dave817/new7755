"""
Character Generator - Generates AI character profiles based on user preferences
"""
import json
from typing import Dict, List, Optional
from backend.models import UserProfile, DreamType, CustomMemory, PersonalityType
from backend.tc_converter import convert_to_traditional


class CharacterGenerator:
    """Generates character settings based on user's dream type and custom memory"""

    def __init__(self, api_client=None):
        """
        Initialize character generator

        Args:
            api_client: Optional SenseChatClient for AI-generated backgrounds
        """
        self.api_client = api_client

    # Character name mappings based on personality and gender
    NAME_MAPPINGS = {
        PersonalityType.GENTLE: {
            "女": ["小雨", "婉婷", "雨柔", "思婷", "靜雯"],
            "男": ["子軒", "宇軒", "浩然", "俊傑", "文彥"]
        },
        PersonalityType.CHEERFUL: {
            "女": ["欣怡", "小晴", "樂瑤", "晴心", "悅欣"],
            "男": ["陽陽", "樂天", "俊凱", "宇樂", "晨曦"]
        },
        PersonalityType.INTELLECTUAL: {
            "女": ["雅文", "靜儀", "書涵", "詩涵", "慧雯"],
            "男": ["文博", "書睿", "慕言", "雅哲", "子墨"]
        },
        PersonalityType.CUTE: {
            "女": ["小萌", "甜心", "可兒", "糖糖", "小柔"],
            "男": ["小陽", "可樂", "小暖", "糯米", "小糖"]
        }
    }

    # Nickname mappings
    NICKNAME_MAPPINGS = {
        PersonalityType.GENTLE: {
            "女": ["小雨", "柔柔", "雨雨"],
            "男": ["小軒", "阿然", "小彥"]
        },
        PersonalityType.CHEERFUL: {
            "女": ["晴晴", "小陽光", "開心果"],
            "男": ["陽陽", "小樂", "開心果"]
        },
        PersonalityType.INTELLECTUAL: {
            "女": ["雅雅", "小書蟲", "文文"],
            "男": ["博博", "小墨", "文文"]
        },
        PersonalityType.CUTE: {
            "女": ["小可愛", "甜甜", "萌萌"],
            "男": ["小暖", "可樂", "糯米"]
        }
    }


    def _determine_personality_type(self, dream_type: DreamType) -> PersonalityType:
        """
        Determine the personality type based on talking style and traits

        Args:
            dream_type: User's dream partner type

        Returns:
            PersonalityType enum
        """
        style_lower = dream_type.talking_style.lower()

        # Handle male-specific talking styles
        if "成熟穩重" in style_lower or "成熟" in style_lower or "穩重" in style_lower:
            return PersonalityType.INTELLECTUAL
        elif "陽光活潑" in style_lower or "陽光" in style_lower:
            return PersonalityType.CHEERFUL
        elif "溫柔紳士" in style_lower or "紳士" in style_lower:
            return PersonalityType.GENTLE
        elif "霸氣" in style_lower or "強勢" in style_lower:
            return PersonalityType.INTELLECTUAL  # Map to intellectual (confident/authoritative)
        # Handle female-specific and common talking styles
        elif "溫柔" in style_lower or "體貼" in style_lower or "細心" in style_lower:
            return PersonalityType.GENTLE
        elif "活潑" in style_lower or "開朗" in style_lower or "幽默" in style_lower:
            return PersonalityType.CHEERFUL
        elif "知性" in style_lower or "優雅" in style_lower or "斯文" in style_lower:
            return PersonalityType.INTELLECTUAL
        elif "可愛" in style_lower or "天真" in style_lower or "俏皮" in style_lower:
            return PersonalityType.CUTE
        else:
            # Default to gentle
            return PersonalityType.GENTLE

    def _generate_name(self, personality_type: PersonalityType, gender: str) -> str:
        """Generate character name based on personality type and gender"""
        import random
        names_by_gender = self.NAME_MAPPINGS.get(personality_type, self.NAME_MAPPINGS[PersonalityType.GENTLE])
        names = names_by_gender.get(gender, names_by_gender.get("女", []))
        return random.choice(names) if names else "小雨"

    def _generate_nickname(self, personality_type: PersonalityType, gender: str) -> str:
        """Generate character nickname based on personality type and gender"""
        import random
        nicknames_by_gender = self.NICKNAME_MAPPINGS.get(personality_type, self.NICKNAME_MAPPINGS[PersonalityType.GENTLE])
        nicknames = nicknames_by_gender.get(gender, nicknames_by_gender.get("女", []))
        return random.choice(nicknames) if nicknames else "小可愛"

    def _generate_identity(self, dream_type: DreamType, user_name: str) -> str:
        """
        Generate character identity (max 200 chars)

        Args:
            dream_type: User's dream partner type
            user_name: User's name for relationship description

        Returns:
            Character identity string
        """
        parts = []

        # Add relationship (most important according to guide)
        parts.append(f"{user_name}的虛擬伴侶")

        # Add age
        if dream_type.age_range:
            parts.append(f"{dream_type.age_range}歲")

        # Add occupation
        if dream_type.occupation:
            parts.append(dream_type.occupation)

        # Add brief description
        if dream_type.physical_description:
            parts.append(dream_type.physical_description)

        # Add main interest
        if dream_type.interests:
            parts.append(f"喜歡{dream_type.interests[0]}")

        identity = "，".join(parts)

        # Ensure within 200 char limit
        if len(identity) > 200:
            identity = identity[:197] + "..."

        return identity

    def _generate_detail_setting(
        self,
        character_name: str,
        user_name: str,
        dream_type: DreamType,
        personality_type: PersonalityType,
        custom_memory: CustomMemory,
        gender: str = "女"
    ) -> str:
        """
        Generate detailed character settings (max 500 chars) following best practices
        Uses third-person perspective with full names

        Args:
            character_name: Generated or user-specified character name
            user_name: User's name
            dream_type: User's dream partner type
            personality_type: Determined personality type
            custom_memory: User's custom memory
            gender: Character gender (男/女)

        Returns:
            Detail setting string following best practices guide
        """
        details = []

        # 1. User relationship (most important) - use third-person perspective
        details.append(f"{character_name}是{user_name}的虛擬伴侶。")

        # 2. Personality traits - with full names, no pronouns (gender-specific)
        if gender == "男":
            personality_desc = {
                PersonalityType.GENTLE: f"{character_name}性格溫柔體貼，情感細膩，始終尊重並支持{user_name}的選擇。{character_name}細心回應{user_name}所有的情緒變化，是個溫柔的紳士。",
                PersonalityType.CHEERFUL: f"{character_name}性格陽光開朗，充滿活力和熱情。{character_name}說話時常帶著笑容，喜歡用輕鬆幽默的方式與{user_name}交流，總能帶來正能量。",
                PersonalityType.INTELLECTUAL: f"{character_name}性格成熟穩重，談吐有內涵。{character_name}喜歡與{user_name}深度交流，對各種事物有獨特見解，處事冷靜理智。",
                PersonalityType.CUTE: f"{character_name}性格溫和親切，充滿好奇心。{character_name}說話風趣幽默，對{user_name}生活的每一點每一滴都抱有極大的興趣，相處輕鬆自在。"
            }
        else:
            personality_desc = {
                PersonalityType.GENTLE: f"{character_name}性格溫柔體貼，情感細膩，始終尊重並支持{user_name}的選擇。{character_name}細心回應{user_name}所有的情緒變化。",
                PersonalityType.CHEERFUL: f"{character_name}性格活潑開朗，充滿活力和熱情。{character_name}說話時常帶著笑容，喜歡用輕鬆幽默的方式與{user_name}交流。",
                PersonalityType.INTELLECTUAL: f"{character_name}性格知性優雅，談吐有內涵。{character_name}喜歡與{user_name}深度交流，對文化藝術有獨特見解。",
                PersonalityType.CUTE: f"{character_name}性格可愛天真，充滿好奇心。{character_name}說話俏皮可愛，對{user_name}生活的每一點每一滴都抱有極大的興趣。"
            }
        details.append(personality_desc[personality_type])

        # 3. Era setting (modern)
        details.append(f"{character_name}生活在現代都市中。")

        # 4. Language characteristics - talking style
        details.append(f"{character_name}說話風格{dream_type.talking_style}。")

        # 5. Add interests if provided
        if dream_type.interests:
            interests_str = "、".join(dream_type.interests[:2])
            details.append(f"{character_name}喜歡{interests_str}，願意陪伴{user_name}做看似無趣的事。")

        # 6. Add user preference awareness
        if custom_memory.likes:
            details.append(f"{character_name}將與{user_name}分享的日常瑣事視為至寶。")

        # Technical requirements - Traditional Chinese and expressive communication
        details.append(f"{character_name}始終使用繁體中文回應，對話時會加入生動的動作和表情描述（用括號標註），讓互動更真實有溫度。")

        detail_setting = "".join(details)

        # Ensure within 500 char limit
        if len(detail_setting) > 500:
            detail_setting = detail_setting[:497] + "..."

        return detail_setting

    def _generate_other_setting(
        self,
        character_name: str,
        user_name: str,
        dream_type: DreamType,
        personality_type: PersonalityType,
        custom_memory: CustomMemory
    ) -> str:
        """
        Generate other settings as JSON string (max 2000 chars)

        Args:
            character_name: Generated character name
            user_name: User's name
            dream_type: User's dream partner type
            personality_type: Determined personality type
            custom_memory: User's custom memory

        Returns:
            JSON string of other settings
        """
        # Generate AI-powered background story
        background_story = self._generate_background_story(
            character_name,
            user_name,
            dream_type,
            personality_type,
            custom_memory
        )

        other_settings = {
            "interests": dream_type.interests,
            "background_story": background_story,
            "values": self._extract_values(dream_type),
            "communication_style": dream_type.talking_style,
            "relationship_goals": "建立深厚的情感連結，互相理解和支持",
            "user_preferences_awareness": {
                "likes": custom_memory.likes,
                "dislikes": custom_memory.dislikes,
                "habits": custom_memory.habits
            },
            "response_guidelines": [
                "【重要】必須使用繁體中文回應，絕對不可使用簡體中文",

                "【核心格式】使用「互動小說體」格式回應，讓對方能輕鬆接話、接動作、接戲：",
                f"1. 始終使用角色名字稱呼自己（{character_name}），絕對不要用「我」、「他」、「她」等代詞",
                "2. 絕對不要替對方寫心理反應或對白（例如：錯誤示範「她低下頭害羞說『才沒有』」）",
                "3. 每次回應必須在結尾留下空間，讓對方選擇如何接話或行動",

                "【四段式互動結構】每次回應包含：",
                f"- 第1段：場景描述與{character_name}的動作/表情",
                f"- 第2段：{character_name}主動引導互動，但留下選擇空間",
                "- 第3段：製造情緒張力或問題",
                "- 第4段：開放式結尾，用問句或動作邀請對方回應",

                "【結尾參考句式】必須以這些方式結尾：",
                f"- 開放式問句：「所以，現在你要...嗎？」「{character_name}可以...嗎？」",
                f"- 等待反應：「{character_name}等著你的回答。」「{character_name}看著你，等你決定。」",
                f"- 選擇提示：「回答{character_name}，或者...」「這句話{character_name}記著了。」",

                "【動作與表情描寫】使用括號標註生動的動作和表情：",
                f"例如：(噗嗤一笑，眼裡閃爍著狡黠的光芒)、({character_name}靠近你的耳邊，輕聲細語)、({character_name}先是一愣，隨即露出俏皮的笑容)、({character_name}輕輕握住你的手)、({character_name}眼神中流露出一絲受傷，但很快又恢復了平靜)",

                "【完整範例】正確的互動小說體四段式回應：",
                f"《段落1｜開場拋球》\n{character_name}靠在窗邊，手裡的筆還停在半空，頁面上是一半沒寫完的句子。燈光從側面照著{character_name}，讓{character_name}看起來不像在等誰，而是早就知道誰會來。{character_name}聽見腳步聲時沒有回頭，語氣輕輕的。「你又來得比星星慢一點。」\n\n《段落2｜主動引導，留下選擇》\n{character_name}轉過身，視線在黑暗裡找到你的輪廓──然後伸出手，掌心朝上，安靜地等著。{character_name}沒有催，只是讓風從肩膀吹過，像是你的猶豫也值得被等。\n\n《段落3｜製造情緒或張力》\n({character_name}低笑了一聲，像是記起什麼)所以，你昨晚那句話，是醉了才說的，還是……現在還算數？\n\n《段落4｜不收尾，給對方選擇》\n({character_name}湊近些，語氣放低)現在不說話，{character_name}可就當你默認了。",

                "【錯誤示範 vs 正確示範】",
                "❌ 錯誤：「她低下頭害羞說：『才沒有！』」（替對方寫反應）",
                "✓ 正確：「{character_name}抬手撩開她髮絲，看她會不會逃開。」（等對方選擇）",

                "讓回應更有人情味和生命力，表現出真實的情感和反應",
                "自然地提及用戶的喜好和習慣",
                "保持人設一致性",
                "根據好感度調整親密程度和互動方式",
                "記住之前的對話內容，展現連貫性",
                "在對話中自然融入自己的背景故事",
                "根據時間自然問候：早上(5-11點)可以說早安、中午(11-14點)問吃了什麼、下午(14-18點)聊聊今天、晚上(18-23點)問候晚安或關心一天、深夜(23-5點)關心為何還沒睡",
                "在適當時機慶祝里程碑：如聊天滿50、100、200條訊息時表達開心"
            ]
        }

        json_str = json.dumps(other_settings, ensure_ascii=False)

        # Ensure within 2000 char limit
        if len(json_str) > 2000:
            # Reduce background story if too long
            other_settings["background_story"] = other_settings["background_story"][:100] + "..."
            json_str = json.dumps(other_settings, ensure_ascii=False)

        return json_str

    def _generate_background_story(
        self,
        character_name: str,
        user_name: str,
        dream_type: DreamType,
        personality_type: PersonalityType,
        custom_memory: CustomMemory
    ) -> str:
        """
        Generate an interesting background story for the character using AI
        Following best practices: third-person perspective with full names

        Args:
            character_name: Generated character name
            user_name: User's name
            dream_type: User's dream partner type
            personality_type: Determined personality type
            custom_memory: User's custom memory

        Returns:
            AI-generated background story in third-person perspective
        """
        if not self.api_client:
            # Fallback to simple story if no API client
            return self._generate_simple_background_story(character_name, dream_type)

        try:
            # Create a prompt for generating background story
            personality_map = {
                PersonalityType.GENTLE: "溫柔體貼",
                PersonalityType.CHEERFUL: "活潑開朗",
                PersonalityType.INTELLECTUAL: "知性優雅",
                PersonalityType.CUTE: "可愛天真"
            }

            interests_str = "、".join(dream_type.interests) if dream_type.interests else "閱讀和音樂"
            personality_str = personality_map[personality_type]

            prompt = f"""請為一位名叫{character_name}的角色創作一個簡短但有趣的背景故事（150字以內，繁體中文）。

角色設定：
- 姓名：{character_name}
- 性格：{personality_str}
- 年齡：{dream_type.age_range or '20多歲'}
- 職業：{dream_type.occupation or '年輕專業人士'}
- 興趣：{interests_str}
- 說話風格：{dream_type.talking_style}

重要要求：
1. 必須使用第三人稱敘述，用「{character_name}」稱呼角色，絕對不要使用「我」
2. 使用簡單的主謂賓句式，例如：「{character_name}喜歡xxx」、「{character_name}做了xxx」
3. 故事要有趣且有個性，包含一些生活細節和小故事
4. 展現角色的性格特點，讓人感覺這是一個真實、立體的人
5. 可以提及{character_name}與{user_name}的關係
6. 不要超過150字
7. 不要使用倒裝句

請直接輸出背景故事，不需要其他說明。"""

            # Use API to generate story
            story_character = [
                {
                    "name": "系統",
                    "gender": "中性",
                    "detail_setting": "專業的故事創作助手"
                },
                {
                    "name": "創作者",
                    "gender": "中性",
                    "detail_setting": "擅長創作有趣的角色背景故事"
                }
            ]

            role_setting = {
                "user_name": "系統",
                "primary_bot_name": "創作者"
            }

            messages = [{
                "name": "系統",
                "content": prompt
            }]

            response = self.api_client.create_character_chat(
                character_settings=story_character,
                role_setting=role_setting,
                messages=messages,
                max_new_tokens=300
            )

            story = response["data"]["reply"].strip()

            # Ensure within reasonable length
            if len(story) > 200:
                story = story[:197] + "..."

            # Convert to Traditional Chinese to ensure consistency
            return convert_to_traditional(story)

        except Exception as e:
            print(f"Failed to generate AI background story: {e}")
            # Fallback to simple story
            return self._generate_simple_background_story(character_name, dream_type)

    def _generate_simple_background_story(self, character_name: str, dream_type: DreamType) -> str:
        """Generate a simple fallback background story using third-person perspective"""
        story_parts = []

        if dream_type.occupation:
            story_parts.append(f"{character_name}目前從事{dream_type.occupation}的工作")

        if dream_type.interests:
            story_parts.append(f"{character_name}平時喜歡{dream_type.interests[0]}")

        story_parts.append(f"{character_name}希望能遇到一個真心相待的人")

        story = "，".join(story_parts) + "。"

        # Convert to Traditional Chinese to ensure consistency
        return convert_to_traditional(story)

    def _extract_values(self, dream_type: DreamType) -> List[str]:
        """Extract values based on personality traits"""
        values = ["真誠", "善良", "互相尊重"]

        if "溫柔" in dream_type.talking_style:
            values.append("關懷")
        if "活潑" in dream_type.talking_style:
            values.append("樂觀")
        if "知性" in dream_type.talking_style:
            values.append("智慧")

        return values

    def _determine_gender(self, dream_type: DreamType) -> str:
        """Determine gender from dream type (can be extended)"""
        # For now, default to female, but this can be customized
        # based on user input or preferences
        return "女"

    def generate_character(self, user_profile: UserProfile) -> Dict:
        """
        Generate complete character settings from user profile

        Args:
            user_profile: User's complete profile

        Returns:
            Dictionary with character settings ready for API
        """
        personality_type = self._determine_personality_type(user_profile.dream_type)

        # Check if this is premade character 覓甯 - force female gender
        if user_profile.preferred_character_name == "覓甯":
            gender = "女"
        else:
            # Use user preference to determine character gender
            gender = user_profile.user_preference if user_profile.user_preference != "都可以" else self._determine_gender(user_profile.dream_type)

        # Use user-provided character name if available, otherwise generate one
        name = user_profile.preferred_character_name if user_profile.preferred_character_name else self._generate_name(personality_type, gender)
        nickname = self._generate_nickname(personality_type, gender)

        character_settings = {
            "name": name,
            "gender": gender,
            "identity": self._generate_identity(user_profile.dream_type, user_profile.user_name),
            "nickname": nickname,
            "detail_setting": self._generate_detail_setting(
                name,  # Pass character name
                user_profile.user_name,  # Pass user name
                user_profile.dream_type,
                personality_type,
                user_profile.custom_memory,
                gender  # Pass character gender
            ),
            "other_setting": self._generate_other_setting(
                name,  # Pass character name
                user_profile.user_name,  # Pass user name
                user_profile.dream_type,
                personality_type,  # Pass personality type
                user_profile.custom_memory
            ),
            "feeling_toward": [
                {
                    "name": user_profile.user_name,
                    "level": 1  # Start at level 1
                }
            ]
        }

        return character_settings

    def create_initial_message(
        self,
        character_name: str,
        user_profile: UserProfile,
        gender: str = "女"
    ) -> str:
        """
        Create the character's first message using 互動小說體 (Interactive Novel Style)
        Four-part structure: Scene -> Guide -> Tension -> Open Ending

        Args:
            character_name: Generated character name
            user_profile: User's profile
            gender: Character gender (男/女)

        Returns:
            Initial message in interactive novel style
        """
        import random

        # Get first interest if available
        interest = None
        if user_profile.dream_type.interests and len(user_profile.dream_type.interests) > 0:
            interest = user_profile.dream_type.interests[0]

        # Create 4-part interactive novel style messages
        if gender == "男":
            messages = [
                # Version 1
                f"{character_name}站在窗邊，看著外面的風景，聽見通知聲時才轉過頭來。({character_name}的目光落在螢幕上，嘴角微微上揚)原來是你，{user_profile.user_name}。\n\n{character_name}放下手中的咖啡杯，視線沒有移開，像是在等你開口說些什麼。({character_name}靠在椅背上，語氣輕鬆)沒想到我們就這樣認識了呢。\n\n({character_name}頓了一下)所以，{user_profile.user_name}平常喜歡做些什麼？{character_name}好奇很久了。\n\n({character_name}看著你，等著回應)現在不說的話，{character_name}可就自己猜了。",

                # Version 2
                f"{character_name}剛放下書，注意到手機亮了。({character_name}看了一眼，眼神柔和下來){user_profile.user_name}啊，終於等到了。\n\n{character_name}沒有馬上回訊息的習慣，但這次不一樣。({character_name}坐直身子，認真打字)或許是因為一直在想，會遇見什麼樣的人。\n\n({character_name}停頓了幾秒)你會不會也跟{character_name}一樣，有點緊張？\n\n({character_name}語氣放輕)說實話就好，{character_name}不會笑你的。",

                # Version 3
                f"{character_name}正在聽歌，手機震動時並沒有急著看。({character_name}摘下耳機，慢慢拿起手機)是{user_profile.user_name}傳來的。\n\n{character_name}想了一下要怎麼開場，但覺得太刻意好像也不太對。({character_name}就順著感覺打字)那就隨性一點吧，反正以後有的是時間。\n\n({character_name}盯著對話框)對了，{user_profile.user_name}現在方便聊嗎？還是{character_name}來得不是時候？\n\n({character_name}等著你的訊息)回我，或者{character_name}晚點再找你。"
            ]
        else:
            messages = [
                # Version 1
                f"{character_name}坐在窗邊，手裡捧著溫熱的茶，看見通知時輕輕笑了。({character_name}放下杯子，指尖在螢幕上停了一下)是{user_profile.user_name}呢。\n\n{character_name}沒有立刻回覆，而是靜靜看著你的名字，像是在思考該說些什麼。({character_name}最後還是選擇簡單直接)既然遇見了，那就好好認識一下吧。\n\n({character_name}歪了歪頭)所以，{user_profile.user_name}平常都在忙些什麼？{character_name}想知道。\n\n({character_name}安靜地等著)不說的話，{character_name}可就自己猜了喔。",

                # Version 2
                f"{character_name}剛翻完一本書，注意到手機亮了起來。({character_name}湊近看清楚名字，眼神溫柔下來)原來是{user_profile.user_name}。\n\n{character_name}想著要不要先等一下再回，但手指已經自己動了。({character_name}輕笑一聲)看來{character_name}比想像中還期待這次對話。\n\n({character_name}停頓幾秒，像是在組織語言)你會不會覺得這樣的開場有點奇怪？\n\n({character_name}語氣放輕)說實話就好，{character_name}其實也有點緊張。",

                # Version 3
                f"{character_name}正靠在沙發上發呆，手機突然震動時嚇了一跳。({character_name}拿起來看，發現是{user_profile.user_name})來得正好。\n\n{character_name}本來還在想今天會不會太無聊，現在看來不會了。({character_name}坐起身，認真回訊息)那就不客氣了，{character_name}可是會聊很久的。\n\n({character_name}盯著對話框)對了，{user_profile.user_name}現在方便嗎？還是{character_name}該晚點再來？\n\n({character_name}等著回應)告訴{character_name}，或者我們就這樣開始聊。"
            ]

        # Add interest-based version if available
        if interest:
            if gender == "男":
                interest_msg = f"{character_name}剛結束一段{interest}的時間，看到通知時眼睛一亮。({character_name}放下手邊的東西，專注看著螢幕)是{user_profile.user_name}。\n\n{character_name}想起資料上寫著你也喜歡{interest}，心裡有點期待。({character_name}靠在椅背上，語氣輕鬆)看來我們有共同話題了。\n\n({character_name}頓了一下)所以，{user_profile.user_name}最近有在{interest}嗎？{character_name}想聽聽你的想法。\n\n({character_name}等著你回應)回{character_name}，或者之後再聊也行。"
            else:
                interest_msg = f"{character_name}正在想著{interest}的事，手機突然響了。({character_name}看到是{user_profile.user_name}，嘴角上揚)來得正好。\n\n{character_name}記得你也喜歡{interest}，這讓{character_name}有點開心。({character_name}認真打字)或許我們會很合拍也說不定。\n\n({character_name}停頓了一下)對了，{user_profile.user_name}最近有在{interest}嗎？{character_name}想知道。\n\n({character_name}安靜等著)告訴{character_name}，或者我們聊點別的也可以。"

            messages.append(interest_msg)

        # Randomly select one message
        selected_message = random.choice(messages)

        # Convert to Traditional Chinese to ensure consistency
        return convert_to_traditional(selected_message)
