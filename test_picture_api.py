"""
Test the picture feature via the actual API endpoint
This script tests that the /api/generate-character endpoint includes the character picture
"""
import requests
import json

API_BASE_URL = "http://localhost:8000"


def test_generate_character_with_picture():
    """Test that generate-character returns a picture URL"""
    print("🧪 Testing /api/generate-character endpoint")
    print("=" * 60)

    # Test data for female character
    user_profile = {
        "user_name": "測試用戶",
        "user_gender": "男",
        "user_preference": "女",
        "dream_type": {
            "personality_traits": ["溫柔", "體貼"],
            "talking_style": "溫柔體貼",
            "interests": ["音樂", "閱讀"],
            "age_range": "22-25",
            "occupation": "學生"
        },
        "custom_memory": {
            "likes": {"food": ["咖啡"]},
            "dislikes": {},
            "habits": {},
            "personal_background": {}
        }
    }

    print(f"\n📤 Sending POST request to {API_BASE_URL}/api/generate-character")
    print(f"   User preference: {user_profile['user_preference']} (should get female picture)")

    try:
        response = requests.post(
            f"{API_BASE_URL}/api/generate-character",
            json=user_profile,
            timeout=30
        )

        print(f"\n📥 Response status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()

            print("\n✅ Response received successfully!")
            print("\n📋 Response fields:")
            for key in data.keys():
                print(f"   - {key}")

            # Check for character_picture field
            if "character_picture" in data:
                picture_url = data["character_picture"]
                print(f"\n🖼️ Character Picture: {picture_url}")

                if picture_url:
                    print(f"   ✅ Picture URL is present!")

                    # Check if it's a female picture
                    if "/pictures/female/" in picture_url:
                        print(f"   ✅ Correct gender folder (female)")
                    elif "/pictures/male/" in picture_url:
                        print(f"   ⚠️ Male picture returned (expected female)")
                    else:
                        print(f"   ⚠️ Unexpected picture path format")

                    # Try to access the picture
                    picture_full_url = f"{API_BASE_URL}{picture_url}"
                    print(f"\n🔗 Testing picture URL: {picture_full_url}")

                    try:
                        pic_response = requests.get(picture_full_url, timeout=10)
                        if pic_response.status_code == 200:
                            print(f"   ✅ Picture is accessible!")
                            print(f"   Content-Type: {pic_response.headers.get('content-type')}")
                            print(f"   Size: {len(pic_response.content)} bytes")
                        else:
                            print(f"   ❌ Picture URL returned status {pic_response.status_code}")
                    except Exception as e:
                        print(f"   ❌ Error accessing picture: {e}")

                else:
                    print(f"   ⚠️ Picture URL is None/empty")
            else:
                print(f"\n❌ 'character_picture' field is missing from response!")
                print(f"\nFull response:")
                print(json.dumps(data, indent=2, ensure_ascii=False))

            # Show character info
            if "character" in data:
                char = data["character"]
                print(f"\n👤 Generated Character:")
                print(f"   Name: {char.get('name')}")
                print(f"   Gender: {char.get('gender')}")

            # Show initial message
            if "initial_message" in data:
                print(f"\n💬 Initial Message:")
                print(f"   {data['initial_message'][:100]}...")

        else:
            print(f"❌ Request failed with status {response.status_code}")
            print(f"Response: {response.text}")

    except requests.exceptions.ConnectionError:
        print("\n❌ Connection Error!")
        print("   Make sure the server is running:")
        print("   python -m uvicorn backend.main:app --reload")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


def test_male_character():
    """Test male character picture"""
    print("\n\n" + "=" * 60)
    print("🧪 Testing male character picture")
    print("=" * 60)

    user_profile = {
        "user_name": "測試用戶",
        "user_gender": "女",
        "user_preference": "男",
        "dream_type": {
            "personality_traits": ["成熟", "穩重"],
            "talking_style": "溫柔體貼",
            "interests": ["運動", "旅遊"],
            "age_range": "25-30",
            "occupation": "工程師"
        },
        "custom_memory": {
            "likes": {},
            "dislikes": {},
            "habits": {},
            "personal_background": {}
        }
    }

    print(f"\n📤 Sending POST request")
    print(f"   User preference: {user_profile['user_preference']} (should get male picture)")

    try:
        response = requests.post(
            f"{API_BASE_URL}/api/generate-character",
            json=user_profile,
            timeout=30
        )

        if response.status_code == 200:
            data = response.json()

            if "character_picture" in data and data["character_picture"]:
                picture_url = data["character_picture"]
                print(f"\n🖼️ Character Picture: {picture_url}")

                if "/pictures/male/" in picture_url:
                    print(f"   ✅ Correct gender folder (male)")
                else:
                    print(f"   ⚠️ Wrong gender folder")
            else:
                print(f"   ❌ No picture in response")

    except Exception as e:
        print(f"   ❌ Error: {e}")


def main():
    print("\n" + "=" * 60)
    print("🚀 Testing Picture Feature via API")
    print("=" * 60)
    print("\n⚠️ Make sure the server is running first:")
    print("   python -m uvicorn backend.main:app --reload")
    print("=" * 60)

    input("\nPress Enter to start testing...")

    # Test female character
    test_generate_character_with_picture()

    # Test male character
    test_male_character()

    print("\n\n" + "=" * 60)
    print("✅ API Testing Complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
