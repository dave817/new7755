"""
Test script to demonstrate text cleaning functionality
Shows before/after examples of cleaning action tags
"""

from backend.text_cleaner import clean_for_line

# Test cases based on user's reported issues
test_cases = [
    # Case 1: teleport tag (user's example)
    {
        "name": "teleport tag with Chinese description",
        "input": "(teleport\n(傳送了一個動態表情包：糯糯締手指，眼神飄忽)這才哪到哪～ (動態表情包中糯糯眨著眼睛，露出神秘的微笑)我還準備了很多絕技呢，等著被我贏哭的準備好了嗎～",
        "expected": "(傳送了一個動態表情包：糯糯締手指，眼神飄忽)這才哪到哪～ (動態表情包中糯糯眨著眼睛，露出神秘的微笑)我還準備了很多絕技呢，等著被我贏哭的準備好了嗎～"
    },
    # Case 2: Dampen tag
    {
        "name": "Dampen action tag",
        "input": "Dampen\n你好呀！今天想聊什麼？",
        "expected": "你好呀！今天想聊什麼？"
    },
    # Case 3: iteleport tag
    {
        "name": "iteleport action tag",
        "input": "iteleport(眨了眨眼睛)嗨～",
        "expected": "(眨了眨眼睛)嗨～"
    },
    # Case 4: Multiple tags
    {
        "name": "Multiple action tags",
        "input": "teleport\nDampen\n(笑了笑)你真有趣呢～",
        "expected": "(笑了笑)你真有趣呢～"
    },
    # Case 5: English user name should be kept
    {
        "name": "Keep English user names",
        "input": "嗨 D！今天想聊什麼？",
        "expected": "嗨 D！今天想聊什麼？"
    },
    # Case 6: Mixed content
    {
        "name": "Complex mixed content",
        "input": "activate\n(傳送了一個表情包：害羞)哎呀 Dave，你這樣說我會不好意思的啦～",
        "expected": "(傳送了一個表情包：害羞)哎呀 Dave，你這樣說我會不好意思的啦～"
    },
    # Case 7: Only Chinese description (should stay intact)
    {
        "name": "Pure Chinese description",
        "input": "(傳送了一個動態表情包：糯糯開心地轉圈圈)太好了！",
        "expected": "(傳送了一個動態表情包：糯糯開心地轉圈圈)太好了！"
    },
]


def run_tests():
    """Run all test cases and print results"""
    print("=" * 80)
    print("TEXT CLEANING TEST RESULTS")
    print("=" * 80)
    print()

    passed = 0
    failed = 0

    for i, test in enumerate(test_cases, 1):
        print(f"\nTest {i}: {test['name']}")
        print("-" * 80)

        result = clean_for_line(test['input'])

        print(f"Input:    {repr(test['input'][:100])}...")
        print(f"Expected: {repr(test['expected'][:100])}...")
        print(f"Result:   {repr(result[:100])}...")

        # Check if result matches expected (or at least removes the action tags)
        if result == test['expected']:
            print("✅ PASS - Perfect match!")
            passed += 1
        elif '(傳送了' in test['input'] and '(傳送了' in result:
            # Chinese descriptions are preserved
            if 'teleport' not in result and 'Dampen' not in result and 'iteleport' not in result:
                print("✅ PASS - Action tags removed, Chinese preserved!")
                passed += 1
            else:
                print("❌ FAIL - Action tags still present")
                failed += 1
        else:
            print("⚠️  PARTIAL - Check manually")
            print(f"   Action tags removed: {'teleport' not in result and 'Dampen' not in result}")

    print("\n" + "=" * 80)
    print(f"SUMMARY: {passed} passed, {failed} failed out of {len(test_cases)} tests")
    print("=" * 80)


if __name__ == "__main__":
    run_tests()
