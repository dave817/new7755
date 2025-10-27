# Character Picture Feature

## Overview
This feature adds character profile pictures to the initial greeting message from AI companions. Pictures are randomly selected based on the character's gender and are only sent once during character creation.

## 📁 Folder Structure

```
7755/
├── pictures/
│   ├── female/          # Pictures for female characters (女)
│   │   ├── image1.png
│   │   ├── image2.jpg
│   │   └── ...
│   └── male/            # Pictures for male characters (男)
│       ├── image1.png
│       ├── image2.jpg
│       └── ...
```

## 🎯 How It Works

### 1. Picture Selection
- When a character is generated via `/api/generate-character`, the system automatically selects a random picture
- Selection is based on the character's gender:
  - `女` (female) → selects from `pictures/female/`
  - `男` (male) → selects from `pictures/male/`

### 2. Initial Message Only
- The picture URL is **only included** in the response from `/api/generate-character`
- Subsequent messages via `/api/v2/send-message` do **NOT** include pictures
- This ensures the picture appears only in the introductory message

### 3. Picture URL Format
Pictures are served as static files and accessible via:
```
http://localhost:8000/pictures/female/<filename>
http://localhost:8000/pictures/male/<filename>
```

## 🔧 API Response Format

### Generate Character Endpoint
**POST** `/api/generate-character`

**Response:**
```json
{
  "success": true,
  "character": {
    "name": "小雨",
    "gender": "女",
    ...
  },
  "initial_message": "嗨！我是小雨...",
  "character_picture": "/pictures/female/random-image.png",
  "message": "角色生成成功！"
}
```

### Send Message Endpoint (No Picture)
**POST** `/api/v2/send-message`

**Response:**
```json
{
  "message": "這是對話回應內容",
  "conversation_id": "...",
  ...
  // No "character_picture" field
}
```

## 🧪 Testing

### Run the Test Script
```bash
python test_picture_feature.py
```

This will:
- ✅ Verify picture folders exist
- ✅ Test picture selection for both genders
- ✅ Verify randomness of selection
- ✅ Confirm pictures are correctly formatted

### Manual API Testing

1. **Start the server:**
   ```bash
   python -m uvicorn backend.main:app --reload
   ```

2. **Create a female character:**
   ```bash
   curl -X POST http://localhost:8000/api/generate-character \
     -H "Content-Type: application/json" \
     -d '{
       "user_name": "測試",
       "user_gender": "男",
       "user_preference": "女",
       "dream_type": {
         "personality_traits": ["溫柔"],
         "talking_style": "溫柔體貼",
         "interests": ["音樂"]
       },
       "custom_memory": {}
     }'
   ```

3. **Check the response** includes `character_picture` field

4. **Access the picture** in browser:
   ```
   http://localhost:8000/pictures/female/<filename-from-response>
   ```

## 📝 Implementation Details

### Files Modified/Created

1. **`backend/picture_utils.py`** (NEW)
   - `PictureManager` class for handling picture selection
   - `get_random_picture(gender)` - Returns random picture URL
   - `picture_exists(gender)` - Checks if pictures available

2. **`backend/main.py`** (MODIFIED)
   - Imported `StaticFiles` from FastAPI
   - Mounted `/pictures` directory as static files
   - Updated `/api/generate-character` to include `character_picture`

3. **`test_picture_feature.py`** (NEW)
   - Test script to verify functionality

### Supported Image Formats
- `.jpg` / `.jpeg`
- `.png`
- `.gif`
- `.webp`

## 🎨 Frontend Integration

To display the picture in your frontend:

```javascript
// After calling /api/generate-character
const response = await fetch('/api/generate-character', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(userProfile)
});

const data = await response.json();

// Display the picture (only in initial message)
if (data.character_picture) {
  const imgElement = document.createElement('img');
  imgElement.src = data.character_picture;
  imgElement.alt = data.character.name;
  // Add to your UI
}
```

## ⚙️ Configuration

### Adding New Pictures
1. Simply add image files to the appropriate folder:
   - Female characters: `pictures/female/`
   - Male characters: `pictures/male/`
2. No server restart needed
3. New pictures will be automatically included in random selection

### Picture Requirements
- Recommended size: 512x512px or larger
- Supported formats: JPG, PNG, GIF, WEBP
- File naming: Any valid filename

## 🐛 Troubleshooting

### No Picture Returned
**Symptom:** `character_picture` is `null` in response

**Possible causes:**
1. Pictures folder doesn't exist
2. No images in the gender-specific folder
3. Invalid image format

**Solution:**
- Check console for warnings when server starts
- Verify pictures exist in `pictures/female/` or `pictures/male/`
- Ensure images have correct extensions

### Picture Not Loading
**Symptom:** Picture URL returns 404

**Possible causes:**
1. Static files not mounted correctly
2. Picture path incorrect

**Solution:**
- Check server startup logs for "✅ Mounted pictures directory"
- Verify the file exists at the path shown in response
- Test direct access: `http://localhost:8000/pictures/female/<filename>`

### Same Picture Every Time
**Symptom:** Always getting the same picture

**Possible causes:**
1. Only one picture in the folder
2. Random seed issue (unlikely)

**Solution:**
- Add more pictures to the folder
- Verify multiple files exist with `ls pictures/female/` or `ls pictures/male/`

## 📚 Related Documentation
- Main README: [README.md](README.md)
- Quick Start: [QUICKSTART.md](QUICKSTART.md)
- API Documentation: http://localhost:8000/docs (when server running)

---

**Feature implemented:** 2025-10-27
**Version:** 1.0.0
