# normalize_article.py
import re
from datetime import datetime
from email.utils import parsedate_to_datetime

from content_extractor import (
    fetch_html,
    extract_content_candidates,
    select_best_content_block,
    normalize_body,
    decide_summary
)



#Qiita / Zenn / RSS データ形式を、共通の形にそろえるための“変換クラス”の初期設定
class BaseAdapter:
    def __init__(self, raw):
        self.raw = raw

    def normalize(self):
        raise NotImplementedError


class Qiita_Article(BaseAdapter):
    def normalize(self):
        tags = self.raw.get("tags", [])
        category = ", ".join([t.get("name", "") for t in tags]) if tags else ""

        return {
            "title": self.raw.get("title", "").strip(),
            "url": normalize_url(self.raw.get("url", "")),
            "category": category,
            "published_at": normalize_date(self.raw.get("created_at")),
            "summary_raw": self.raw.get("body", "")[:200],  # Qiita は body の先頭200文字
            "source": "qiita",
        }

 #記事全体の変換クラス
class Zenn_Article(BaseAdapter):
    def normalize(self):
        published = (
            self.raw.get("published")
            or self.raw.get("updated")
            or ""
        )

    
        tags = self.raw.get("tags")
        if isinstance(tags, list) and len(tags) > 0:
            category = tags[0].get("term", "")
        else:
            category = ""

        return {
            "title": self.raw.get("title", "").strip(),
            "url": normalize_url(self.raw.get("link", "")),
            "category": category,
            "published_at": normalize_date(published),
            "summary_raw": self.raw.get("summary", "") or self.raw.get("description", ""),
            "source": "zenn",
        }

#URL(ZENN) を正規化する
class RSS_Article(BaseAdapter):
    def normalize(self):
      
        published = (
            self.raw.get("published")
            or self.raw.get("updated")
            or ""
        )

        # category: list/dict/string → string に統一
        raw_cat = self.raw.get("category")
        category = normalize_category(raw_cat)

        return {
            "title": self.raw.get("title", "").strip(),
            "url": normalize_url(self.raw.get("link", "")),
            "category": category,
            "published_at": normalize_date(published),
            "summary_raw": self.raw.get("summary", "") or self.raw.get("description", ""),
            "source": "rss",
        }


def get_adapter(raw, source):
    if source == "qiita":
        return Qiita_Article(raw)
    elif source == "zenn":
        return Zenn_Article(raw)
    elif source == "rss":
        return RSS_Article(raw)
    else:
        raise ValueError(f"Unknown source: {source}")



# メイン処理
#Qiita / Zenn / RSS データ形式を、共通の形にそろえるための“変換クラス”の作成

class ArticleNormalizer:

    def normalize(self, raw_item, source):

        # 1. Adapter で統一
        adapter = get_adapter(raw_item, source)
        meta = adapter.normalize()

        # 2. summary_raw の整形
        summary_norm = normalize_summary(meta["summary_raw"])

        # 3. HTML取得
        html = fetch_html(meta["url"], source)

        # 4. 本文抽出
        candidates = extract_content_candidates(html)

        # 5. ベスト選択
        best_block = select_best_content_block(candidates)

        # 6. 本文整形
        body = normalize_body(best_block)

        # 7. summary決定
        summary = decide_summary(meta["title"], summary_norm, body)
       
        #カテゴリの欠損を補正する
        if not meta["category"]:
         meta["category"] = "Other"

        # 8. 出力
        return build_output(meta, summary, body)


# =========================
# 共通処理
# =========================

def normalize_url(url):
    if not url:
        return ""
    url = re.sub(r"\s+", "", url.strip())
    match = re.search(r"(https?://[^\s]+)", url)
    url = match.group(1) if match else url
    return re.sub(r"\?.*$", "", url)

#日付を datetime に変換
def normalize_date(date_str):
    if not date_str:
        return ""

    date_str = date_str.strip()

    # 1. ISO8601形式
    try:
        return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
    except:
        pass

    # 2. RFC822 (RSS)形式
    try:
        return parsedate_to_datetime(date_str)
    except:
        pass

    # 3. yyyy/mm/dd
    try:
        return datetime.strptime(date_str, "%Y/%m/%d")
    except:
        pass

    return ""

 #RSS の category を string に統一
def normalize_category(cat):   
    if not cat:
        return ""

    # list → 最初の term
    if isinstance(cat, list):
        first = cat[0]
        if isinstance(first, dict):
            return first.get("term", "") or first.get("label", "")
        return str(first)

    # dict
    if isinstance(cat, dict):
        return cat.get("term", "") or cat.get("label", "")

    # string
    return str(cat)

#summary_raw を読みやすく整形
def normalize_summary(text):
    text = re.sub(r"<[^>]*>", "", text)
    text = re.sub(r"\n{2,}", "\n", text)
    text = re.sub(r"[\s\u3000]{2,}", " ", text)
    return text.strip()


#最終的な記事データを組み立てる
def build_output(meta, summary, body):
    return {
        "title": meta["title"],
        "url": meta["url"],
        "category": meta["category"],
        "published_at": meta["published_at"],
        "summary": summary,
        "body": body,
        "source": meta["source"],
    }
