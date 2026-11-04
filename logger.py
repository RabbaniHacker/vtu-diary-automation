"""
Logging setup for the diary automation.
Logs to both console and a daily log file.
"""

import logging
import os
from datetime import datetime

from config import LOGS_DIR, ensure_dirs


def setup_logger(name: str = "diary_bot") -> logging.Logger:
    """Create a logger that writes to console + daily log file."""
    ensure_dirs()

    logger = logging.getLogger(name)
    if logger.handlers:          # already configured
        return logger
    logger.setLevel(logging.DEBUG)

    fmt = logging.Formatter(
        "[%(asctime)s] %(levelname)-7s  %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # -- console ----------------------------------------------
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(fmt)
    logger.addHandler(ch)

    # -- file (one per day) -----------------------------------
    today = datetime.now().strftime("%Y-%m-%d")
    log_path = os.path.join(LOGS_DIR, f"{today}.log")
    fh = logging.FileHandler(log_path, encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(fmt)
    logger.addHandler(fh)

    return logger

