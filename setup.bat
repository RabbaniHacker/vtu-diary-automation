@echo off
REM =============================================================
REM  VTU Diary Automation - One-Click Setup for Friends & Users
REM =============================================================

cd /d "%~dp0"

echo ===================================================
echo   VTU Internship Diary Automation - Setup
echo ===================================================
echo.

REM 1. Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in your system PATH!
    echo Please install Python 3.10 or higher from python.org
    echo and make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

REM 2. Install requirements
echo [*] Installing required Python libraries...
python -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install requirements. Please check your internet connection.
    pause
    exit /b 1
)

REM 3. Install Playwright browser
echo.
echo [*] Installing Chromium browser for automation...
python -m playwright install chromium

REM 4. Run interactive credentials wizard
echo.
python setup_wizard.py

REM 5. Ask to backfill
echo.
echo ---------------------------------------------------
set /p DO_BACKFILL="Do you have past missing diary entries to backfill right now? (y/N): "
if /i "%DO_BACKFILL%"=="y" (
    echo.
    echo Enter the start date from which your entries are pending.
    echo Formats accepted: DD/MM/YYYY or DD/M/YY (e.g. 24/09/2026 or 24/9/26)
    set /p START_DATE="Enter pending start date (Press Enter for all): "
    echo.
    echo [*] Starting backfill...
    if not "%START_DATE%"=="" (
        python main.py --backfill --start %START_DATE%
    ) else (
        python main.py --backfill
    )
)

REM 6. Ask to register automatic 15-minute background task
echo.
echo ---------------------------------------------------
set /p DO_TASK="Do you want to enable automatic silent daily submission (every 15 mins)? (Y/n): "
if /i not "%DO_TASK%"=="n" (
    echo.
    echo [*] Launching Task Scheduler setup...
    call setup_scheduler.bat
)

echo.
echo ===================================================
echo   Setup Complete! Everything is ready to go.
echo ===================================================
pause
