# VTU Internship Diary Automation

Automatically fills your daily internship diary entries on the [VTU Internship Portal](https://vtu.internyet.in/sign-in). Runs silently in the background every day — zero effort after setup.

Works with **any internship domain**: Web Development, Artificial Intelligence, Data Science, Machine Learning, Cyber Security, Cloud Computing, and more.

---

## How It Works

1. Reads your diary content from your Word (.docx) file
2. Logs into the VTU portal with your credentials
3. Navigates to Internship Diary and selects your internship
4. Picks the correct date, fills Work Summary, Hours (5.5), Reference Links, Learnings, Blockers
5. Selects matching skills one-by-one from the portal dropdown
6. Clicks Save and verifies the entry appeared in the records
7. Takes a verification screenshot saved as `screenshots/DDMMYY.png`

---

## Quick Start (3 Steps)

### Step 1: Download
```bash
git clone https://github.com/RabbaniHacker/vtu-diary-automation.git
cd vtu-diary-automation
```

Or click **Code → Download ZIP** on GitHub and extract it.

### Step 2: Add Your Diary File
Copy your VTU Internship Diary Word file (`.docx`) into the project folder. You can name it anything — the bot auto-detects it.

### Step 3: Run
Double-click **`start.bat`**

That's it! It will:
- ✅ Auto-install Python libraries and Chromium (first time only)
- ✅ Ask for your VTU Email and Password
- ✅ Ask your internship domain (or auto-detect it)
- ✅ Show you a menu to choose what to do:

```
  1. Fill today's diary entry only
  2. Backfill all pending past entries
  3. Backfill from a specific date
  4. Check completion status
  5. Exit
```

> **Note:** You need [Python 3.10+](https://www.python.org/downloads/) installed.
> Make sure to check **"Add Python to PATH"** during installation.

---

## Enable Automatic Daily Mode (Optional)

Want the bot to fill your diary automatically every day without you doing anything?

1. Right-click **`setup_scheduler.bat`** → **Run as Administrator**
2. Click **Yes** on the Windows prompt
3. Done! From now on:
   - Every time you log in or wake your laptop, it silently checks if today's entry is pending
   - If your laptop starts without Wi-Fi and connects later, it catches up automatically
   - Once today's entry is done, background checks exit in 0.05 seconds with zero resource usage
   - You get a desktop notification when your entry is submitted

---

## Requirements

| Requirement | Details |
|:---|:---|
| **OS** | Windows 10 / 11 |
| **Python** | 3.10 or higher ([Download](https://www.python.org/downloads/)) |
| **Internet** | Required during diary submission |
| **Your Diary File** | The `.docx` file provided by Edutainer with daily entries |

All other dependencies (Playwright, python-docx, Chromium) are installed automatically.

---

## Project Structure

```
├── start.bat                 ← START HERE (new users)
├── setup.bat                 ← Alternative: full install + start
├── setup_scheduler.bat       ← Enable daily auto-mode (run as Admin)
├── run_backfill.bat          ← Quick backfill shortcut
│
├── main.py                   # CLI orchestrator
├── browser_bot.py            # Playwright automation engine
├── docx_parser.py            # Universal .docx diary parser
├── config.py                 # Auto-config & credential loader
├── state_manager.py          # Persistent state tracker (state.json)
├── setup_wizard.py           # Interactive setup & menu
├── logger.py                 # File + console logging
│
├── launcher.bat              # Smart launcher for scheduled task
├── launcher.vbs              # Silent background runner
├── register_task.ps1         # Windows Task Scheduler registration
├── requirements.txt          # Python dependencies
├── credentials.example.json  # Template for credentials
│
├── screenshots/              # Verification screenshots (DDMMYY.png)
├── logs/                     # Daily execution logs
└── state.json                # Tracks completed/pending entries
```

---

## CLI Commands (Advanced)

| Command | What it does |
|:---|:---|
| `python main.py` | Fill today's entry (or earliest pending) |
| `python main.py --headless` | Run silently without opening browser |
| `python main.py --backfill` | Fill all pending entries up to today |
| `python main.py --backfill --start 24/09/2026` | Backfill from a specific date |
| `python main.py --date 15/10/2026` | Fill one specific date |
| `python main.py --date 15/10/2026 --force` | Re-do a completed date |
| `python main.py --status` | Show completion summary |

Date formats accepted: `DD/MM/YYYY`, `DD/MM/YY`, `YYYY-MM-DD`

---

## FAQ

**Q: Will this work for AI / Data Science / Cloud internships?**
Yes! The bot auto-detects your enrolled internship on the portal. Skills are mapped for Web Dev, AI, ML, Data Science, Cyber Security, Cloud, and more.

**Q: What if I turn on my laptop without Wi-Fi?**
The bot checks every 15 minutes. As soon as Wi-Fi connects, it submits automatically.

**Q: What if my laptop was off all day?**
When you next turn it on and connect to Wi-Fi, it catches up and fills the missed day.

**Q: Is my password safe?**
Your `credentials.json` is listed in `.gitignore` and will never be pushed to GitHub. It stays only on your local machine.

**Q: Can I change my credentials later?**
Run `start.bat` again — it will ask if you want to change credentials.

---

## Privacy & Security

Your `.gitignore` ensures these files are **never** pushed to GitHub:
- `credentials.json` (email & password)
- `state.json` (completion history)
- `screenshots/` (personal verification images)
- `*.docx` (your diary document)

---

## Credits

Built by [RabbaniHacker](https://github.com/RabbaniHacker)
