# Python Version Requirement - IMPORTANT

## Problem

The LINE Bot SDK (`line-bot-sdk 3.5.0`) requires `aiohttp==3.8.5`, which **does not support Python 3.12**.

You are currently running **Python 3.12**, which causes dependency conflicts.

## Solution: Use Python 3.11

Your project requires **Python 3.11** (same as production Heroku environment).

---

## How to Install Python 3.11 on Windows

### Option 1: Install Python 3.11 from Microsoft Store (Easiest)

1. Open **Microsoft Store**
2. Search for "Python 3.11"
3. Install **Python 3.11** (not 3.12)
4. Done!

### Option 2: Download from Python.org

1. Go to https://www.python.org/downloads/
2. Download **Python 3.11.9** (latest 3.11 version)
3. Run installer
4. **Check "Add Python 3.11 to PATH"**
5. Install

---

## How to Use Python 3.11 for This Project

### Check Your Python Versions

```bash
# Check Python 3.12 location
py -3.12 --version

# Check Python 3.11 location
py -3.11 --version
```

### Create Virtual Environment with Python 3.11

```bash
# Navigate to your project directory
cd C:\Users\Administrator\Desktop\7755_clone\Desktop\7755

# Create virtual environment with Python 3.11
py -3.11 -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Verify you're using Python 3.11
python --version
# Should show: Python 3.11.x

# Now install dependencies
pip install -r requirements.txt
```

---

## Why Python 3.11?

1. **LINE Bot SDK compatibility** - line-bot-sdk 3.5.0 requires aiohttp 3.8.5
2. **aiohttp 3.8.5 only supports Python ≤ 3.11**
3. **Matches production** - Your Heroku deployment uses Python 3.11.6 (runtime.txt)
4. **Stability** - Python 3.11 is the stable choice for this project

---

## Quick Setup Commands

```bash
# 1. Install Python 3.11 (if not installed)
#    Use Microsoft Store or python.org

# 2. Create virtual environment
py -3.11 -m venv venv

# 3. Activate virtual environment
venv\Scripts\activate

# 4. Upgrade pip
python -m pip install --upgrade pip

# 5. Install dependencies
pip install -r requirements.txt

# 6. Initialize database
python backend/database.py

# 7. Start server
python backend/main.py
```

---

## Verification Checklist

After following the steps above:

- [ ] `python --version` shows Python 3.11.x
- [ ] `pip install -r requirements.txt` completes successfully
- [ ] No aiohttp or line-bot-sdk errors
- [ ] Server starts: `python backend/main.py`
- [ ] Can access: http://localhost:8000/health

---

## Future Note

When deploying to Heroku, it will automatically use Python 3.11.6 as specified in `runtime.txt`.

Your local environment now matches production! ✅
