"""
Parse the VTU internship daily diary DOCX and return structured entry data.
Supports any student domain (Web Dev, AI, Cyber Security, Cloud, Data Science, etc.),
flexible heading formats, various date styles, and both paragraph & table layouts.
"""

import os
import re
from datetime import date, datetime
from typing import Dict, List, Optional

import docx

MONTH_MAP = {
    'jan': 1, 'january': 1,
    'feb': 2, 'february': 2,
    'mar': 3, 'march': 3,
    'apr': 4, 'april': 4,
    'may': 5,
    'jun': 6, 'june': 6,
    'jul': 7, 'july': 7,
    'aug': 8, 'august': 8,
    'sep': 9, 'sept': 9, 'september': 9,
    'oct': 10, 'october': 10,
    'nov': 11, 'november': 11,
    'dec': 12, 'december': 12
}


def parse_date_string(text: str) -> Optional[date]:
    """
    Try various date formats commonly used in internship diaries:
    - 24 September 2026 / 24th Sept 2026 / 24 Sep 2026 / 3rd Oct 2026
    - 24/09/2026 / 24/9/2026 / 24-09-2026 / 24.09.2026
    - 2026-09-24 / 2026/09/24
    """
    if not text:
        return None

    # Strip ordinals (24th -> 24, 1st -> 1, 2nd -> 2, 3rd -> 3)
    clean = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', text, flags=re.IGNORECASE)

    # 1. Day Month Year: e.g. "24 September 2026" or "24 Sept 2026" or "6 Oct 2026"
    m = re.search(r'\b(\d{1,2})\s+([A-Za-z]+)\.?\s+(\d{4})\b', clean)
    if m:
        d, mon, y = m.groups()
        mon_num = MONTH_MAP.get(mon.lower())
        if mon_num:
            try:
                return date(int(y), mon_num, int(d))
            except ValueError:
                pass

    # 2. Month Day, Year: e.g. "September 24, 2026" or "Oct 6, 2026"
    m = re.search(r'\b([A-Za-z]+)\.?\s+(\d{1,2}),?\s+(\d{4})\b', clean)
    if m:
        mon, d, y = m.groups()
        mon_num = MONTH_MAP.get(mon.lower())
        if mon_num:
            try:
                return date(int(y), mon_num, int(d))
            except ValueError:
                pass

    # 3. DD/MM/YYYY or DD-MM-YYYY or DD.MM.YYYY
    m = re.search(r'\b(\d{1,2})[/\-\.](\d{1,2})[/\-\.](\d{4})\b', clean)
    if m:
        p1, p2, y = m.groups()
        d_val, mon_val = int(p1), int(p2)
        # Determine day vs month (standard VTU format is DD/MM/YYYY)
        if 1 <= mon_val <= 12 and 1 <= d_val <= 31:
            try:
                return date(int(y), mon_val, d_val)
            except ValueError:
                pass

    # 4. YYYY-MM-DD or YYYY/MM/DD
    m = re.search(r'\b(\d{4})[/\-](\d{1,2})[/\-](\d{1,2})\b', clean)
    if m:
        y, mon, d = m.groups()
        try:
            return date(int(y), int(mon), int(d))
        except ValueError:
            pass

    return None


def create_entry_dict(day_number: int, entry_date: date) -> dict:
    return {
        "day_number": day_number,
        "date": entry_date,
        "date_str": entry_date.strftime("%Y-%m-%d"),
        "date_display": entry_date.strftime("%d/%m/%Y"),
        "work_summary": "",
        "hours_worked": "5.5",
        "reference_links": "",
        "learnings_outcomes": "",
        "blockers_risks": "",
        "skills": [],
    }


def parse_diary(docx_path: str) -> Dict[date, dict]:
    """
    Parse every day entry from the DOCX.

    Returns
    -------
    dict  -  { datetime.date : { day_number, date, work_summary,
               hours_worked, reference_links, learnings_outcomes,
               blockers_risks, skills[] } }
    """
    if not os.path.exists(docx_path):
        raise FileNotFoundError(f"Diary document not found: {docx_path}")

    doc = docx.Document(docx_path)
    entries: Dict[date, dict] = {}
    current_entry: Optional[dict] = None
    pending_day_num: Optional[int] = None

    # Strategy 1: Paragraph-based parsing
    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            continue

        day_match = re.search(r"\bDay\s+(\d+)\b", text, re.IGNORECASE)
        entry_date = parse_date_string(text)

        # Case A: Both Day number and Date on same line (e.g. "Day 53 -- 24 September 2026")
        if day_match and entry_date:
            day_num = int(day_match.group(1))
            current_entry = create_entry_dict(day_num, entry_date)
            entries[entry_date] = current_entry
            pending_day_num = None
            continue

        # Case B: Day header on this line, Date on next line (e.g. Line 1: "Day 53", Line 2: "24/09/2026")
        if day_match and not entry_date:
            pending_day_num = int(day_match.group(1))
            continue

        # Case C: Previous line was Day header, and this line contains the date
        if pending_day_num is not None and entry_date:
            current_entry = create_entry_dict(pending_day_num, entry_date)
            entries[entry_date] = current_entry
            pending_day_num = None
            continue

        if current_entry is None:
            continue

        # Flexible field extraction
        lower = text.lower()
        if lower.startswith(("work summary:", "summary:", "work done:", "description:")):
            current_entry["work_summary"] = text.split(":", 1)[1].strip()
        elif lower.startswith(("hours worked:", "hours:", "duration:")):
            current_entry["hours_worked"] = text.split(":", 1)[1].strip()
        elif lower.startswith(("reference links:", "reference link:", "reference:", "links:", "link:")):
            current_entry["reference_links"] = text.split(":", 1)[1].strip()
        elif lower.startswith(("learnings / outcomes:", "learnings & outcomes:", "learnings:", "outcomes:", "learnings/outcomes:")):
            current_entry["learnings_outcomes"] = text.split(":", 1)[1].strip()
        elif lower.startswith(("blockers / risks:", "blockers & risks:", "blockers:", "risks:", "challenges:", "blockers/risks:")):
            current_entry["blockers_risks"] = text.split(":", 1)[1].strip()
        elif lower.startswith(("skills used:", "skills:", "key skills:", "technologies:")):
            raw = text.split(":", 1)[1].strip()
            current_entry["skills"] = [s.strip() for s in raw.split(",") if s.strip()]

    # Strategy 2: If no entries found via paragraphs, check document tables
    if not entries and doc.tables:
        for table in doc.tables:
            for row in table.rows:
                cells_text = [c.text.strip() for c in row.cells]
                combined = " \n ".join(cells_text)
                day_m = re.search(r"\bDay\s+(\d+)\b", combined, re.IGNORECASE)
                d_val = parse_date_string(combined)
                if day_m and d_val:
                    entry = create_entry_dict(int(day_m.group(1)), d_val)
                    for t in cells_text:
                        l = t.lower()
                        if ":" in t:
                            k, v = t.split(":", 1)
                            k = k.strip().lower()
                            v = v.strip()
                            if "summary" in k or "work" in k: entry["work_summary"] = v
                            elif "link" in k or "ref" in k: entry["reference_links"] = v
                            elif "learning" in k or "outcome" in k: entry["learnings_outcomes"] = v
                            elif "blocker" in k or "risk" in k: entry["blockers_risks"] = v
                            elif "skill" in k: entry["skills"] = [s.strip() for s in v.split(",") if s.strip()]
                    entries[d_val] = entry

    return entries


def get_entry_for_date(docx_path: str, target: date) -> Optional[dict]:
    """Return the diary entry for a single date, or None."""
    return parse_diary(docx_path).get(target)


def get_entries_for_range(docx_path: str, start: date, end: date) -> List[dict]:
    """Return a sorted list of entries whose date falls in [start, end]."""
    all_entries = parse_diary(docx_path)
    return sorted(
        [e for d, e in all_entries.items() if start <= d <= end],
        key=lambda e: e["date"],
    )


# -- quick self-test ----------------------------------------------
if __name__ == "__main__":
    import sys, pprint
    path = sys.argv[1] if len(sys.argv) > 1 else "diary_data.docx"
    entries = parse_diary(path)
    print(f"Parsed {len(entries)} day entries from {path}.")
    dates = sorted(entries.keys())
    if dates:
        print("\nFirst entry:")
        pprint.pprint(entries[dates[0]])
        print("\nLast entry:")
        pprint.pprint(entries[dates[-1]])
