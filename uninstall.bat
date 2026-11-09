@echo off
REM =============================================================
REM  VTU Diary Automation - Uninstaller
REM  Removes the background Windows Scheduled Task and cleans up.
REM  Auto-elevates to Administrator if needed.
REM =============================================================

:: Check for Administrator privileges
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo Requesting Administrator privileges to remove scheduled task...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

echo ===================================================
echo   VTU Diary Automation - Uninstaller
echo ===================================================
echo.

cd /d "%~dp0"

REM 1. Remove the Windows Scheduled Task
echo [*] Removing Windows Scheduled Task "VTU_Diary_Automation"...
powershell -Command "Unregister-ScheduledTask -TaskName 'VTU_Diary_Automation' -Confirm:$false -ErrorAction SilentlyContinue" >nul 2>&1
schtasks /delete /tn "VTU_Diary_Automation" /f >nul 2>&1

echo [OK] Background automation task removed. It will no longer run.
echo.

REM 2. Optional: Clean up Playwright Chromium browser to free disk space (~400 MB)
set /p CLEAN_BROWSER="Do you want to remove the Playwright Chromium browser to free up ~400 MB? (y/N): "
if /i "%CLEAN_BROWSER%"=="y" (
    echo [*] Removing downloaded Chromium browser...
    python -m playwright uninstall --all >nul 2>&1
    echo [OK] Browser files cleaned up.
)
echo.

echo ===================================================
echo   Uninstallation Complete!
echo ===================================================
echo.
echo You can now safely delete this folder whenever you wish.
echo.
pause
