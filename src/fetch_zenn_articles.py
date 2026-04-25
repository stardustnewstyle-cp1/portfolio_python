# fetch_zenn_articles.py
import requests
import feedparser
from config import USER_AGENT, ZENN_RSS_URL, FETCH_LIMIT

#Zenn RSS から記事を取得し、
#生データ（＋source）を返す。
def fetch_zenn_articles():

    # HTTP取得
    try:
        headers = {"User-Agent": USER_AGENT}
        response = requests.get(ZENN_RSS_URL, headers=headers, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"[Zenn取得失敗] {e}")
        return []

    # RSS パース(HTTPの情報を取得し、解析する)
    feed = feedparser.parse(response.text)
    entries = feed.entries[:FETCH_LIMIT]

    articles = []

    for entry in entries:
        raw = {
            "title": getattr(entry, "title", ""),
            "url": getattr(entry, "link", ""),
            "summary_raw": getattr(entry, "description", ""),
            "published_at": getattr(entry, "published", ""),
            "category": getattr(entry, "tags", getattr(entry, "category", "")),
            "source": "zenn",
        }
        articles.append(raw)

    return articles
