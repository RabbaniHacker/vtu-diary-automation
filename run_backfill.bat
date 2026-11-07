@echo off
REM =============================================================
REM  Backfill pending diary entries
REM  Auto-installs dependencies if missing.
REM =============================================================

cd /d "%~dp0"

echo ===================================================
echo   VTU Diary - Backfill Pending Entries
echo ===================================================
echo.

REM Auto-install dependencies if missing
python -c "import playwright; import docx" >nul 2>&1
if %errorlevel% neq 0 (
    echo [*] First run detected. Installing dependencies...
    python -m pip install --quiet playwright>=1.40.0 python-docx>=1.1.0
    python -m playwright install chromium
    echo [OK] Dependencies installed.
    echo.
)

echo Enter the start date from which your entries are pending.
echo Formats accepted: DD/MM/YYYY or DD/M/YY (e.g. 24/09/2026 or 24/9/26)
echo.
set /p START_DATE="Enter pending start date (Press Enter to backfill all past dates): "
echo.

if not "%START_DATE%"=="" (
    echo [*] Starting backfill from %START_DATE% up to today...
    python main.py --backfill --start %START_DATE%
) else (
    echo [*] Starting backfill for all uncompleted dates up to today...
    python main.py --backfill
)

echo.
echo ===================================================
echo   Backfill Complete! Check screenshots/ folder.
echo ===================================================
pause
