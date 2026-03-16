from __future__ import annotations

import sqlite3
from pathlib import Path

from config import SQL_DB_PATH


def init_db() -> sqlite3.Connection:
    """
    Initialise the SQLite database and create the articles table if needed.
    """
    db_path = Path(SQL_DB_PATH)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            url TEXT NOT NULL UNIQUE,
            source TEXT,
            time_published TEXT,
            sentiment_score REAL,
            sentiment_label TEXT,
            tickers TEXT
        )
        """
    )

    conn.commit()
    return conn


def store_articles(conn: sqlite3.Connection, articles: list[dict]) -> int:
    """
    Insert articles into SQLite.
    Uses INSERT OR IGNORE so repeated GitHub runs do not duplicate rows.
    """
    cursor = conn.cursor()
    inserted = 0

    sql = """
        INSERT OR IGNORE INTO articles (
            title, url, source, time_published,
            sentiment_score, sentiment_label, tickers
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """

    for article in articles:
        cursor.execute(
            sql,
            (
                article["title"],
                article["url"],
                article["source"],
                article["time_published"],
                article["sentiment_score"],
                article["sentiment_label"],
                article["tickers"],
            ),
        )
        inserted += cursor.rowcount

    conn.commit()
    return inserted


if __name__ == "__main__":
    sample = [
        {
            "title": "Apple reports record quarterly earnings",
            "url": "https://example.com/apple-earnings",
            "source": "FinanceNews",
            "time_published": "20260101T1200",
            "sentiment_score": 0.72,
            "sentiment_label": "Positive",
            "tickers": "AAPL",
        }
    ]

    conn = init_db()
    inserted = store_articles(conn, sample)
    print(f"Inserted {inserted} article(s)")
    conn.close()