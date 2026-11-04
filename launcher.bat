@echo off
REM =============================================================
REM  VTU Diary Automation - Smart Launcher
REM  1. Checks if today is already completed (exits in 0.05s if done)
REM  2. Checks if internet is connected (exits if offline)
REM  3. Runs headless automation when internet becomes available
REM =============================================================

cd /d "%~dp0"

REM Step 1: Check state.json first. If today is already done, exit immediately.
python -c "from state_manager import StateManager; from datetime import date; import sys; s=StateManager('state.json'); sys.exit(0 if s.is_completed(date.today().isoformat()) else 1)"
if %errorlevel% equ 0 (
    exit /b 0
)

REM Step 2: Check if Internet is available (ping 8.8.8.8)
ping -n 1 8.8.8.8 >nul 2>&1
if %errorlevel% neq 0 (
    echo [%date% %time%] Laptop is offline. Automation will run as soon as Wi-Fi connects.
    exit /b 0
)

REM Step 3: Run the daily entry silently in headless mode
echo [%date% %time%] Internet connected and today's entry is pending. Running automation...
python main.py --headless

echo [%date% %time%] Completed.
