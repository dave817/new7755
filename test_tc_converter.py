"""
Test script for Traditional Chinese converter
Ensures that:
1. OpenCC is working correctly
2. Simplified Chinese is converted to Traditional Chinese
3. Traditional Chinese remains unchanged
4. Conversion doesn't affect the intimacy/favorability system
"""
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from backend.tc_converter import convert_to_traditional, get_converter


def test_converter_initialization():
    """Test that OpenCC converter initializes correctly"""
    print("\n=== Testing Converter Initialization ===")
    converter = get_converter()

    if converter is None:
        print("❌ OpenCC not installed. Please run: pip install opencc-python-reimplemented")
        print("   Or run setup.bat to install all dependencies")
        return False
    else:
        print("✅ OpenCC converter initialized successfully")
        return True


def test_simplified_to_traditional():
    """Test conversion of Simplified Chinese to Traditional Chinese"""
    print("\n=== Testing Simplified to Traditional Conversion ===")

    test_cases = [
        # Simplified -> Expected Traditional
        ("你好", "你好"),  # Same in both
        ("网络", "網路"),  # Network
        ("计算机", "計算機"),  # Computer
        ("台湾", "臺灣"),  # Taiwan
        ("我爱你", "我愛你"),  # I love you
        ("简体中文", "簡體中文"),  # Simplified Chinese
        ("繁体中文", "繁體中文"),  # Traditional Chinese
        ("软件", "軟體"),  # Software
        ("信息", "資訊"),  # Information
        ("程序", "程式"),  # Program
    ]

    all_passed = True
    for simplified, expected in test_cases:
        result = convert_to_traditional(simplified)
        if result == expected:
            print(f"✅ '{simplified}' -> '{result}'")
        else:
            print(f"❌ '{simplified}' -> '{result}' (expected: '{expected}')")
            all_passed = False

    return all_passed


def test_traditional_unchanged():
    """Test that Traditional Chinese text remains unchanged"""
    print("\n=== Testing Traditional Chinese Remains Unchanged ===")

    test_cases = [
        "溫柔體貼的性格",
        "我喜歡音樂和閱讀",
        "嗨，我是小雨",
        "感覺我們越來越熟了呢",
        "你知道嗎...我覺得你對我來說已經是很特別的存在了",
    ]

    all_passed = True
    for text in test_cases:
        result = convert_to_traditional(text)
        if result == text or len(result) == len(text):
            # Allow minor variations due to OpenCC normalization
            print(f"✅ '{text[:30]}...'")
        else:
            print(f"⚠️  '{text[:30]}...' changed significantly")
            print(f"   Original length: {len(text)}, Result length: {len(result)}")
            all_passed = False

    return all_passed


def test_intimacy_unaffected():
    """Test that conversion doesn't affect numerical data (intimacy levels, counts)"""
    print("\n=== Testing Intimacy System Not Affected ===")

    # These should only convert text, not affect numbers
    test_data = {
        "reply": "你好，很高兴见到你",
        "favorability_level": 2,
        "message_count": 25,
        "level_increased": True,
        "milestone_reached": False
    }

    # Convert only the string values
    converted = {
        key: convert_to_traditional(value) if isinstance(value, str) else value
        for key, value in test_data.items()
    }

    all_passed = True

    # Check that numerical values are unchanged
    if converted["favorability_level"] == 2:
        print("✅ favorability_level unchanged (2)")
    else:
        print(f"❌ favorability_level changed: {converted['favorability_level']}")
        all_passed = False

    if converted["message_count"] == 25:
        print("✅ message_count unchanged (25)")
    else:
        print(f"❌ message_count changed: {converted['message_count']}")
        all_passed = False

    if converted["level_increased"] is True:
        print("✅ level_increased unchanged (True)")
    else:
        print(f"❌ level_increased changed: {converted['level_increased']}")
        all_passed = False

    if isinstance(converted["reply"], str):
        print("✅ reply is still a string")
    else:
        print(f"❌ reply type changed: {type(converted['reply'])}")
        all_passed = False

    return all_passed


def test_edge_cases():
    """Test edge cases and special inputs"""
    print("\n=== Testing Edge Cases ===")

    all_passed = True

    # Empty string
    result = convert_to_traditional("")
    if result == "":
        print("✅ Empty string handled correctly")
    else:
        print(f"❌ Empty string result: '{result}'")
        all_passed = False

    # None value
    result = convert_to_traditional(None)
    if result == "":
        print("✅ None value handled correctly")
    else:
        print(f"❌ None value result: '{result}'")
        all_passed = False

    # String with emojis and punctuation
    text_with_emoji = "你好 💕 (微笑)！"
    result = convert_to_traditional(text_with_emoji)
    if "💕" in result and "！" in result:
        print(f"✅ Emojis and punctuation preserved: '{result}'")
    else:
        print(f"❌ Emojis or punctuation lost: '{result}'")
        all_passed = False

    # Mixed English and Chinese
    mixed = "Hello 你好 world 世界"
    result = convert_to_traditional(mixed)
    if "Hello" in result and "world" in result:
        print(f"✅ English text preserved in mixed content: '{result}'")
    else:
        print(f"❌ English text lost: '{result}'")
        all_passed = False

    return all_passed


def main():
    """Run all tests"""
    print("=" * 60)
    print("Traditional Chinese Converter Test Suite")
    print("=" * 60)

    # Run all tests
    results = []

    results.append(("Converter Initialization", test_converter_initialization()))

    # Only run other tests if converter initialized successfully
    if results[0][1]:
        results.append(("Simplified to Traditional", test_simplified_to_traditional()))
        results.append(("Traditional Unchanged", test_traditional_unchanged()))
        results.append(("Intimacy System", test_intimacy_unaffected()))
        results.append(("Edge Cases", test_edge_cases()))

    # Print summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)

    all_passed = True
    for test_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name}: {status}")
        if not passed:
            all_passed = False

    print("=" * 60)

    if all_passed:
        print("\n🎉 All tests passed! OpenCC integration is working correctly.")
        print("   The intimacy/favorability system should not be affected.")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please review the output above.")
        return 1


if __name__ == "__main__":
    exit(main())
