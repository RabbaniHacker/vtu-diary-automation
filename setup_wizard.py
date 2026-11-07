"""
Interactive Setup Wizard for VTU Diary Automation.
Handles credentials setup, docx file detection, and action menu.

Usage:
    python setup_wizard.py                  # Just setup credentials
    python setup_wizard.py --interactive-start  # Full flow: setup + menu + run
"""

import argparse
import json
import glob
import os
import subprocess
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CREDS_FILE = os.path.join(BASE_DIR, "credentials.json")


def prompt_credentials() -> dict:
    """Prompt user for VTU portal credentials interactively."""
    print("  --- Enter Your VTU Portal Credentials ---")
    print()
    user_id = input("  VTU InternYet Email / User ID: ").strip()
    while not user_id:
        user_id = input("  Email cannot be empty. Enter Email: ").strip()

    password = input("  VTU Portal Password: ").strip()
    while not password:
        password = input("  Password cannot be empty. Enter Password: ").strip()

    print()
    print("  --- Internship Domain ---")
    print("  Examples: 'Web Development', 'Artificial Intelligence',")
    print("            'Data Science', 'Cyber Security', 'Cloud Computing'")
    domain = input("  Internship Name (Press Enter to auto-detect): ").strip()
    if not domain:
        domain = "auto"

    work_hours = input("  Daily Work Hours [Default: 5.5]: ").strip()
    if not work_hours:
        work_hours = "5.5"

    return {
        "user_id": user_id,
        "password": password,
        "internship_keyword": domain,
        "work_hours": work_hours
    }


def ensure_credentials() -> dict:
    """Ensure credentials.json exists and has real values. Returns creds dict."""
    needs_setup = False

    if not os.path.exists(CREDS_FILE):
        needs_setup = True
    else:
        try:
            with open(CREDS_FILE, "r", encoding="utf-8") as f:
                creds = json.load(f)
            if creds.get("user_id", "").startswith("YOUR_") or not creds.get("user_id"):
                needs_setup = True
            elif not creds.get("password"):
                needs_setup = True
            else:
                # Credentials exist and look valid
                print(f"  [OK] Credentials found for: {creds['user_id']}")
                change = input("  Want to change credentials? (y/N): ").strip().lower()
                if change == "y":
                    needs_setup = True
                else:
                    # Ensure defaults exist
                    if "work_hours" not in creds:
                        creds["work_hours"] = "5.5"
                    if "internship_keyword" not in creds:
                        creds["internship_keyword"] = "auto"
                    return creds
        except (json.JSONDecodeError, Exception):
            needs_setup = True

    if needs_setup:
        print()
        creds = prompt_credentials()
        with open(CREDS_FILE, "w", encoding="utf-8") as f:
            json.dump(creds, f, indent=2)
        print()
        print(f"  [OK] Credentials saved!")
        print()

    return creds


def check_docx() -> bool:
    """Check if a diary .docx file exists in the project folder."""
    docx_files = [
        f for f in glob.glob(os.path.join(BASE_DIR, "*.docx"))
        if not os.path.basename(f).startswith("~$")
    ]
    if not docx_files:
        print("  [!] No diary .docx file found!")
        print()
        print("  Please copy your VTU Internship Diary Word file (.docx) into:")
        print(f"  {BASE_DIR}")
        print()
        print("  You can name it anything (e.g. diary_data.docx, AI_Diary.docx, etc.)")
        print("  The automation will auto-detect it.")
        print()
        return False
    else:
        print(f"  [OK] Diary document found: {os.path.basename(docx_files[0])}")
        return True


def show_menu_and_run():
    """Show the action menu and run the selected option."""
    print()
    print("  ====================================================")
    print("  What would you like to do?")
    print("  ====================================================")
    print()
    print("  1. Fill today's diary entry only")
    print("  2. Backfill all pending past entries")
    print("  3. Backfill from a specific date")
    print("  4. Check completion status")
    print("  5. Exit")
    print()

    choice = input("  Enter your choice (1-5): ").strip()
    print()

    if choice == "1":
        print("  [*] Running today's entry...")
        print("  " + "=" * 50)
        subprocess.call([sys.executable, "main.py"])

    elif choice == "2":
        print("  [*] Backfilling all pending entries up to today...")
        print("  " + "=" * 50)
        subprocess.call([sys.executable, "main.py", "--backfill"])

    elif choice == "3":
        print("  Enter the start date from which entries are pending.")
        print("  Formats: DD/MM/YYYY or DD/M/YY (e.g. 24/09/2026 or 24/9/26)")
        start_date = input("  Pending from date: ").strip()
        if start_date:
            print()
            print(f"  [*] Backfilling from {start_date} to today...")
            print("  " + "=" * 50)
            subprocess.call([sys.executable, "main.py", "--backfill", "--start", start_date])
        else:
            print("  No date entered. Running full backfill...")
            subprocess.call([sys.executable, "main.py", "--backfill"])

    elif choice == "4":
        subprocess.call([sys.executable, "main.py", "--status"])

    elif choice == "5":
        print("  Goodbye!")
        return

    else:
        print("  Invalid choice. Please run start.bat again.")
        return

    print()
    print("  ====================================================")
    print("  Done! Check the screenshots/ folder for verification.")
    print("  ====================================================")
    print()
    print("  TIP: To enable automatic daily silent submissions,")
    print("  right-click 'setup_scheduler.bat' and 'Run as Administrator'.")
    print()


def run_wizard():
    """Original standalone wizard (backward compatible)."""
    print("\n" + "=" * 55)
    print("   VTU Internship Diary Automation - Setup Wizard")
    print("=" * 55 + "\n")

    ensure_credentials()

    if not check_docx():
        return

    print("\nSetup configuration is complete!")


def interactive_start():
    """Full interactive flow called from start.bat."""
    # Step 1: Credentials
    ensure_credentials()
    print()

    # Step 2: Check docx
    if not check_docx():
        return

    print()

    # Step 3: Menu
    show_menu_and_run()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--interactive-start", action="store_true",
                        help="Run the full interactive flow (credentials + docx check + menu)")
    args = parser.parse_args()

    if args.interactive_start:
        interactive_start()
    else:
        run_wizard()
