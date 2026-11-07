# VTU Internship Diary Automation

Automatically fills your daily internship diary entries on the [VTU Internship Portal](https://vtu.internyet.in/sign-in). Runs silently in the background every day — zero effort after setup.

Works with **any internship domain**: Web Development, Artificial Intelligence, Data Science, Machine Learning, Cyber Security, Cloud Computing, and more.

---

## How It Works

1. Reads your diary content from your Word (.docx) file
2. Logs into the VTU portal with your credentials
3. Navigates to Internship Diary and selects your internship
4. Picks the correct date, fills Work Summary, Hours (configurable, default 5.5), Reference Links, Learnings, Blockers
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

### Step 2: Add Your Diary File (Or Generate One)
- **Already have a Word file?** Copy your `.docx` file into the folder (any name works).
- **Don't have a file?**
  - **Option A (Instant Built-in Generator)**: Run `python generate_diary.py` to generate a complete diary for AI, Data Science, Cyber Security, Cloud, Python, etc. in 5 seconds!
  - **Option B (Use Claude / ChatGPT)**: Copy the ready-made prompt from [PROMPT_TEMPLATE.md](PROMPT_TEMPLATE.md) into [Claude](https://claude.ai) or ChatGPT to generate your exact custom diary.
  - **Option C (Sample Template)**: A complete 110-day reference is included as [`sample_diary_template.docx`](sample_diary_template.docx).

### Step 3: Run
Double-click **`start.bat`**

That's it! It will:
- ✅ Auto-install Python libraries and Chromium (first time only)
- ✅ Ask for your VTU Email and Password
- ✅ Ask your internship domain (or auto-detect it)
- ✅ Ask your daily work hours (default: 5.5, or enter any hours you need)
- ✅ Show you a menu to choose what to do:

```
  1. Fill today's diary entry only
  2. Backfill all pending past entries
  3. Backfill from a specific date
  4. Check completion status
  5. Change Settings (Work Hours, Domain, Credentials)
  6. Exit
```

> **Note:** You need [Python 3.10+](https://www.python.org/downloads/) installed.
> Make sure to check **"Add Python to PATH"** during installation.

---

## 📝 Generating a Custom Diary for Any Domain / Company

If your internship is from another company (Infosys, Internshala, Rooman, Oasis Infobyte, Cisco, TCS, etc.) or a different domain (AI/ML, Data Science, Cyber Security, Cloud, Python, Java), you can create your `.docx` file easily:

### Method 1: The Master AI Prompt (Claude / ChatGPT)
Copy this prompt into [Claude](https://claude.ai) or [ChatGPT](https://chatgpt.com) and replace the bracketed values:

```text
You are an expert technical curriculum designer. Generate a complete, realistic, day-by-day VTU Internship Daily Diary for my university internship submission.

My Details:
- Domain: [e.g. Artificial Intelligence & Machine Learning / Cyber Security / Web Dev]
- Company: [e.g. Infosys Springboard / Internshala / Rooman / Oasis Infobyte]
- Start Date: [e.g. 03 August 2026]
- Total Days: [e.g. 110 days or 60 days or 30 days]
- Daily Work Hours: [e.g. 5.5]
- Reference Link: [e.g. https://springboard.infosys.com or https://vtu.internyet.in]

Every day entry MUST follow this exact format:
Day [N] -- [DD Month YYYY]
Internship: [Domain] -- [Company]
Work Summary: [1-2 sentences of technical tasks completed]
Hours Worked: [5.5]
Reference Links: [Reference URL]
Learnings / Outcomes: [1-2 sentences on technical concepts learned]
Blockers / Risks: [1 sentence on technical hurdles or 'No major blockers']
Skills Used: [Skill 1], [Skill 2], [Skill 3]

Please generate Day 1 through Day [Total Days] and output as a downloadable .docx file or provide python-docx code to save it.
```
Then ask Claude to give you the `.docx` file (or paste into Word and save as `.docx`). See [PROMPT_TEMPLATE.md](PROMPT_TEMPLATE.md) for full instructions.

### Method 2: Built-in Instant Generator
Don't have an AI account? Run this in your terminal:
```bash
python generate_diary.py
```
Pick your domain (AI/ML, Data Science, Cyber Security, Cloud, Python), enter your company name and start date. It creates a ready-to-use `.docx` file automatically!

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
├── generate_diary.py         ← Instant offline diary generator for any domain
├── PROMPT_TEMPLATE.md        ← Ready-to-copy Claude / ChatGPT prompt
├── sample_diary_template.docx← 110-day reference template (Edutainer Web Dev)
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
| `python main.py --hours 6.5` | Run with custom daily work hours |
| `python main.py --backfill` | Fill all pending entries up to today |
| `python main.py --backfill --start 24/09/2026` | Backfill from a specific date |
| `python main.py --date 15/10/2026` | Fill one specific date |
| `python main.py --date 15/10/2026 --force` | Re-do a completed date |
| `python main.py --status` | Show completion summary |

Date formats accepted: `DD/MM/YYYY`, `DD/MM/YY`, `YYYY-MM-DD`

---

## FAQ

**Q: Can I change my daily work hours from 5.5 to something else?**
Yes! You can set any hours you want:
- In `start.bat` → select **Option 5** (Change Settings) → **1** (Change Work Hours), or
- Pass `--hours 6` or `--hours 6.5` via command line, or
- Edit `"work_hours": "6.0"` in `credentials.json`.

**Q: Will this work for AI / Data Science / Cloud internships?**
Yes! The bot auto-detects your enrolled internship on the portal. Skills are mapped for Web Dev, AI, ML, Data Science, Cyber Security, Cloud, and more.

**Q: What if I turn on my laptop without Wi-Fi?**
The bot checks every 15 minutes. As soon as Wi-Fi connects, it submits automatically.

**Q: What if my laptop was off all day?**
When you next turn it on and connect to Wi-Fi, it catches up and fills the missed day.

**Q: Is my password safe?**
Your `credentials.json` is listed in `.gitignore` and will never be pushed to GitHub. It stays only on your local machine.

**Q: Can I change my credentials or domain later?**
Run `start.bat` and select **Option 5** (Change Settings) to update your hours, domain, or login anytime.

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
