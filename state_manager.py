"""
Persistent state tracker for diary entries.

Stores completed/failed entries in state.json so the automation can:
  * resume after a crash or laptop shutdown
  * skip dates that were already submitted
  * report progress
"""

import json
import os
from datetime import date, datetime
from typing import List, Optional


class StateManager:
    """Read/write state.json with completed and failed entry records."""

    def __init__(self, state_file: str):
        self.state_file = state_file
        self.state = self._load()

    # -- persistence ------------------------------------------
    def _load(self) -> dict:
        if os.path.exists(self.state_file):
            with open(self.state_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {
            "completed_entries": {},   # "YYYY-MM-DD" -> { completed_at, screenshot }
            "failed_entries": {},      # "YYYY-MM-DD" -> [ { failed_at, error } ]
            "last_run": None,
            "total_completed": 0,
            "in_progress": None,       # date string of entry currently being filled
        }

    def save(self):
        with open(self.state_file, "w", encoding="utf-8") as f:
            json.dump(self.state, f, indent=2, default=str)

    # -- queries ----------------------------------------------
    def is_completed(self, date_str: str) -> bool:
        return date_str in self.state["completed_entries"]

    def get_pending(self, all_date_strs: List[str]) -> List[str]:
        """Return date strings that are not yet completed."""
        return [d for d in all_date_strs if not self.is_completed(d)]

    def get_progress(self) -> dict:
        return {
            "completed": self.state["total_completed"],
            "last_run": self.state["last_run"],
            "in_progress": self.state["in_progress"],
        }

    # -- mutations --------------------------------------------
    def mark_in_progress(self, date_str: str):
        self.state["in_progress"] = date_str
        self.save()

    def mark_completed(self, date_str: str, screenshot_path: Optional[str] = None):
        self.state["completed_entries"][date_str] = {
            "completed_at": datetime.now().isoformat(),
            "screenshot": screenshot_path,
        }
        self.state["total_completed"] = len(self.state["completed_entries"])
        self.state["last_run"] = datetime.now().isoformat()
        self.state["in_progress"] = None
        self.save()

    def mark_failed(self, date_str: str, error_msg: str):
        fails = self.state["failed_entries"].setdefault(date_str, [])
        fails.append({
            "failed_at": datetime.now().isoformat(),
            "error": str(error_msg)[:500],
        })
        self.state["in_progress"] = None
        self.save()

    def clear_in_progress(self):
        self.state["in_progress"] = None
        self.save()

