"""
Debug script to test if character picture is being returned by API
Run this while the server is running to check the API response
"""
import requests
import json

API_URL = "http://localhost:8000/api/v2/create-character"

def test_api_response():
    """Test the API and check if character_picture is in response"""

    print("=" * 60)
    print("🔍 DEBUGGING CHARACTER PICTURE FEATURE")
    print("=" * 60)

    # Test data
    test_data = {
        "user_name": "Debug測試",
        "user_gender": "男",
        "user_preference": "女",
        "preferred_character_name": "",
        "dream_type": {
            "personality_traits": ["溫柔", "體貼"],
            "talking_style": "溫柔體貼",
            "interests": ["音樂"],
            "age_range": "22-25",
            "occupation": "學生"
        },
        "custom_memory": {
            "likes": {},
            "dislikes": {},
            "habits": {},
            "personal_background": {}
        }
    }

    print("\n1️⃣ Sending request to:", API_URL)
    print("   User Preference: 女 (should get female picture)")

    try:
        response = requests.post(API_URL, json=test_data, timeout=30)

        print(f"\n2️⃣ Response Status: {response.status_code}")

        if response.status_code != 200:
            print(f"\n❌ ERROR: Server returned status {response.status_code}")
            print(f"Response: {response.text}")
            return False

        data = response.json()

        print("\n3️⃣ Response Fields:")
        for key in data.keys():
            print(f"   ✓ {key}")

        # Check for character_picture
        print("\n4️⃣ Checking for 'character_picture' field...")

        if "character_picture" not in data:
            print("   ❌ PROBLEM: 'character_picture' field is MISSING!")
            print("\n   This means the API is NOT returning the picture.")
            print("   The server may not have restarted with the new code.")
            print("\n   SOLUTION:")
            print("   1. Kill the server completely")
            print("   2. Restart using: kill_and_restart.bat")
            print("   3. Run this script again")
            return False

        picture_url = data.get("character_picture")

        if picture_url is None:
            print("   ⚠️ PROBLEM: 'character_picture' exists but is NULL")
            print("\n   This means:")
            print("   - Pictures folder might not exist")
            print("   - No pictures in the gender folder")
            print("   - Path resolution issue")
            print("\n   Check server console for warnings like:")
            print("   ⚠️ Warning: Picture directory does not exist")
            print("   ⚠️ Warning: No pictures found in ...")
            return False

        print(f"   ✅ 'character_picture' field EXISTS!")
        print(f"   📸 Picture URL: {picture_url}")

        # Test if picture is accessible
        print("\n5️⃣ Testing if picture URL is accessible...")
        picture_full_url = f"http://localhost:8000{picture_url}"
        print(f"   Testing: {picture_full_url}")

        try:
            pic_response = requests.get(picture_full_url, timeout=10)

            if pic_response.status_code == 200:
                print(f"   ✅ Picture is ACCESSIBLE!")
                print(f"   Content-Type: {pic_response.headers.get('content-type')}")
                print(f"   Size: {len(pic_response.content):,} bytes")
            else:
                print(f"   ❌ Picture URL returned status {pic_response.status_code}")
                print(f"   The picture file might not exist")
                return False

        except Exception as e:
            print(f"   ❌ Error accessing picture: {e}")
            return False

        # Show character info
        print("\n6️⃣ Generated Character Info:")
        if "character" in data:
            char = data["character"]
            print(f"   Name: {char.get('name')}")
            print(f"   Gender: {char.get('gender')}")
            print(f"   Nickname: {char.get('nickname')}")

        print("\n7️⃣ Initial Message Preview:")
        if "initial_message" in data:
            msg = data["initial_message"]
            print(f"   {msg[:100]}...")

        # Full response for debugging
        print("\n8️⃣ FULL API RESPONSE:")
        print("-" * 60)
        print(json.dumps(data, indent=2, ensure_ascii=False))
        print("-" * 60)

        print("\n" + "=" * 60)
        print("✅ API TEST PASSED!")
        print("=" * 60)
        print("\n✓ The API is correctly returning the character_picture")
        print("✓ The picture URL is accessible")
        print("\n🔍 If you still don't see the picture in the browser:")
        print("   1. Open browser Developer Tools (F12)")
        print("   2. Go to Console tab - look for JavaScript errors")
        print("   3. Go to Network tab - check if image request fails")
        print("   4. Hard refresh the page (Ctrl+Shift+R)")
        print("   5. Clear browser cache completely")
        print("\n📝 Next: Check browser console for errors!")
        print("=" * 60)

        return True

    except requests.exceptions.ConnectionError:
        print("\n❌ CONNECTION ERROR!")
        print("   The server is NOT running.")
        print("\n   SOLUTION:")
        print("   1. Start the server:")
        print("      python -m uvicorn backend.main:app --reload")
        print("   2. Wait for 'Uvicorn running' message")
        print("   3. Run this script again")
        return False

    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("\n🚀 Starting API Debug Test...")
    print("\n⚠️  IMPORTANT: Make sure the server is running first!")
    print("   If not, run: kill_and_restart.bat")
    print()

    input("Press Enter to continue...")

    success = test_api_response()

    if not success:
        print("\n\n❌ TEST FAILED - See errors above")

    print("\n")
    input("Press Enter to exit...")
