# VTU Internship Diary Automation

An intelligent, silent background automation bot for the **VTU Internship Portal** (`https://vtu.internyet.in/`). 

Designed to be universal, modular, and shareable with friends across **any internship domain** (Web Development, Artificial Intelligence, Data Science, Machine Learning, Cyber Security, Cloud Computing, etc.).

---

## Key Features

- **Any Domain / Internship**: Automatically detects your enrolled internship or selects your specific domain (Web Dev, AI, Cyber Security, etc.).
- **Drop-in DOCX Parser**: Drop **any** VTU Diary `.docx` file into the folder; the bot parses all days, work summaries, learnings, reference links, blockers, and skills automatically.
- **Fixed 5.5 Hours**: Enforces 5.5 hours per day as required by VTU guidelines.
- **Intelligent Skill Selection**: Selects skills one-by-one from the portal dropdown with automatic fallback so the Save button is always enabled.
- **Silent Background Execution**: Runs headless in the background via Windows Task Scheduler. No command prompt popups or browser windows interrupt your work.
- **Wi-Fi Catch-Up**: If your laptop turns on without Wi-Fi and connects hours later (e.g., opened at 5 AM offline, Wi-Fi connected at 5 PM), the bot automatically detects internet and submits your diary.
- **Zero Resource Consumption**: After today's entry is completed, background checks exit in 0.05 seconds with 0% CPU, 0% Wi-Fi, and 0 browser activity.
- **Automated Verification & Screenshots**: Verifies each submission on the portal entries table and saves full-page screenshots as `screenshots/DDMMYY.png`.
- **Desktop Notifications**: Displays a native Windows notification whenever an entry is completed.
- **Smart Memory (`state.json`)**: Remembers what was submitted. If your laptop shuts down mid-run, it picks up right where it left off without duplicate submissions.

---

## Quick Start (For You & Friends)

### Step 1: Clone or Download the Repository
```bash
git clone https://github.com/YOUR_USERNAME/vtu-diary-automation.git
cd vtu-diary-automation
```

### Step 2: Add Your Diary Word File
Copy your VTU Internship Diary Word file (`.docx`) into the project folder. You can name it anything (e.g. `diary_data.docx` or `VTU_AI_Internship_Diary.docx`).

### Step 3: Run the One-Click Setup
Double-click **`setup.bat`**:
1. Automatically installs Python dependencies (`playwright`, `python-docx`).
2. Downloads the Chromium automation engine.
3. Asks for your VTU portal Email, Password, and Internship Domain (or press Enter for auto-detect).
4. Asks if you want to backfill any missed past dates right now.
5. Configures the silent 15-minute background Task Scheduler!

*That's it! Your diary entries are now fully automated.*

---

## Manual / Advanced CLI Usage

| Command | Purpose |
| :--- | :--- |
| `python main.py` | Submits today's entry (or earliest pending past entry). |
| `python main.py --headless` | Runs silently in the background without opening the browser. |
| `python main.py --backfill` | Backfills all uncompleted entries up to today. |
| `python main.py --backfill --start 2026-10-06 --end 2026-11-03` | Backfills a specific date range. |
| `python main.py --date 2026-10-15` | Submits a single specific date. |
| `python main.py --date 2026-10-15 --force` | Re-does a date even if marked completed in `state.json`. |
| `python main.py --status` | Displays total completed, remaining, and failed entries. |

---

## File Structure

```text
├── config.py                 # Auto-detects docx, loads credentials & settings
├── docx_parser.py            # Universal multi-format .docx diary parser
├── browser_bot.py            # Playwright automation engine (all domains)
├── state_manager.py          # Persistent JSON tracker (state.json)
├── main.py                   # Orchestrator & CLI runner
├── setup.bat                 # One-click interactive setup for friends
├── setup_wizard.py           # CLI credential & docx configurator
├── setup_scheduler.bat       # Auto-elevating Windows Task Scheduler installer
├── register_task.ps1         # Registers logon + 15-minute repeat trigger
├── launcher.bat              # Smart launcher: checks state -> checks Wi-Fi -> runs
├── launcher.vbs              # 100% silent background runner (0 cmd flicker)
├── run_backfill.bat          # One-click backfill runner
├── credentials.example.json  # Template for login credentials
├── requirements.txt          # Python dependencies
├── .gitignore                # Protects credentials, screenshots, and docx
├── screenshots/              # Saved verification screenshots (DDMMYY.png)
└── logs/                     # Daily timestamped execution logs
```

---

## Privacy & Security

Your `.gitignore` is pre-configured to ensure that:
- `credentials.json` (your password and email) is **never** pushed to GitHub.
- `state.json`, `screenshots/`, and `*.docx` remain private to your local machine.
