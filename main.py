"""
VTU Internship Diary Automation -- Main Orchestrator

Decides which dates need entries, drives the browser bot, and tracks state.
Works with any domain, flexible docx files, and supports automatic backfill.

Usage:
    python main.py                  # normal daily run (today only, or catchup)
    python main.py --backfill       # fill all pending entries up to today
    python main.py --backfill --start 2026-10-06 --end 2026-11-03
    python main.py --date 2026-10-15  # fill a specific date
    python main.py --status         # show completion status
"""

import argparse
import asyncio
import os
import subprocess
import sys
import time
import traceback
from datetime import date, datetime, timedelta

from config import (
    DOCX_FILE,
    STATE_FILE,
    STARTUP_WAIT_SECS,
    MAX_RETRIES,
    RETRY_BACKOFF_SECS,
    ensure_dirs,
    load_credentials,
)
from docx_parser import parse_diary, get_entry_for_date
from state_manager import StateManager
from browser_bot import DiaryBot
from logger import setup_logger

# Ensure UTF-8 output on Windows console
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

log = setup_logger("main")


def show_notification(title: str, message: str, timeout_secs: int = 5):
    """Show a non-blocking Windows desktop notification."""
    try:
        escaped_title = title.replace("'", "''")
        escaped_msg = message.replace("'", "''")
        cmd = f"powershell -Command \"(New-Object -ComObject Wscript.Shell).Popup('{escaped_msg}', {timeout_secs}, '{escaped_title}', 64)\""
        subprocess.Popen(cmd, shell=True)
    except Exception as e:
        log.debug(f"Could not show desktop notification: {e}")


def compute_target_dates(args, state: StateManager) -> list[date]:
    """Decide which dates need entries."""
    if not os.path.exists(DOCX_FILE):
        log.error(f"Diary document not found: {DOCX_FILE}")
        return []

    all_entries = parse_diary(DOCX_FILE)
    all_dates = sorted(all_entries.keys())

    if args.status:
        _print_status(state, all_dates)
        sys.exit(0)

    if args.date:
        # Single specific date
        target = datetime.strptime(args.date, "%Y-%m-%d").date()
        if state.is_completed(target.isoformat()):
            log.info(f"{target} is already completed. Use --force to redo.")
            if not args.force:
                return []
        if target not in all_entries:
            log.error(f"No diary data found for {target} in the DOCX.")
            return []
        return [target]

    if args.backfill:
        # Determine backfill start and end
        today = date.today()
        start_d = datetime.strptime(args.start, "%Y-%m-%d").date() if args.start else (all_dates[0] if all_dates else today)
        end_d = datetime.strptime(args.end, "%Y-%m-%d").date() if args.end else today

        targets = []
        d = start_d
        while d <= end_d:
            if d in all_entries and not state.is_completed(d.isoformat()):
                targets.append(d)
            d += timedelta(days=1)
        log.info(f"Backfill: {len(targets)} pending entries between {start_d} and {end_d}")
        return targets

    # Default daily run
    today = date.today()
    if today not in all_entries:
        log.info(f"No diary data for today ({today}). Checking for earlier pending dates...")
        # Check if there are any pending dates before today
        past_pending = [d for d in all_dates if d <= today and not state.is_completed(d.isoformat())]
        if past_pending:
            log.info(f"Found {len(past_pending)} pending past entries. Processing earliest: {past_pending[0]}")
            return [past_pending[0]]
        log.info("All past and current entries are completed.")
        return []

    if state.is_completed(today.isoformat()):
        log.info(f"Today's entry ({today}) is already completed.")
        return []

    return [today]


def _print_status(state: StateManager, all_dates: list[date]):
    """Print a summary of completed / pending entries."""
    progress = state.get_progress()
    completed = set(state.state["completed_entries"].keys())
    total = len(all_dates)
    done = len(completed)

    print(f"\n{'='*50}")
    print(f"  VTU Diary Automation - Status")
    print(f"{'='*50}")
    print(f"  Total diary days : {total}")
    print(f"  Completed        : {done}")
    print(f"  Remaining        : {total - done}")
    print(f"  Last run         : {progress['last_run'] or 'Never'}")
    print(f"  In progress      : {progress['in_progress'] or 'None'}")

    today = date.today()
    pending = [d for d in all_dates if d <= today and d.isoformat() not in completed]
    if pending:
        print(f"\n  Pending entries up to today ({len(pending)} total):")
        for pd in pending[:10]:
            print(f"    - {pd.strftime('%d %b %Y (%A)')}")
        if len(pending) > 10:
            print(f"    ... and {len(pending) - 10} more.")

    if state.state["failed_entries"]:
        print(f"\n  Failed entries:")
        for date_str, failures in state.state["failed_entries"].items():
            print(f"    - {date_str}: {len(failures)} attempt(s), "
                  f"last error: {failures[-1]['error'][:80]}")

    print(f"{'='*50}\n")


async def run_automation(target_dates: list[date], state: StateManager, headless: bool = False):
    """Run the browser automation for all target dates."""
    creds = load_credentials()
    all_entries = parse_diary(DOCX_FILE)

    bot = DiaryBot(credentials=creds, headless=headless)

    try:
        await bot.start()
        await bot.login()
        await bot.handle_popup()
        await bot.navigate_to_diary()
        await bot.select_internship()

        for i, target_date in enumerate(target_dates, 1):
            date_str = target_date.isoformat()
            entry = all_entries[target_date]

            log.info(f"\n[{i}/{len(target_dates)}] Processing {target_date.strftime('%d %b %Y')} "
                     f"(Day {entry['day_number']})...")

            state.mark_in_progress(date_str)

            success = False
            last_error = None

            for attempt in range(1, MAX_RETRIES + 1):
                try:
                    screenshot_path = await bot.do_single_entry(entry)
                    state.mark_completed(date_str, screenshot_path)
                    log.info(f"[OK] Day {entry['day_number']} completed (attempt {attempt}/{MAX_RETRIES})")
                    success = True

                    # Notify user of successful submission
                    show_notification(
                        "VTU Diary Automation",
                        f"Day {entry['day_number']} ({target_date.strftime('%d %b')}) entry saved successfully!"
                    )
                    break
                except Exception as exc:
                    last_error = str(exc)
                    log.error(f"Attempt {attempt}/{MAX_RETRIES} failed for {target_date}: {exc}")
                    if attempt < MAX_RETRIES:
                        wait = RETRY_BACKOFF_SECS * (2 ** (attempt - 1))
                        log.info(f"Retrying in {wait}s...")
                        await asyncio.sleep(wait)
                        try:
                            await bot.navigate_to_diary()
                            await bot.select_internship()
                        except Exception:
                            log.warning("Could not re-navigate - will retry from current state")

            if not success:
                state.mark_failed(date_str, last_error)
                log.error(f"[FAIL] Day {entry['day_number']} FAILED after {MAX_RETRIES} attempts")

            if i < len(target_dates):
                log.info("Waiting 3s before next entry...")
                await asyncio.sleep(3)

    except Exception as exc:
        log.error(f"Fatal error: {exc}")
        log.debug(traceback.format_exc())
        state.clear_in_progress()
        raise
    finally:
        await bot.close()

    completed = sum(1 for d in target_dates if state.is_completed(d.isoformat()))
    failed = len(target_dates) - completed
    log.info(f"\n{'='*50}")
    log.info(f"  Run complete: {completed} succeeded, {failed} failed out of {len(target_dates)} entries")
    log.info(f"{'='*50}")


def main():
    parser = argparse.ArgumentParser(description="VTU Internship Diary Automation")
    parser.add_argument("--backfill", action="store_true",
                        help="Fill all pending entries up to today")
    parser.add_argument("--start", type=str,
                        help="Optional start date for backfill (YYYY-MM-DD)")
    parser.add_argument("--end", type=str,
                        help="Optional end date for backfill (YYYY-MM-DD)")
    parser.add_argument("--date", type=str,
                        help="Fill a specific date (YYYY-MM-DD format)")
    parser.add_argument("--status", action="store_true",
                        help="Show completion status and exit")
    parser.add_argument("--force", action="store_true",
                        help="Re-do entries even if already completed")
    parser.add_argument("--headless", action="store_true",
                        help="Run browser in headless mode")
    parser.add_argument("--wait", type=int, default=0,
                        help="Seconds to wait before starting")
    args = parser.parse_args()

    ensure_dirs()
    state = StateManager(STATE_FILE)

    if args.wait > 0:
        log.info(f"Waiting {args.wait}s for system startup...")
        time.sleep(args.wait)

    target_dates = compute_target_dates(args, state)

    if not target_dates:
        log.info("No entries to fill. Exiting.")
        return

    log.info(f"Target dates ({len(target_dates)}):")
    for d in target_dates:
        log.info(f"  {d.strftime('%d %b %Y (%A)')}")

    asyncio.run(run_automation(target_dates, state, headless=args.headless))


if __name__ == "__main__":
    main()
