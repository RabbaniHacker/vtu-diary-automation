"""
Interactive Setup Wizard for VTU Diary Automation.
Guides friends and new users through setting up credentials, docx file, and initial backfill.
"""

import json
import os
import sys
import glob

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CREDS_FILE = os.path.join(BASE_DIR, "credentials.json")


def run_wizard():
    print("\n" + "=" * 55)
    print("   VTU Internship Diary Automation - Setup Wizard")
    print("=" * 55 + "\n")

    # 1. Credentials Setup
    if os.path.exists(CREDS_FILE):
        try:
            with open(CREDS_FILE, "r", encoding="utf-8") as f:
                existing = json.load(f)
            user_id = existing.get("user_id", "")
            print(f"[*] Found existing credentials for: {user_id}")
            reconf = input("Do you want to re-enter credentials? (y/N): ").strip().lower()
            if reconf != "y":
                creds = existing
            else:
                creds = prompt_credentials()
        except Exception:
            creds = prompt_credentials()
    else:
        creds = prompt_credentials()

    with open(CREDS_FILE, "w", encoding="utf-8") as f:
        json.dump(creds, f, indent=2)
    print("[OK] Credentials saved to credentials.json\n")

    # 2. Check for DOCX file
    docx_files = [f for f in glob.glob(os.path.join(BASE_DIR, "*.docx")) if not os.path.basename(f).startswith("~$")]
    if not docx_files:
        print("[!] NOTICE: No .docx file found in this folder!")
        print("    Please copy your VTU Internship Diary (.docx) file into:")
        print(f"    {BASE_DIR}\n")
    else:
        print(f"[OK] Found diary document: {os.path.basename(docx_files[0])}\n")

    print("Setup configuration is complete!")


def prompt_credentials() -> dict:
    print("--- 1. Enter Your VTU Portal Credentials ---")
    user_id = input("VTU InternYet Email / User ID: ").strip()
    while not user_id:
        user_id = input("Email cannot be empty. Enter Email: ").strip()

    password = input("VTU Portal Password: ").strip()
    while not password:
        password = input("Password cannot be empty. Enter Password: ").strip()

    print("\n--- 2. Domain / Internship Name ---")
    print("Examples: 'Web Development', 'Artificial Intelligence', 'Data Science', 'Cloud'")
    domain = input("Internship Name (Press Enter to auto-detect): ").strip()
    if not domain:
        domain = "auto"

    work_hours = input("Daily Work Hours [Default: 5.5]: ").strip()
    if not work_hours:
        work_hours = "5.5"

    return {
        "user_id": user_id,
        "password": password,
        "internship_keyword": domain,
        "work_hours": work_hours
    }


if __name__ == "__main__":
    run_wizard()

