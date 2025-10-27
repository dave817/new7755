@echo off
echo ============================================
echo Stopping Dating Chatbot Server
echo ============================================
echo.
echo Killing all Python processes...
taskkill /F /IM python.exe 2>nul
if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✓ Python processes killed successfully!
) else (
    echo.
    echo ℹ No Python processes found running.
)

echo.
echo Waiting 2 seconds...
timeout /t 2 >nul

echo.
echo Checking if port 8000 is free...
netstat -ano | findstr :8000 >nul
if %ERRORLEVEL% EQU 0 (
    echo.
    echo WARNING: Port 8000 is still in use!
    echo Attempting to kill process on port 8000...
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000 ^| findstr LISTENING') do (
        echo Killing process ID: %%a
        taskkill /F /PID %%a 2>nul
    )
) else (
    echo.
    echo ✓ Port 8000 is now free!
)

echo.
echo ============================================
echo Server stopped successfully!
echo ============================================
echo.
echo To start the server again, run:
echo   run_server.bat
echo or
echo   kill_and_restart.bat
echo.
pause
