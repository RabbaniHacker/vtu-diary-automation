@echo off
REM =============================================================
REM  Backfill pending diary entries
REM  Runs to catch up on any missed past entries up to today.
REM =============================================================

cd /d "%~dp0"

echo ===================================================
echo   VTU Diary - Backfill Pending Entries
echo ===================================================
echo.
echo This will fill all pending diary entries up to today.
echo The browser will open and fill each entry one by one.
echo.
pause

python main.py --backfill

echo.
echo Done! Check screenshots/ folder for verification.
pause
