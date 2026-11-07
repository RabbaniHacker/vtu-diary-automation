@echo off
REM =============================================================
REM  VTU Diary Automation - Full Setup
REM  Installs everything and launches the interactive start menu.
REM =============================================================

cd /d "%~dp0"

echo ===================================================
echo   VTU Internship Diary Automation - Full Setup
echo ===================================================
echo.

REM 1. Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in your system PATH!
    echo Please install Python 3.10+ from: https://www.python.org/downloads/
    echo IMPORTANT: Check the box "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

REM 2. Install requirements
echo [*] Installing required Python libraries...
python -m pip install --quiet playwright>=1.40.0 python-docx>=1.1.0
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install requirements. Check your internet connection.
    pause
    exit /b 1
)

REM 3. Install Playwright browser
echo [*] Installing Chromium browser engine...
python -m playwright install chromium

echo.
echo [OK] All dependencies installed successfully!
echo.

REM 4. Launch the interactive start menu
python setup_wizard.py --interactive-start

pause
