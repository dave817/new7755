@echo off
echo ============================================
echo Force Kill ALL Processes on Port 8000
echo ============================================
echo.

echo Finding processes on port 8000...
echo.

REM Find all PIDs using port 8000 and kill them
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000 ^| findstr LISTENING') do (
    echo Killing PID: %%a
    taskkill /F /PID %%a 2>nul
    if errorlevel 1 (
        echo   Failed to kill %%a - may need Administrator rights
    ) else (
        echo   Successfully killed %%a
    )
)

echo.
echo Waiting 2 seconds...
timeout /t 2 >nul

echo.
echo Verifying port 8000 is free...
netstat -ano | findstr :8000 >nul
if %ERRORLEVEL% EQU 0 (
    echo.
    echo ❌ WARNING: Port 8000 still in use!
    echo.
    netstat -ano | findstr :8000
    echo.
    echo Try running this script as Administrator:
    echo Right-click on force_kill_port_8000.bat -^> Run as administrator
) else (
    echo.
    echo ✅ SUCCESS! Port 8000 is now free!
)

echo.
echo ============================================
pause
