@echo off
REM =============================================================
REM  VTU Diary Automation - START HERE
REM  This is the ONLY file new users need to double-click.
REM  It handles everything: install, credentials, and running.
REM =============================================================

cd /d "%~dp0"

echo.
echo  ====================================================
echo   VTU Internship Diary Automation
echo   https://github.com/RabbaniHacker/vtu-diary-automation
echo  ====================================================
echo.

REM ---- Step 1: Check Python ----
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo  [ERROR] Python is not installed!
    echo.
    echo  Please install Python 3.10+ from: https://www.python.org/downloads/
    echo  IMPORTANT: Check the box "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)
echo  [OK] Python found.

REM ---- Step 2: Auto-install libraries if missing ----
python -c "import playwright; import docx" >nul 2>&1
if %errorlevel% neq 0 (
    echo  [*] Installing required libraries...
    python -m pip install --quiet playwright>=1.40.0 python-docx>=1.1.0
    if %errorlevel% neq 0 (
        echo  [ERROR] Failed to install libraries. Check your internet connection.
        pause
        exit /b 1
    )
    echo  [*] Installing Chromium browser engine...
    python -m playwright install chromium
    echo  [OK] All dependencies installed.
) else (
    echo  [OK] Libraries already installed.
)
echo.

REM ---- Step 3: Setup credentials + docx check + menu ----
python setup_wizard.py --interactive-start

pause
