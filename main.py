# main.py
from __future__ import annotations

from fetch import fetch_news
from store_sql import init_db, store_articles
from store_vector import init_vector_db, store_articles_vector
from query import query_sql, query_vector
from config import TICKERS


def main() -> None:
    print("=" * 60)
    print(f"Financial News Pipeline — {TICKERS}")
    print("=" * 60)

    print("\n[1/4] Fetching news articles...")
    articles = fetch_news()
    if not articles:
        print("No articles fetched.")
        return
    print(f"Fetched {len(articles)} articles")

    print("\n[2/4] Storing structured data in SQLite...")
    conn = init_db()
    inserted_sql = store_articles(conn, articles)
    print(f"Inserted {inserted_sql} new article(s) into SQLite")

    print("\n[3/4] Storing vector data in ChromaDB...")
    print("First run may download an embedding model. That is normal.")
    collection = init_vector_db()
    inserted_vector = store_articles_vector(collection, articles)
    print(f"Stored {inserted_vector} new article(s) in ChromaDB")

    print("\n[4/4] Querying results...")

    print("\n── SQL: Positive sentiment articles ─────────────────────────")
    query_sql(conn, sentiment_label="Positive")

    print("── Vector: 'interest rate and inflation' ───────────────────")
    query_vector(collection, "interest rate and inflation")

    conn.close()

    print("=" * 60)
    print("Pipeline complete.")
    print("=" * 60)


if __name__ == "__main__":
    main()