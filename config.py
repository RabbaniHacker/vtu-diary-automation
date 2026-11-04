"""
Configuration for VTU Internship Diary Automation.
All paths, constants, and credential loading live here.
Designed to be modular, shareable, and adaptable to any student domain.
"""

import json
import os
import sys

# ------------------------ paths ------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CREDENTIALS_FILE = os.path.join(BASE_DIR, "credentials.json")
STATE_FILE = os.path.join(BASE_DIR, "state.json")
SCREENSHOTS_DIR = os.path.join(BASE_DIR, "screenshots")
LOGS_DIR = os.path.join(BASE_DIR, "logs")

def find_docx_file() -> str:
    """
    Find the diary docx file automatically.
    Prioritizes 'diary_data.docx', then any file with 'diary' in name,
    or falls back to the first .docx file in the folder.
    """
    default_name = os.path.join(BASE_DIR, "diary_data.docx")
    if os.path.exists(default_name):
        return default_name

    candidates = [
        f for f in os.listdir(BASE_DIR)
        if f.lower().endswith(".docx") and not f.startswith("~$")
    ]
    if candidates:
        diary_candidates = [f for f in candidates if "diary" in f.lower()]
        chosen = diary_candidates[0] if diary_candidates else candidates[0]
        return os.path.join(BASE_DIR, chosen)

    return default_name

DOCX_FILE = find_docx_file()

# ------------------------ portal -----------------------
PORTAL_URL = "https://vtu.internyet.in/sign-in"
DEFAULT_WORK_HOURS = "5.5"

# ------------------------ timing -----------------------
PAGE_TIMEOUT_MS = 60_000                 # 60 s page-level timeout
NAV_TIMEOUT_MS = 30_000                  # 30 s for navigations
ACTION_DELAY_MS = 800                    # delay between actions for reliability
SLOW_MO_MS = 300                         # Playwright slow-mo
STARTUP_WAIT_SECS = 30                   # wait after OS login for network

# ------------------------ retry ------------------------
MAX_RETRIES = 3
RETRY_BACKOFF_SECS = 5                   # first retry after 5 s, then 10, 20...


# ------------------------ helpers ----------------------
def ensure_dirs():
    """Create output directories if they don't exist."""
    os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
    os.makedirs(LOGS_DIR, exist_ok=True)


def load_credentials() -> dict:
    """Load portal credentials and optional settings from credentials.json."""
    if not os.path.exists(CREDENTIALS_FILE):
        template = {
            "user_id": "YOUR_VTU_EMAIL_OR_ID_HERE",
            "password": "YOUR_PORTAL_PASSWORD_HERE",
            "internship_keyword": "auto",
            "work_hours": "5.5"
        }
        with open(CREDENTIALS_FILE, "w", encoding="utf-8") as f:
            json.dump(template, f, indent=2)
        print(f"[!] Created {CREDENTIALS_FILE} -- please fill in your credentials and re-run.")
        sys.exit(1)

    with open(CREDENTIALS_FILE, "r", encoding="utf-8") as f:
        creds = json.load(f)

    if creds.get("user_id", "").startswith("YOUR_"):
        print(f"[!] Please fill in your real credentials in {CREDENTIALS_FILE}")
        sys.exit(1)

    # Defaults
    if "work_hours" not in creds:
        creds["work_hours"] = DEFAULT_WORK_HOURS
    if "internship_keyword" not in creds:
        creds["internship_keyword"] = "auto"

    return creds
