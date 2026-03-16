from __future__ import annotations

import sqlite3

import chromadb

from config import CHROMA_COLLECTION, CHROMA_DB_PATH, SQL_DB_PATH


def query_sql(conn: sqlite3.Connection, sentiment_label: str = "Positive") -> None:
    """
    Query SQLite articles by sentiment label.
    """
    cursor = conn.cursor()

    sql = """
        SELECT title, source, sentiment_score, tickers
        FROM articles
        WHERE sentiment_label = ?
        ORDER BY sentiment_score DESC
    """

    cursor.execute(sql, (sentiment_label,))
    rows = cursor.fetchall()

    if not rows:
        print(f"No SQL results found for sentiment_label='{sentiment_label}'.")
        print()
        return

    for i, row in enumerate(rows, start=1):
        title, source, sentiment_score, tickers = row
        print(f"{i}. {title}")
        print(f"   Source: {source}")
        print(f"   Sentiment score: {sentiment_score}")
        print(f"   Tickers: {tickers}")
        print()


def query_vector(collection: chromadb.Collection, search_text: str, n_results: int = 3) -> None:
    """
    Query ChromaDB by semantic similarity.
    """
    results = collection.query(query_texts=[search_text], n_results=n_results)

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    if not documents:
        print(f"No vector results found for query='{search_text}'.")
        print()
        return

    for i, (document, metadata, distance) in enumerate(
        zip(documents, metadatas, distances), start=1
    ):
        print(f"{i}. {metadata.get('title', 'N/A')}")
        print(f"   Source: {metadata.get('source', 'N/A')}")
        print(f"   Sentiment: {metadata.get('sentiment_label', 'N/A')}")
        print(f"   Tickers: {metadata.get('tickers', 'N/A')}")
        print(f"   Distance: {distance}")
        print(f"   Text: {document[:200]}...")
        print()


if __name__ == "__main__":
    print("── SQL Query Test ─────────────────────────────────────────────")
    conn = sqlite3.connect(SQL_DB_PATH)
    query_sql(conn, sentiment_label="Positive")
    conn.close()

    print("── Vector Query Test ──────────────────────────────────────────")
    client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
    collection = client.get_or_create_collection(name=CHROMA_COLLECTION)
    query_vector(collection, "interest rate and inflation")