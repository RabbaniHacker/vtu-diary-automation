@echo off
REM =============================================================
REM  VTU Diary Automation - Scheduler Setup
REM  Creates a Windows Task Scheduler task that triggers on logon
REM  AND repeats every 15 minutes completely silently in background.
REM  Auto-elevates to Administrator if not already elevated.
REM =============================================================

:: Check for Administrator privileges
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo Requesting Administrator privileges...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

echo ===================================================
echo   VTU Diary Automation - Task Scheduler Setup
echo ===================================================
echo.

cd /d "%~dp0"

powershell -ExecutionPolicy Bypass -File "%~dp0register_task.ps1"

if %errorlevel% equ 0 (
    echo.
    echo [OK] Task "VTU_Diary_Automation" successfully configured!
    echo   - Runs on Windows Logon and laptop wake
    echo   - Retries every 15 minutes silently with zero popups
    echo   - Catches Wi-Fi connection automatically whenever laptop is opened
    echo   - Once today's entry is completed, subsequent checks exit in 0.05s
    echo.
) else (
    echo.
    echo [FAIL] Could not register scheduled task.
    echo.
)

pause
