from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from config import TICKERS
from fetch import fetch_news
from store_sql import init_db, store_articles
from store_vector import init_vector_db, store_articles_vector


def main() -> None:

    print("Starting news pipeline...")

    # ── Fetch ──────────────────────────────────────
    articles = fetch_news()
    fetched_count = len(articles)

    print(f"Fetched {fetched_count} articles")

    if not articles:
        print("No articles fetched — exiting.")
        return

    # ── Store SQL ──────────────────────────────────
    conn = init_db()
    sql_inserted = store_articles(conn, articles)
    conn.close()

    print(f"Inserted {sql_inserted} new rows into SQLite")

    # ── Store vectors ──────────────────────────────
    collection = init_vector_db()
    vector_inserted = store_articles_vector(collection, articles)

    print(f"Stored {vector_inserted} vectors")

    # ── Summary ────────────────────────────────────
    summary = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "tickers": TICKERS,
        "articles_fetched": fetched_count,
        "sql_inserted": sql_inserted,
        "vector_inserted": vector_inserted,
    }

    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)

    summary_path = output_dir / "run_summary.json"

    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=4)

    print("Run summary written to:", summary_path)
    print(summary)


if __name__ == "__main__":
    main()