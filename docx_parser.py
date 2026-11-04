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


def parse_date_string(text: str) -> Optional[date]:
    """Try various date formats commonly used in internship diaries."""
    # 06 October 2026 / 6 Oct 2026
    m = re.search(r"(\d{1,2})\s+([A-Za-z]+)\s+(\d{4})", text)
    if m:
        d, mon, y = m.groups()
        for fmt in ("%d %B %Y", "%d %b %Y"):
            try:
                return datetime.strptime(f"{d} {mon} {y}", fmt).date()
            except ValueError:
                pass

    # DD/MM/YYYY or DD-MM-YYYY
    m = re.search(r"(\d{1,2})[/-](\d{1,2})[/-](\d{4})", text)
    if m:
        d, mon, y = m.groups()
        try:
            return datetime.strptime(f"{d}/{mon}/{y}", "%d/%m/%Y").date()
        except ValueError:
            pass

    return None


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

    # Strategy 1: Paragraph-based parsing
    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            continue

        # Look for Day header: e.g. "Day 65 -- 06 October 2026" or "Day 1 - 03 Aug 2026"
        day_match = re.search(r"\bDay\s+(\d+)\b", text, re.IGNORECASE)
        entry_date = parse_date_string(text) if day_match else None

        if day_match and entry_date:
            current_entry = {
                "day_number": int(day_match.group(1)),
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
            entries[entry_date] = current_entry
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
                    entry = {
                        "day_number": int(day_m.group(1)),
                        "date": d_val,
                        "date_str": d_val.strftime("%Y-%m-%d"),
                        "date_display": d_val.strftime("%d/%m/%Y"),
                        "work_summary": "",
                        "hours_worked": "5.5",
                        "reference_links": "",
                        "learnings_outcomes": "",
                        "blockers_risks": "",
                        "skills": [],
                    }
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
