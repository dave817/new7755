@echo off
echo ============================================
echo Step 1: Killing all Python processes...
echo ============================================
taskkill /F /IM python.exe 2>nul
if %ERRORLEVEL% EQU 0 (
    echo ✓ Python processes killed successfully!
) else (
    echo ℹ No Python processes found running.
)

echo.
echo Waiting 2 seconds...
timeout /t 2 >nul

echo.
echo ============================================
echo Step 2: Killing all processes on port 8000...
echo ============================================

REM Find and kill ALL processes using port 8000
set FOUND=0
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000 ^| findstr LISTENING') do (
    set FOUND=1
    echo Killing PID: %%a
    taskkill /F /PID %%a 2>nul
)

if %FOUND%==0 (
    echo ℹ No processes found on port 8000
) else (
    echo ✓ Killed all processes on port 8000
)

echo.
echo Waiting 3 seconds...
timeout /t 3 >nul

echo.
echo ============================================
echo Step 3: Verifying port 8000 is free...
echo ============================================
netstat -ano | findstr :8000 >nul
if %ERRORLEVEL% EQU 0 (
    echo.
    echo ❌ ERROR: Port 8000 is STILL in use!
    echo.
    netstat -ano | findstr :8000
    echo.
    echo Please run as Administrator:
    echo Right-click this file -^> Run as administrator
    echo.
    pause
    exit /b 1
)

echo ✓ Port 8000 is free!
echo.
echo ============================================
echo Starting Dating Chatbot Server...
echo ============================================
echo.
echo Server will start at: http://localhost:8000
echo Web UI2 available at: http://localhost:8000/ui2
echo.
echo IMPORTANT: After server starts, press Ctrl+Shift+R in browser to hard refresh!
echo.
echo Press Ctrl+C to stop the server
echo ============================================
echo.

python -m uvicorn backend.main:app --reload

pause
