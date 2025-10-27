# Testing Character Picture in UI2

## ✅ Changes Made

### Backend (`backend/main.py`)
1. ✅ Updated `/api/v2/create-character` endpoint to include `character_picture` field
2. ✅ Added CSS for character picture display with hover effects
3. ✅ Updated JavaScript `displayCharacter()` function to accept and display picture
4. ✅ Updated JavaScript `displayMessage()` function to show picture in chat

### How It Works
- Picture appears in TWO places:
  1. In the character profile card (top section)
  2. In the chat message area (with the initial greeting)
- Picture is **only shown once** - in the initial message
- Subsequent chat messages do NOT include pictures

## 🧪 Testing Steps

### Step 1: Restart the Server

**IMPORTANT:** You must restart the server for changes to take effect!

```bash
# If server is running, press Ctrl+C to stop it
# Then restart:
cd C:\Users\Administrator\Desktop\7755_clone\Desktop\7755
python -m uvicorn backend.main:app --reload
```

**Look for these messages in console:**
```
📁 PictureManager initialized:
   Base path: C:\Users\Administrator\Desktop\7755_clone\Desktop\7755\pictures
   Female path exists: True
   Male path exists: True
✅ Mounted pictures directory: ...
```

### Step 2: Open UI2 in Browser

1. Open your browser
2. Go to: **http://localhost:8000/ui2**
3. You should see the character creation form

### Step 3: Create a Character

Fill in the form:

**Step 1 - Basic Info:**
- Your Name: `測試用戶`
- Your Gender: `男`
- Preference: `女` (to get a female character with picture)

**Step 2 - Dream Partner:**
- Talking Style: `溫柔體貼`
- Personality: Check some traits like `溫柔`, `體貼`
- Interests: `音樂、閱讀`
- Age Range: `22-25`
- Occupation: `學生`

**Step 3 - Personal Info:**
- You can skip this or add some info

**Step 4 - Generate:**
- Click the generate button

### Step 4: Verify Picture Appears

After character generation, you should see:

1. **✅ In the Character Profile Card:**
   ```
   💕 [Character Name] ([Nickname])
   [CHARACTER PICTURE HERE] ← Should appear here!
   身份：...
   性格：...
   ```

2. **✅ In the Chat Messages:**
   ```
   [CHARACTER PICTURE] ← Should appear here too!
   [Character Name]：嗨！我是... (initial greeting)
   ```

### Step 5: Test Subsequent Messages

1. Type a message in the chat box
2. Send it
3. **✅ Verify:** The character's reply should NOT include a picture
4. Only text should appear in subsequent messages

## 🎯 What Should Happen

### ✅ SUCCESS if you see:
1. Character picture appears under the character name
2. Picture appears in the first chat message
3. Picture is properly sized and styled (rounded corners, shadow)
4. Hover effect works (slight zoom on hover)
5. **No picture** in subsequent chat messages

### ❌ FAILURE if:
1. No picture appears at all
2. Picture appears in every message (should only be first)
3. Picture shows as broken image icon
4. Picture URL returns 404

## 🐛 Troubleshooting

### Issue: No Picture Appears

**Check 1: Server logs**
Look for this in server console when creating character:
```
🖼️ Selected picture for 女: /pictures/female/xxx.png
```

**Check 2: Browser console**
1. Press F12 to open developer tools
2. Go to Console tab
3. Look for errors about loading images
4. Go to Network tab
5. Check if picture request returns 200 OK

**Check 3: Verify API response**
1. Open F12 Developer Tools
2. Go to Network tab
3. Create a character
4. Find the request to `/api/v2/create-character`
5. Check the response includes:
   ```json
   {
     "character_picture": "/pictures/female/xxx.png"
   }
   ```

**Check 4: Test picture URL directly**
1. Create a character
2. Right-click on the picture → Copy image address
3. Open in new tab
4. Should show the picture

### Issue: Picture in Every Message

This means the picture is being passed to subsequent `displayMessage()` calls.
- **Expected:** Only the initial call should pass the picture
- **Verify:** Check that `sendMessage()` function doesn't pass picture parameter

### Issue: Broken Image Icon

**Possible causes:**
1. Picture file doesn't exist
2. Wrong path
3. Static files not mounted

**Solution:**
1. Check server started message shows: `✅ Mounted pictures directory`
2. Test direct URL: `http://localhost:8000/pictures/female/` (should list or error)
3. Verify files exist in `pictures/female/` folder

## 📊 Example Console Output

When creating a female character, you should see:
```
📁 PictureManager initialized:
   Base path: C:\Users\Administrator\Desktop\7755_clone\Desktop\7755\pictures
   Female path exists: True
   Male path exists: True
✅ Mounted pictures directory: C:\Users\Administrator\Desktop\7755_clone\Desktop\7755\pictures
🖼️ Selected picture for 女: /pictures/female/abc123.png
INFO:     127.0.0.1:xxxxx - "POST /api/v2/create-character HTTP/1.1" 200 OK
```

## 🎨 Visual Check

The picture should:
- ✅ Be centered in its container
- ✅ Have rounded corners (12px border-radius)
- ✅ Have a subtle shadow
- ✅ Zoom slightly on hover (1.02x scale)
- ✅ Be max 300px wide on desktop
- ✅ Be responsive on mobile (100% width)

## 📝 Testing Checklist

- [ ] Server restarted with picture manager initialized
- [ ] UI2 page loads at http://localhost:8000/ui2
- [ ] Fill out character creation form
- [ ] Character generated successfully
- [ ] Picture appears in character profile card
- [ ] Picture appears in first chat message
- [ ] Picture has proper styling (rounded, shadow, centered)
- [ ] Hover effect works on picture
- [ ] Subsequent messages do NOT have pictures
- [ ] Different characters get different random pictures

## ✨ Success!

If all checks pass, the feature is working correctly! 🎉

**The character picture now appears in:**
1. ✅ Character profile card (after generation)
2. ✅ First chat message only
3. ❌ NOT in subsequent messages (as designed)

---

**Need help?** Check the server console for detailed logs with emoji indicators (🖼️, ✅, ⚠️)
