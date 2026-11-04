"""
Playwright-based browser automation for the VTU Internship Diary portal.
Supports any student domain (Web Dev, AI, Cyber Security, Cloud, Data Science, etc.).

Portal workflow:
  1. Login at https://vtu.internyet.in/sign-in
  2. Dismiss disclaimer popup ("I understand")
  3. Navigate to Internship Diary (https://vtu.internyet.in/dashboard/student/student-diary)
  4. Select internship (auto-detects or matches configured domain)
  5. Open entry form:
       a. Click "Pick a Date"
       b. Navigate calendar to target month & click target day
       c. Click "Continue" -> navigates to /dashboard/student/create-diary-entry
  6. Fill fields:
       - Work Summary: textarea[name="description"]
       - Work Hours: input[type="number"] (configurable, defaults to 5.5)
       - Reference Links: textarea[name="links"]
       - Learnings / Outcomes: textarea[name="learnings"]
       - Blockers / Risks: textarea[name="blockers"]
  7. Skills Used: react-select multi-select (selected one-by-one, with auto-fallback)
  8. Click Save: button:has-text("Save")[type="submit"]
  9. Verify entry at https://vtu.internyet.in/dashboard/student/diary-entries
 10. Take full-page screenshot -> screenshots/DDMMYY.png
"""

import asyncio
from datetime import date, datetime
import os
import re
import sys
from typing import List, Optional

from playwright.async_api import (
    async_playwright,
    Browser,
    BrowserContext,
    Page,
    TimeoutError as PlaywrightTimeout,
    Locator,
)

from config import (
    PORTAL_URL,
    DEFAULT_WORK_HOURS,
    SCREENSHOTS_DIR,
    PAGE_TIMEOUT_MS,
    NAV_TIMEOUT_MS,
    ACTION_DELAY_MS,
    SLOW_MO_MS,
    ensure_dirs,
)
from logger import setup_logger

log = setup_logger("browser_bot")

# Comprehensive mapping of skills from various internship documents to exact VTU portal names
SKILL_MAP = {
    # Web Development
    "react": "React.js",
    "react.js": "React.js",
    "javascript": "Java Script",
    "java script": "Java Script",
    "js": "Java Script",
    "typescript": "TypeScript",
    "type script": "TypeScript",
    "html": "HTML",
    "semantic html": "HTML",
    "css": "CSS",
    "css selectors": "CSS",
    "box model": "CSS",
    "flexbox": "CSS",
    "grid": "CSS",
    "media queries": "CSS",
    "responsive design": "CSS",
    "layout": "Layout Design",
    "layout design": "Layout Design",
    "web design": "Layout Design",
    "ui design": "UX design",
    "user experience": "UX design",
    "user interface": "UX design",
    "git": "Git",
    "github": "Git",
    "version control": "Git",
    "branching": "Git",
    "node.js": "Node.js",
    "nodejs": "Node.js",
    "npm": "Node.js",
    "express": "Node.js",
    "mongodb": "MongoDB",
    "database": "Database design",
    "database design": "Database design",
    "data modeling": "Data modeling",
    "crud": "Database design",
    "api": "API",
    "rest api": "API",
    "restful api": "API",
    "testing": "Software Testing",
    "software testing": "Software Testing",
    "unit testing": "Software Testing",
    "qa": "Verification & Validations",
    "quality assurance": "Verification & Validations",
    "validation": "Verification & Validations",
    "web development": "Web technology",
    "full stack development": "Web technology",
    "frontend": "Web technology",
    "deployment": "Deployment",
    "figma": "Figma",
    # AI / ML / Data Science / Python
    "python": "Python",
    "ai": "Artificial Intelligence",
    "artificial intelligence": "Artificial Intelligence",
    "machine learning": "Machine Learning",
    "ml": "Machine Learning",
    "deep learning": "Deep Learning",
    "data science": "Data Science",
    "data analysis": "Data Analysis",
    "data analytics": "Data Analysis",
    "pandas": "Python",
    "numpy": "Python",
    "scikit-learn": "Machine Learning",
    "tensorflow": "Machine Learning",
    "pytorch": "Deep Learning",
    "nlp": "Natural Language Processing",
    "natural language processing": "Natural Language Processing",
    "computer vision": "Computer Vision",
    # Cloud & DevOps
    "cloud": "Cloud Computing",
    "cloud computing": "Cloud Computing",
    "aws": "Cloud Computing",
    "azure": "Cloud Computing",
    "gcp": "Cloud Computing",
    "docker": "Docker",
    "devops": "DevOps",
    # Cyber Security & Database
    "cyber security": "Cyber Security",
    "cybersecurity": "Cyber Security",
    "security": "Cyber Security",
    "sql": "SQL",
    "mysql": "MySQL",
    "postgresql": "PostgreSQL",
}


def map_skill(skill: str) -> str:
    """Map a skill string to the corresponding portal skill option."""
    key = skill.strip().lower()
    return SKILL_MAP.get(key, skill.strip())


class DiaryBot:
    """Drives the VTU diary portal with Playwright."""

    def __init__(self, credentials: dict, headless: bool = False):
        self.creds = credentials
        self.headless = headless
        self.internship_keyword = credentials.get("internship_keyword", "auto")
        self.work_hours = str(credentials.get("work_hours", DEFAULT_WORK_HOURS))
        self.pw = None
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        self.logged_in = False

    # ================================================================
    #  LIFECYCLE
    # ================================================================
    async def start(self):
        """Launch browser with native 100% resolution (no DPI zoom)."""
        ensure_dirs()
        self.pw = await async_playwright().start()
        self.browser = await self.pw.chromium.launch(
            headless=self.headless,
            slow_mo=SLOW_MO_MS,
            args=[
                "--start-maximized",
                "--force-device-scale-factor=1",
            ],
        )
        self.context = await self.browser.new_context(
            no_viewport=True,
            ignore_https_errors=True,
        )
        self.context.set_default_timeout(PAGE_TIMEOUT_MS)
        self.page = await self.context.new_page()
        log.info("Browser launched with natural resolution.")

    async def close(self):
        """Shut everything down gracefully."""
        try:
            if self.context:
                await self.context.close()
            if self.browser:
                await self.browser.close()
            if self.pw:
                await self.pw.stop()
        except Exception as exc:
            log.warning(f"Error during close: {exc}")
        log.info("Browser closed.")

    async def _delay(self, ms: int = ACTION_DELAY_MS):
        await self.page.wait_for_timeout(ms)

    # ================================================================
    #  1. LOGIN
    # ================================================================
    async def login(self):
        """Navigate to sign-in page and log in."""
        log.info(f"Navigating to {PORTAL_URL}")
        await self.page.goto(PORTAL_URL, wait_until="domcontentloaded", timeout=NAV_TIMEOUT_MS)
        await self._delay(2000)

        user_id = self.creds["user_id"]
        password = self.creds["password"]

        # Email / ID input
        id_input = self.page.locator('input[placeholder*="email" i], input[type="email"], input[type="text"]').first
        await id_input.fill(user_id)
        await self._delay(400)

        # Password input
        pw_input = self.page.locator('input[type="password"]').first
        await pw_input.fill(password)
        await self._delay(400)

        # Submit button
        submit_btn = self.page.locator('button[type="submit"]:has-text("Sign In"), button:has-text("Sign In"), button[type="submit"]').first
        await submit_btn.click()

        # Wait for navigation after login
        await self._delay(4000)

        current = self.page.url
        if "sign-in" in current.lower():
            log.error(f"Login failed. Still on: {current}")
            raise RuntimeError(f"Login failed. Still on: {current}")

        self.logged_in = True
        log.info("Login successful.")

    # ================================================================
    #  2. POPUP DISMISSAL
    # ================================================================
    async def handle_popup(self):
        """Dismiss the disclaimer popup if present."""
        log.info("Checking for disclaimer popup...")
        await self._delay(1500)

        understand_btn = self.page.locator('button:has-text("I understand"), button:has-text("Understand")')
        if await understand_btn.count() > 0 and await understand_btn.first.is_visible():
            try:
                modals = self.page.locator('[role="dialog"], .modal, [class*="modal"]')
                if await modals.count() > 0:
                    await modals.first.evaluate("el => el.scrollTo(0, el.scrollHeight)")
            except Exception:
                pass
            await self._delay(500)
            await understand_btn.first.click()
            await self._delay(2000)
            log.info("Disclaimer popup dismissed.")
        else:
            log.info("No disclaimer popup found.")

    # ================================================================
    #  3. NAVIGATE TO DIARY
    # ================================================================
    async def navigate_to_diary(self):
        """Directly navigate to the student diary dashboard."""
        log.info("Navigating to Internship Diary...")
        await self.page.goto("https://vtu.internyet.in/dashboard/student/student-diary", wait_until="domcontentloaded")
        await self._delay(2000)

    # ================================================================
    #  4. SELECT INTERNSHIP (Any Domain or Auto-Detect)
    # ================================================================
    async def select_internship(self):
        """Ensure the internship is selected (supports any domain or auto-detect)."""
        keyword = self.internship_keyword
        log.info(f"Selecting internship (preference: '{keyword}')...")

        # 1. Native <select> element
        selects = self.page.locator("select")
        if await selects.count() > 0 and await selects.first.is_visible():
            # If specific keyword provided and not auto
            if keyword and keyword.lower() != "auto":
                opt = selects.first.locator(f'option:has-text("{keyword}")')
                if await opt.count() > 0:
                    val = await opt.get_attribute("value")
                    await selects.first.select_option(value=val)
                    await self._delay(1500)
                    log.info(f"Selected internship matching '{keyword}'.")
                    return

            # Otherwise select the first valid option
            all_opts = selects.first.locator("option")
            cnt = await all_opts.count()
            for i in range(cnt):
                val = await all_opts.nth(i).get_attribute("value")
                txt = (await all_opts.nth(i).inner_text()).strip()
                if val and txt and "select" not in txt.lower():
                    await selects.first.select_option(value=val)
                    await self._delay(1500)
                    log.info(f"Selected available internship: {txt}")
                    return

        # 2. Button / Custom Dropdown
        btn = self.page.locator('button#internship_id, [id*="internship"]').first
        if await btn.count() > 0 and await btn.is_visible():
            btn_txt = await btn.inner_text()
            if keyword and keyword.lower() != "auto" and keyword.lower() in btn_txt.lower():
                log.info(f"Internship already selected: {btn_txt}")
                return
            log.info("Internship dropdown detected.")
            return

    # ================================================================
    #  5. OPEN ENTRY FORM (Date Picker + Continue)
    # ================================================================
    async def open_entry_form(self, target_date: date):
        """Pick the target date on the diary calendar and click Continue."""
        log.info(f"Opening entry form for {target_date.strftime('%d %b %Y')}...")

        # 1. Click 'Pick a Date'
        pick_btn = self.page.locator('button:has-text("Pick a Date"), button:has([class*="calendar"])').first
        await pick_btn.click()
        await self._delay(1000)

        target_month_name = target_date.strftime("%B").lower()
        day_str = str(target_date.day)

        # 2. Check calendar current month text
        popover = self.page.locator('.rdp, [role="dialog"]').first
        cal_text = (await popover.inner_text()).lower()

        # If target month is not currently displayed, click previous month
        if target_month_name not in cal_text:
            log.info(f"Navigating calendar to {target_date.strftime('%B %Y')}...")
            prev_btn = self.page.locator('button.rdp-button_previous, [aria-label*="previous" i]').first
            if await prev_btn.count() > 0:
                await prev_btn.click()
                await self._delay(1000)

        # 3. Click Day button
        log.info(f"Selecting day {day_str} in calendar...")
        day_btn = self.page.locator(f'button.rdp-day_button:text-is("{day_str}"), button:text-is("{day_str}")').first
        await day_btn.click()
        await self._delay(800)

        # 4. Click 'Continue'
        continue_btn = self.page.locator('button:has-text("Continue")').first
        await continue_btn.wait_for(state="visible", timeout=10000)
        await continue_btn.click()

        # Wait for form page to load
        await self.page.wait_for_selector('textarea[name="description"]', timeout=15000)
        await self._delay(1000)
        log.info(f"Form ready for {target_date.strftime('%d %b %Y')}.")

    # ================================================================
    #  6. FILL FORM
    # ================================================================
    async def fill_form(self, entry: dict):
        """Fill all fields on the create-diary-entry page."""
        log.info(f"Filling diary fields for Day {entry['day_number']}...")

        # Work Summary -> textarea[name="description"]
        desc = self.page.locator('textarea[name="description"]')
        await desc.fill(entry["work_summary"])
        await self._delay(300)

        # Hours Worked -> configurable (default 5.5)
        hours = self.page.locator('input[type="number"]')
        await hours.fill(self.work_hours)
        await self._delay(300)

        # Reference Links -> textarea[name="links"]
        links = self.page.locator('textarea[name="links"]')
        await links.fill(entry["reference_links"])
        await self._delay(300)

        # Learnings / Outcomes -> textarea[name="learnings"]
        learnings = self.page.locator('textarea[name="learnings"]')
        await learnings.fill(entry["learnings_outcomes"])
        await self._delay(300)

        # Blockers / Risks -> textarea[name="blockers"]
        blockers = self.page.locator('textarea[name="blockers"]')
        await blockers.fill(entry["blockers_risks"])
        await self._delay(300)

        log.info(f"Filled Work Summary, {self.work_hours} Hours, Links, Learnings, and Blockers.")

    # ================================================================
    #  7. SELECT SKILLS (One-by-One with auto-fallback)
    # ================================================================
    async def select_skills(self, skills: List[str]):
        """Select skills one by one using the react-select dropdown."""
        log.info(f"Selecting skills from document: {skills}")

        mapped_skills = []
        for s in skills:
            m = map_skill(s)
            if m not in mapped_skills:
                mapped_skills.append(m)

        # Comprehensive fallbacks across domains
        fallback_skills = [
            "React.js", "HTML", "CSS", "Web technology", "Java Script",
            "Python", "Software Testing", "Database design", "Artificial Intelligence",
            "Machine Learning", "Data Analysis", "Verification & Validations"
        ]

        selected_count = 0
        skill_input = self.page.locator('input.react-select__input, input[id*="react-select"]').first

        for sk in mapped_skills:
            if await self._select_single_skill(skill_input, sk):
                selected_count += 1
            await self._delay(400)

        # If no skills matched from document, try generic fallback skills
        if selected_count == 0:
            log.warning("No skills matched from document. Trying common domain skills...")
            for fb in fallback_skills:
                if await self._select_single_skill(skill_input, fb):
                    selected_count += 1
                    if selected_count >= 2:
                        break
                await self._delay(400)

        # If still 0, select the first available option in react-select via keyboard
        if selected_count == 0:
            log.warning("Selecting first available portal skill via keyboard navigation...")
            try:
                await skill_input.click()
                await self.page.keyboard.press("ArrowDown")
                await self._delay(300)
                await self.page.keyboard.press("Enter")
                await self._delay(300)
                selected_count += 1
                log.info("Selected default skill from portal dropdown.")
            except Exception as e:
                log.warning(f"Could not auto-select default skill: {e}")

        log.info(f"Total skills successfully selected: {selected_count}")

    async def _select_single_skill(self, input_locator: Locator, skill_name: str) -> bool:
        """Type skill name and click the matching option."""
        try:
            await input_locator.click()
            await input_locator.fill(skill_name)
            await self._delay(700)

            opt = self.page.locator(f'[class*="select__option"]:has-text("{skill_name}")').first
            if await opt.count() > 0 and await opt.is_visible():
                await opt.click()
                log.info(f"  [OK] Selected skill: {skill_name}")
                await self._delay(500)
                return True
            else:
                await self.page.keyboard.press("Escape")
                log.debug(f"  [SKIP] Skill option not in portal list: {skill_name}")
                return False
        except Exception as e:
            log.warning(f"Error selecting skill '{skill_name}': {e}")
            try:
                await self.page.keyboard.press("Escape")
            except Exception:
                pass
            return False

    # ================================================================
    #  8. SAVE ENTRY
    # ================================================================
    async def save_entry(self):
        """Click the Save button and wait for submission."""
        log.info("Saving diary entry...")
        save_btn = self.page.locator('button:has-text("Save")[type="submit"]').first

        await save_btn.wait_for(state="visible", timeout=10000)
        is_disabled = await save_btn.get_attribute("disabled")
        if is_disabled is not None:
            log.error("Save button is still disabled! Missing required fields or skills.")
            raise RuntimeError("Save button is disabled. Form validation failed.")

        await save_btn.scroll_into_view_if_needed()
        await self._delay(300)
        await save_btn.click()
        await self._delay(4000)
        log.info("Save clicked.")

    # ================================================================
    #  9. VERIFY ENTRY
    # ================================================================
    async def verify_entry(self, target_date: date) -> bool:
        """Verify the entry appears in https://vtu.internyet.in/dashboard/student/diary-entries."""
        log.info(f"Verifying entry for {target_date.strftime('%d %b %Y')} in diary entries...")
        await self.page.goto("https://vtu.internyet.in/dashboard/student/diary-entries", wait_until="domcontentloaded")
        await self._delay(3000)

        date_iso = target_date.strftime("%Y-%m-%d")
        date_slash = target_date.strftime("%d/%m/%Y")
        date_word = target_date.strftime("%d %b %Y")

        text = await self.page.inner_text("body")
        found = (date_iso in text) or (date_slash in text) or (date_word in text)

        if found:
            log.info(f"[OK] Entry for {target_date} verified in records list!")
            return True
        else:
            log.warning(f"[WARN] Entry for {target_date} not seen in first page of entries list.")
            return False

    # ================================================================
    #  10. SCREENSHOT
    # ================================================================
    async def take_screenshot(self, target_date: date) -> str:
        """Take screenshot in DDMMYY.png format and return path."""
        filename = target_date.strftime("%d%m%y") + ".png"
        path = os.path.join(SCREENSHOTS_DIR, filename)
        await self.page.screenshot(path=path, full_page=True)
        log.info(f"Screenshot saved: {path}")
        return path

    # ================================================================
    #  SINGLE ENTRY WORKFLOW
    # ================================================================
    async def do_single_entry(self, entry: dict) -> str:
        """Complete workflow for a single diary entry."""
        target_date = entry["date"]
        log.info(f"=== Starting entry for Day {entry['day_number']} ({target_date.strftime('%d %b %Y')}) ===")

        await self.navigate_to_diary()
        await self.select_internship()
        await self.open_entry_form(target_date)
        await self.fill_form(entry)
        await self.select_skills(entry["skills"])
        await self.save_entry()
        verified = await self.verify_entry(target_date)
        screenshot_path = await self.take_screenshot(target_date)

        if verified:
            log.info(f"=== Day {entry['day_number']} ({target_date}) COMPLETED & VERIFIED ===")
        else:
            log.warning(f"=== Day {entry['day_number']} ({target_date}) SAVED (verification pending) ===")

        return screenshot_path
