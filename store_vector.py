from __future__ import annotations

import chromadb

from config import CHROMA_COLLECTION, CHROMA_DB_PATH


def init_vector_db() -> chromadb.Collection:
    """
    Initialise a persistent ChromaDB client and return the collection.
    """
    chroma_client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
    collection = chroma_client.get_or_create_collection(name=CHROMA_COLLECTION)
    return collection


def store_articles_vector(collection: chromadb.Collection, articles: list[dict]) -> int:
    """
    Store each article in ChromaDB.
    ChromaDB generates embeddings automatically from the document text.
    """
    stored = 0

    for article in articles:
        text = f"{article['title']}. {article.get('summary', '')}"

        try:
            collection.add(
                ids=[article["url"]],
                documents=[text],
                metadatas=[
                    {
                        "title": str(article["title"]),
                        "source": str(article["source"]),
                        "sentiment_label": str(article["sentiment_label"]),
                        "tickers": str(article["tickers"]),
                    }
                ],
            )
            stored += 1

        except Exception as exc:
            # Most likely duplicate ID on repeated scheduled runs
            print(f"Skipping vector insert for {article['url']}: {exc}")

    return stored


if __name__ == "__main__":
    sample = [
        {
            "title": "Apple reports record quarterly earnings",
            "url": "https://example.com/apple-earnings",
            "source": "FinanceNews",
            "summary": (
                "Apple Inc. reported record quarterly earnings driven by "
                "strong iPhone and services revenue."
            ),
            "sentiment_score": 0.72,
            "sentiment_label": "Positive",
            "tickers": "AAPL",
        }
    ]

    collection = init_vector_db()
    stored = store_articles_vector(collection, sample)
    print(f"Stored {stored} article(s) in ChromaDB")