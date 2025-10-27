# Frontend Debugging Guide - No Picture in Chat

## 🔍 Step-by-Step Debugging Process

Follow these steps in order to find out why the picture isn't showing.

---

## ✅ STEP 1: Test the API (Backend)

### Run the debug script:

```cmd
cd C:\Users\Administrator\Desktop\7755_clone\Desktop\7755
python debug_picture.py
```

### What to look for:

**✅ GOOD - API is working:**
```
✅ 'character_picture' field EXISTS!
📸 Picture URL: /pictures/female/xxx.png
✅ Picture is ACCESSIBLE!
```

**❌ BAD - API issue:**
```
❌ PROBLEM: 'character_picture' field is MISSING!
```

**If API test fails:**
- Server didn't restart with new code
- Run `kill_and_restart.bat` again
- Make sure you see the PictureManager initialization messages

**If API test passes:** Continue to Step 2 →

---

## ✅ STEP 2: Check Browser Console

### Open Developer Tools:
1. Open browser at http://localhost:8000/ui2
2. Press `F12` to open Developer Tools
3. Click on **Console** tab

### Create a character and watch the console

**Look for errors:**
- Red error messages
- Failed to load resource
- JavaScript errors

### Common errors:

**Error 1: Image failed to load**
```
GET http://localhost:8000/pictures/female/xxx.png 404 (Not Found)
```
**Solution:** Picture file doesn't exist, check pictures folder

**Error 2: JavaScript error**
```
Uncaught TypeError: Cannot read property 'character_picture' of undefined
```
**Solution:** API response structure issue

**Error 3: CORS error**
```
Access to image blocked by CORS policy
```
**Solution:** Static files not mounted correctly

---

## ✅ STEP 3: Check Network Tab

### In Developer Tools (F12):
1. Click on **Network** tab
2. Clear the network log (🚫 icon)
3. Create a new character
4. Watch the network requests

### Check these requests:

**Request 1: `/api/v2/create-character`**
- Status should be: `200 OK`
- Click on it → Go to **Response** tab
- Look for: `"character_picture": "/pictures/female/xxx.png"`

**If missing:** Server code didn't update, restart server

**Request 2: `/pictures/female/xxx.png`**
- Status should be: `200 OK`
- Type should be: `png` or `image/png`

**If 404:** Picture file doesn't exist
**If no request:** JavaScript isn't loading the image

---

## ✅ STEP 4: Check the HTML

### In Developer Tools (F12):
1. Click on **Elements** tab (or **Inspector** in Firefox)
2. After creating a character, press `Ctrl+F` to search
3. Search for: `character-picture`

### What you should see:

**✅ GOOD:**
```html
<div class="character-picture-container">
  <img src="/pictures/female/xxx.png" alt="小雨" class="character-picture">
</div>
```

**❌ BAD - No picture element:**
```html
<!-- No <img> tag found -->
```
**Solution:** JavaScript isn't creating the image element

**❌ BAD - Broken src:**
```html
<img src="null" ...>
<img src="undefined" ...>
```
**Solution:** API isn't returning character_picture

---

## ✅ STEP 5: Manual JavaScript Test

### In Console tab, after creating character, run:

```javascript
// Check if data was received
console.log('Last API response:', arguments);

// Try to get the picture URL
fetch('/api/v2/create-character', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    user_name: "Test",
    user_gender: "男",
    user_preference: "女",
    dream_type: {
      personality_traits: ["溫柔"],
      talking_style: "溫柔體貼",
      interests: ["音樂"],
      age_range: "22-25",
      occupation: "學生"
    },
    custom_memory: {likes: {}, dislikes: {}, habits: {}, personal_background: {}}
  })
})
.then(r => r.json())
.then(data => {
  console.log('API Response:', data);
  console.log('Picture URL:', data.character_picture);

  if (data.character_picture) {
    console.log('✅ Picture URL exists:', data.character_picture);
    // Try to load it
    let img = new Image();
    img.onload = () => console.log('✅ Picture loaded successfully!');
    img.onerror = () => console.log('❌ Picture failed to load!');
    img.src = data.character_picture;
  } else {
    console.log('❌ No character_picture in response!');
  }
});
```

### What you should see:

**✅ GOOD:**
```
✅ Picture URL exists: /pictures/female/xxx.png
✅ Picture loaded successfully!
```

**❌ BAD:**
```
❌ No character_picture in response!
```

---

## ✅ STEP 6: Check Server Console

### Look at your server terminal/console

**When creating character, you should see:**
```
🖼️ Selected picture for 女: /pictures/female/xxx.png
INFO: 127.0.0.1:xxxxx - "POST /api/v2/create-character HTTP/1.1" 200 OK
```

**If you DON'T see `🖼️ Selected picture`:**
- Server didn't restart with new code
- PictureManager isn't working
- Kill and restart server

**Check startup messages:**
```
📁 PictureManager initialized:
   Base path: C:\Users\Administrator\Desktop\7755_clone\Desktop\7755\pictures
   Female path exists: True
   Male path exists: True
✅ Mounted pictures directory: ...
```

**If you DON'T see these:** Old code is running!

---

## 🔧 COMMON FIXES

### Fix 1: Server Not Restarted
```cmd
# Kill everything
taskkill /F /IM python.exe

# Wait 5 seconds
timeout /t 5

# Restart
cd C:\Users\Administrator\Desktop\7755_clone\Desktop\7755
python -m uvicorn backend.main:app --reload
```

### Fix 2: Browser Cache
```
1. Press Ctrl+Shift+Delete
2. Clear "Cached images and files"
3. Clear "Cookies and site data"
4. Close ALL browser windows
5. Reopen browser
6. Go to http://localhost:8000/ui2
7. Hard refresh: Ctrl+Shift+R
```

### Fix 3: Try Incognito/Private Mode
```
1. Press Ctrl+Shift+N (Chrome/Edge)
2. Go to http://localhost:8000/ui2
3. Create character
4. If it works here, it's a cache issue
```

### Fix 4: Check File Permissions
```cmd
# Check if pictures folder is accessible
dir C:\Users\Administrator\Desktop\7755_clone\Desktop\7755\pictures\female
```

Should show list of image files.

---

## 📊 Debugging Checklist

Complete this checklist to find the problem:

- [ ] Server shows PictureManager initialization on startup
- [ ] Server shows `🖼️ Selected picture` when creating character
- [ ] `debug_picture.py` script passes all tests
- [ ] API response includes `character_picture` field
- [ ] Picture URL is not null/undefined
- [ ] Picture URL is accessible (returns 200 OK)
- [ ] Browser console shows no errors
- [ ] Network tab shows picture request
- [ ] Network tab shows picture returns 200 OK
- [ ] HTML elements contain `<img class="character-picture">`
- [ ] Image src is correct URL (not null/undefined)
- [ ] Browser cache cleared
- [ ] Hard refresh performed (Ctrl+Shift+R)

---

## 🆘 Still Not Working?

### Share this information:

1. **Server startup logs** (copy everything from server console)
2. **API response** (from `debug_picture.py` output)
3. **Browser console errors** (screenshot of Console tab)
4. **Network tab** (screenshot showing the requests)
5. **HTML inspection** (search for "character-picture" in Elements tab)

### Nuclear option:

```cmd
# 1. Kill everything
taskkill /F /IM python.exe

# 2. Delete database (fresh start)
del dating_chatbot.db

# 3. Restart computer

# 4. After restart, run:
cd C:\Users\Administrator\Desktop\7755_clone\Desktop\7755
python -m uvicorn backend.main:app --reload

# 5. Fresh browser (no cache):
# - Open incognito window
# - Go to http://localhost:8000/ui2
# - Create character
```

---

## 📝 Quick Test Commands

**Test 1: Check server is running**
```cmd
curl http://localhost:8000/health
```
Should return: `{"status":"healthy","service":"dating-chatbot"}`

**Test 2: Check pictures directory mounted**
```cmd
curl http://localhost:8000/pictures/
```
Should NOT return 404

**Test 3: Check specific picture**
```cmd
curl http://localhost:8000/pictures/female/ -I
```
Should return headers (200 or 403, but not 404)

---

**Run `debug_picture.py` first, then follow the steps based on what fails!**
