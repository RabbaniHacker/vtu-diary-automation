@echo off
REM =============================================================
REM  Backfill pending diary entries
REM =============================================================

cd /d "%~dp0"

echo ===================================================
echo   VTU Diary - Backfill Pending Entries
echo ===================================================
echo.
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
