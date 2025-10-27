# Testing the Character Picture Feature

## ✅ What Was Fixed

1. **Absolute Path Resolution** - Fixed picture path to use absolute paths from project root
2. **Debug Logging** - Added detailed logging to track picture selection
3. **Static Files Mounting** - Verified proper mounting of `/pictures` directory
4. **API Integration** - Picture URL included in `/api/generate-character` response

## 🧪 Testing Steps

### Step 1: Test Picture Manager (Unit Test)

Open **Command Prompt** (Windows) or **Terminal** (Mac/Linux):

```bash
cd C:\Users\Administrator\Desktop\7755_clone\Desktop\7755
python test_picture_feature.py
```

**Expected Output:**
```
✅ Female picture: /pictures/female/xxx.png
✅ Male picture: /pictures/male/xxx.png
✅ ALL TESTS PASSED!
```

### Step 2: Start the Server

**Option A: Using batch file (Windows)**
- Double-click `run_server.bat`

**Option B: Using command line**
```bash
cd C:\Users\Administrator\Desktop\7755_clone\Desktop\7755
python -m uvicorn backend.main:app --reload
```

**Look for these messages in the console:**
```
📁 PictureManager initialized:
   Base path: C:\Users\Administrator\Desktop\7755_clone\Desktop\7755\pictures
   Female path exists: True
   Male path exists: True
✅ Mounted pictures directory: C:\Users\Administrator\Desktop\7755_clone\Desktop\7755\pictures
```

### Step 3: Test via API (Automated)

Open a **NEW** Command Prompt window:

```bash
cd C:\Users\Administrator\Desktop\7755_clone\Desktop\7755
python test_picture_api.py
```

**Expected Output:**
```
✅ Response received successfully!
🖼️ Character Picture: /pictures/female/xxx.png
   ✅ Picture URL is present!
   ✅ Correct gender folder (female)
   ✅ Picture is accessible!
```

### Step 4: Test via Browser

1. **Open browser** and go to: http://localhost:8000/docs

2. **Find `/api/generate-character` endpoint**

3. **Click "Try it out"**

4. **Paste this test data:**
```json
{
  "user_name": "測試",
  "user_gender": "男",
  "user_preference": "女",
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
```

5. **Click "Execute"**

6. **Check the response** - Should include:
```json
{
  "success": true,
  "character": {...},
  "initial_message": "...",
  "character_picture": "/pictures/female/xxx.png",  ← THIS!
  "message": "角色生成成功！"
}
```

7. **Test the picture URL** - Copy the picture URL and open in new tab:
```
http://localhost:8000/pictures/female/xxx.png
```
You should see the character picture!

## 🖼️ Verifying Picture in UI

When you create a character via the web UI at http://localhost:8000/ui:

1. Fill in the form and create a character
2. Check the browser console (F12 → Console)
3. Look for the API response containing `character_picture`
4. The frontend should display the picture in the initial message

## 📊 Expected Behavior

### ✅ Pictures SHOULD appear:
- In `/api/generate-character` response
- Only in the **first/initial** message when character is created
- Randomly selected based on character gender

### ❌ Pictures should NOT appear:
- In `/api/v2/send-message` responses (chat messages)
- In subsequent messages after the initial greeting
- For invalid genders or missing picture folders

## 🐛 Troubleshooting

### Issue: No picture in response (`character_picture: null`)

**Check the server console for:**
```
⚠️ Warning: Picture directory does not exist
⚠️ Warning: No pictures found in ...
```

**Solutions:**
1. Verify pictures exist:
   ```bash
   dir pictures\female
   dir pictures\male
   ```
2. Check picture formats (should be .jpg, .png, .gif, .webp)
3. Restart the server

### Issue: Picture URL returns 404

**Check:**
1. Server console shows: `✅ Mounted pictures directory`
2. Picture URL matches format: `/pictures/female/filename.png`
3. File actually exists in the pictures folder

**Test directly:**
```
http://localhost:8000/pictures/female/
```

### Issue: Server won't start

**Error: "No module named 'fastapi'"**
```bash
python -m pip install -r requirements.txt
```

**Error: "Address already in use"**
```bash
# Use different port
python -m uvicorn backend.main:app --reload --port 8080
```

## 📝 Debug Checklist

When testing, verify these outputs appear in server console:

- [ ] `📁 PictureManager initialized:`
- [ ] `Female path exists: True`
- [ ] `Male path exists: True`
- [ ] `✅ Mounted pictures directory:`
- [ ] `🖼️ Selected picture for 女: /pictures/female/xxx.png` (when generating character)

If any of these are missing, there's an issue with the setup.

## 🎯 What Should Happen

1. **Server Starts:**
   - Picture manager initializes
   - Pictures directory mounted
   - Paths verified

2. **Character Created:**
   - Random picture selected based on gender
   - Picture URL included in response
   - Picture logged to console

3. **Picture Accessible:**
   - Can access via URL in browser
   - Proper content-type header
   - Image displays correctly

4. **Subsequent Messages:**
   - NO picture included
   - Only text responses

## ✨ Success Criteria

You'll know it's working when:

1. ✅ Test script passes all tests
2. ✅ Server shows picture paths in logs
3. ✅ API response includes `character_picture` field
4. ✅ Picture URL opens and displays image in browser
5. ✅ Different pictures selected randomly
6. ✅ Correct gender folder used (female/male)

---

**Need help?** Check the server console for detailed error messages with emoji indicators (⚠️, ❌, ✅)
