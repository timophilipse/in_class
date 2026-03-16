# config.py
from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# ── Pipeline settings ────────────────────────────────────────────────────────
TICKERS = os.getenv("TICKERS", "AAPL")
NEWS_LIMIT = int(os.getenv("NEWS_LIMIT", "15"))
LOOKBACK_DAYS = int(os.getenv("LOOKBACK_DAYS", "7"))

# ── Storage settings ─────────────────────────────────────────────────────────
SQL_DB_PATH = os.getenv("SQL_DB_PATH", str(DATA_DIR / "news.db"))
CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", str(DATA_DIR / "chroma_db"))
CHROMA_COLLECTION = os.getenv("CHROMA_COLLECTION", "news_articles")


def alpha_vantage_time_from(lookback_days: int = LOOKBACK_DAYS) -> str:
    """
    Return AlphaVantage-compatible timestamp format: YYYYMMDDTHHMM
    """
    dt = datetime.now(timezone.utc) - timedelta(days=lookback_days)
    return dt.strftime("%Y%m%dT%H%M")