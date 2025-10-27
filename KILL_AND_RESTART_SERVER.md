# How to Kill and Restart the Server

## Issue: Server Still Running After Termination

If you can still access the web page after pressing Ctrl+C, it means:
1. The server process is still running in the background
2. Your browser is showing a cached version
3. Multiple server instances might be running

## 🛑 Method 1: Kill Server Using Task Manager (Easiest)

### Step 1: Open Task Manager
- Press `Ctrl + Shift + Esc`
- Or right-click taskbar → Task Manager

### Step 2: Find Python Processes
- Go to "Details" tab
- Look for `python.exe` or `pythonw.exe`
- Look at the "Command line" column to find uvicorn processes

### Step 3: Kill All Python Processes
- Right-click on each `python.exe` → End Task
- Repeat for ALL Python processes

### Step 4: Verify Server is Stopped
- Open browser and go to: http://localhost:8000/ui2
- You should see "This site can't be reached" or "Connection refused"
- If you still see the page, clear browser cache (Ctrl+Shift+Delete)

---

## 🛑 Method 2: Kill Server Using Command Line (Windows)

### Step 1: Open Command Prompt as Administrator
- Press `Win + X`
- Select "Command Prompt (Admin)" or "Windows PowerShell (Admin)"

### Step 2: Find the Process Using Port 8000
```cmd
netstat -ano | findstr :8000
```

**Output example:**
```
TCP    0.0.0.0:8000    0.0.0.0:0    LISTENING    12345
TCP    [::]:8000       [::]:0       LISTENING    12345
```

The last number (12345) is the Process ID (PID)

### Step 3: Kill the Process
```cmd
taskkill /F /PID 12345
```

Replace `12345` with the actual PID from step 2.

**Or kill ALL Python processes:**
```cmd
taskkill /F /IM python.exe
```

### Step 4: Verify
```cmd
netstat -ano | findstr :8000
```

Should return nothing (empty).

---

## 🛑 Method 3: Kill All Python Processes (PowerShell)

### In PowerShell (Admin):
```powershell
# See all Python processes
Get-Process python*

# Kill all Python processes
Get-Process python* | Stop-Process -Force
```

---

## 🧹 Clear Browser Cache

Even after killing the server, your browser might show cached content.

### Chrome/Edge:
1. Press `Ctrl + Shift + Delete`
2. Select "Cached images and files"
3. Time range: "Last hour"
4. Click "Clear data"

### Or Force Refresh:
- Press `Ctrl + Shift + R` (hard refresh)
- Or `Ctrl + F5`

---

## ✅ Verify Server is Completely Stopped

### Test 1: Try to access the page
```
http://localhost:8000/ui2
```

**Should show:**
- "This site can't be reached"
- "ERR_CONNECTION_REFUSED"
- Or similar error

**If page still loads:**
- Clear browser cache again
- Try different browser
- Check if there are still Python processes running

### Test 2: Check port 8000
```cmd
netstat -ano | findstr :8000
```

**Should return:** Nothing (empty)

**If it shows results:** Another process is using port 8000, kill it.

---

## 🚀 Restart the Server Properly

### Step 1: Open NEW Command Prompt
- Open fresh Command Prompt (not Admin needed)
- Navigate to project directory

```cmd
cd C:\Users\Administrator\Desktop\7755_clone\Desktop\7755
```

### Step 2: Start the Server
```cmd
python -m uvicorn backend.main:app --reload
```

### Step 3: Wait for Startup Messages
You should see:
```
📁 PictureManager initialized:
   Base path: C:\Users\Administrator\Desktop\7755_clone\Desktop\7755\pictures
   Female path exists: True
   Male path exists: True
✅ Mounted pictures directory: ...
Database initialized successfully
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
```

### Step 4: Test in Browser
- Open browser
- Go to: http://localhost:8000/ui2
- Press `Ctrl + Shift + R` for hard refresh
- You should see the updated page

---

## 🔧 Complete Kill & Restart Script

Save this as `kill_and_restart.bat`:

```batch
@echo off
echo ============================================
echo Killing all Python processes...
echo ============================================
taskkill /F /IM python.exe 2>nul
timeout /t 2

echo.
echo ============================================
echo Checking if port 8000 is free...
echo ============================================
netstat -ano | findstr :8000
if %ERRORLEVEL% EQU 0 (
    echo WARNING: Port 8000 is still in use!
    echo Please close the application using this port.
    pause
    exit /b
)

echo Port 8000 is free!
echo.
echo ============================================
echo Starting server...
echo ============================================
echo.
python -m uvicorn backend.main:app --reload

pause
```

**Usage:**
1. Save the file in your project directory
2. Double-click `kill_and_restart.bat`
3. It will kill all Python processes and restart the server

---

## 🐛 Troubleshooting

### Issue: "Port 8000 is already in use"

**Solution 1: Use different port**
```cmd
python -m uvicorn backend.main:app --reload --port 8080
```
Then access at: http://localhost:8080/ui2

**Solution 2: Kill the process using port 8000**
```cmd
netstat -ano | findstr :8000
taskkill /F /PID <PID_NUMBER>
```

### Issue: Multiple Python processes won't die

**Solution:**
1. Restart your computer
2. This will kill all processes
3. Then start fresh

### Issue: Browser still shows old version

**Solutions:**
1. Clear cache: `Ctrl + Shift + Delete`
2. Hard refresh: `Ctrl + Shift + R`
3. Open incognito/private window
4. Try different browser
5. Add cache-busting: http://localhost:8000/ui2?v=2

---

## 📝 Quick Reference

**Kill all Python:**
```cmd
taskkill /F /IM python.exe
```

**Check port 8000:**
```cmd
netstat -ano | findstr :8000
```

**Start server:**
```cmd
cd C:\Users\Administrator\Desktop\7755_clone\Desktop\7755
python -m uvicorn backend.main:app --reload
```

**Clear browser cache:**
```
Ctrl + Shift + Delete
```

**Hard refresh:**
```
Ctrl + Shift + R
```

---

## ✅ Success Checklist

After following these steps, verify:

- [ ] No Python processes running (Task Manager)
- [ ] Port 8000 is free (netstat command)
- [ ] Old page shows "connection refused"
- [ ] Server starts with new initialization messages
- [ ] Browser shows updated page after hard refresh
- [ ] Picture appears in character profile
- [ ] Picture appears in first chat message

---

**Still having issues?** Restart your computer and try again with a fresh start.
