from __future__ import annotations

import os
from typing import Any

import requests
from dotenv import load_dotenv

from config import TICKERS, NEWS_LIMIT, alpha_vantage_time_from

load_dotenv()

BASE_URL = "https://www.alphavantage.co/query"


def build_news_url(api_key: str) -> str:
    """
    Build the AlphaVantage News Sentiment API URL.
    """
    time_from = alpha_vantage_time_from()

    return (
        f"{BASE_URL}?"
        f"function=NEWS_SENTIMENT&"
        f"tickers={TICKERS}&"
        f"time_from={time_from}&"
        f"limit={NEWS_LIMIT}&"
        f"apikey={api_key}"
    )


def fetch_news() -> list[dict[str, Any]]:
    """
    Fetch financial news articles from AlphaVantage and return them
    as cleaned dictionaries.
    """
    api_key = os.getenv("AV_API_KEY")
    if not api_key:
        raise RuntimeError(
            "Missing AV_API_KEY. Add it to your .env file locally or GitHub Secrets in CI."
        )

    url = build_news_url(api_key)

    response = requests.get(url, timeout=30)
    response.raise_for_status()
    data = response.json()

    if "Note" in data:
        raise RuntimeError(f"AlphaVantage note: {data['Note']}")
    if "Error Message" in data:
        raise RuntimeError(f"AlphaVantage error: {data['Error Message']}")

    articles: list[dict[str, Any]] = []

    for article in data.get("feed", []):
        ticker_sentiment = article.get("ticker_sentiment", [])
        tickers = ", ".join(
            item.get("ticker", "")
            for item in ticker_sentiment
            if item.get("ticker")
        )

        articles.append(
            {
                "title": article.get("title", "N/A"),
                "url": article.get("url", "N/A"),
                "source": article.get("source", "N/A"),
                "time_published": article.get("time_published", "N/A"),
                "summary": article.get("summary", "N/A"),
                "sentiment_score": float(article.get("overall_sentiment_score", 0.0)),
                "sentiment_label": article.get("overall_sentiment_label", "N/A"),
                "tickers": tickers,
            }
        )

    return articles


if __name__ == "__main__":
    articles = fetch_news()
    print(f"Fetched {len(articles)} articles")
    if articles:
        print("\nFirst article:")
        for key, value in articles[0].items():
            print(f"  {key}: {value}")