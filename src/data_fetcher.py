#data_fetcher.py
import traceback

from fetch_qiita_articles import fetch_qiita_articles
from fetch_zenn_articles import fetch_zenn_articles
from fetch_rss_articles import fetch_rss_articles

from config import RSS_FEEDS
from normalize_article import ArticleNormalizer


normalizer = ArticleNormalizer()


# RSS 全件取得
def fetch_all_rss_articles():
    articles = []
    for url in RSS_FEEDS:
        try:
            raw_list = fetch_rss_articles(url)
            articles.extend(raw_list)
        except Exception:
            print(f"[RSS取得失敗] {url}")
            traceback.print_exc()
    return articles


# Qiita + Zenn + RSS をまとめて取得
def fetch_all_articles():
    raw_articles = []

    # Qiita
    try:
        raw_articles.extend(fetch_qiita_articles())
    except Exception:
        print("[Qiita取得失敗]")
        traceback.print_exc()

    # Zenn
    try:
        raw_articles.extend(fetch_zenn_articles())
    except Exception:
        print("[Zenn取得失敗]")
        traceback.print_exc()

    # RSS
    try:
        raw_articles.extend(fetch_all_rss_articles())
    except Exception:
        print("[RSS取得失敗]")
        traceback.print_exc()

    
    # 正規化（normalizer）
    normalized = []
    for raw in raw_articles:
        try:
            article = normalizer.normalize(raw, raw.get("source"))
            normalized.append(article)
        except Exception:
            print("[normalize失敗]")
            traceback.print_exc()

    return normalized
