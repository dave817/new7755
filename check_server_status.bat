@echo off
echo ============================================
echo Checking Server Status
echo ============================================
echo.

echo 1. Checking for Python processes...
echo.
tasklist /FI "IMAGENAME eq python.exe" 2>NUL | find /I /N "python.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo ❌ WARNING: Python processes are STILL RUNNING!
    echo.
    tasklist /FI "IMAGENAME eq python.exe"
    echo.
    echo Run kill_server.bat to stop them.
) else (
    echo ✓ No Python processes found
)

echo.
echo 2. Checking if port 8000 is in use...
echo.
netstat -ano | findstr :8000 >NUL
if "%ERRORLEVEL%"=="0" (
    echo ❌ WARNING: Port 8000 is STILL IN USE!
    echo.
    netstat -ano | findstr :8000
    echo.
    echo Something is still running on port 8000!
) else (
    echo ✓ Port 8000 is FREE
)

echo.
echo 3. Testing if server responds...
echo.
curl -s http://localhost:8000/health >NUL 2>&1
if "%ERRORLEVEL%"=="0" (
    echo ❌ WARNING: Server is STILL RESPONDING!
    echo The server is running somewhere!
) else (
    echo ✓ Server is NOT responding (good - it's stopped)
)

echo.
echo ============================================
echo Summary
echo ============================================
echo.
echo If you see any ❌ warnings above, the server is still running.
echo If you see all ✓ checks, the server is completely stopped.
echo.
echo If you can still access the webpage:
echo - Your browser is showing CACHED content
echo - Clear cache: Ctrl+Shift+Delete
echo - Or close ALL browser windows and reopen
echo.
pause
