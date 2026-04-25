# config.py

# =========================
# User-Agent（設計書準拠するよう設定）
# =========================
USER_AGENT = "Mozilla/5.0 (compatible; TechNewsRandomizer/1.0)"

# =========================
# API / RSS URL
# =========================
QIITA_API_URL = "https://qiita.com/api/v2/items"

# Zenn は公式APIがないため RSS を使用
ZENN_RSS_URL = "https://zenn.dev/feed"

# 技術系 RSS フィード一覧
RSS_FEEDS = [
    "https://techcrunch.com/feed/",
    "https://rss.slashdot.org/Slashdot/slashdotMain",
    "https://qiita.com/popular-items/feed",
]

# =========================
# 取得件数（Qiita / Zenn / RSS）
# =========================
FETCH_LIMIT = 30

# =========================
# カテゴリ一覧（UI の選択肢）
# =========================
CATEGORIES = [
    "Python",
    "AI",
    "Web",
    "Security",
    "Cloud",
    "Other",
]
