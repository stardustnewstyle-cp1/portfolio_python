#fetcher_rss_articles.py
import requests
import feedparser

def fetch_rss_articles(url):
    # RSS URLにアクセス
    try:
        response = requests.get(url, timeout=5)
        if response.status_code !=200:
            return []
    except Exception:
        return []
    #RSS 解析
    feed = feedparser.parse(response.text)

    articles = []

    #必要項目の抽出　30件までs
    for entry in feed.entries[:30]:
        title = getattr(entry, "title", "")
        link = getattr(entry, "link", "")
        #RSSの本文はdescription or summary(HTMLのまま)
        summary_raw= (
            getattr(entry, "summary", None) or getattr(entry, "description", None) or ""

        )
        published_at = getattr(entry, "published", getattr(entry, "updated", ""))
        category = getattr(entry, "tags", getattr(entry, "category", ""))

        #raw構造に整形
        article = {
            "title": title,
            "url": link,
            "summary_raw": summary_raw,
            "published_at": published_at,
            "category": category,
            "source": "rss"
        }
        articles.append(article)

    return articles
