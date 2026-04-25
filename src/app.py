# app.py
import streamlit as st
from datetime import datetime

from data_fetcher import fetch_all_articles
from randomizer import pick_random_articles
from config import CATEGORIES
from normalize_article import ArticleNormalizer

normalizer = ArticleNormalizer()

# =========================
# 読了時間（分）を返す
# =========================
def calc_reading_time(text: str) -> float:
    if not text:
        return 0
    chars = len(text)
    return chars / 350.0


# =========================
# 表示件数の決定（読了時間ベース）
# =========================
def decide_display_count(articles, max_count=2):
    if not articles:
        return 0

    candidates = pick_random_articles(articles, count=2)

    if len(candidates) == 1:
        return 1

    t1 = calc_reading_time(candidates[0].get("body", ""))
    t2 = calc_reading_time(candidates[1].get("body", ""))

    if t1 + t2 <= 10:
        return min(2, max_count)
    else:
        return 1


# =========================
# Streamlit UI
# =========================
st.set_page_config(
    page_title="技術記事ランダム表示アプリ",
    layout="wide"
)

st.title("技術記事ランダム表示アプリ")

if "initialized" not in st.session_state:
    st.info("カテゴリを選んで『記事を取得』を押してください。")
    st.session_state.initialized = True


# カテゴリ選択
category = st.selectbox(
    "カテゴリを選択してください",
    ["すべて"] + CATEGORIES
)

# 表示件数（最大値）
max_display = st.radio(
    "最大表示件数",
    [1, 2],
    index=1,
    help="読了時間に応じて自動調整されます（最大値の上限）"
)

# ボタン押下
if st.button("記事を取得"):

    with st.spinner("記事を取得しています..."):

        # 1. 全記事取得
        raw_articles = fetch_all_articles()

        # 2. カテゴリフィルタ
        if category != "すべて":
            raw_articles = [a for a in raw_articles if a.get("category") == category]

        if not raw_articles:
            st.warning("該当する記事がありませんでした。")
            st.stop()

        # 3. 読了時間ベースで表示件数を決定
        display_count = decide_display_count(raw_articles, max_count=max_display)

        # 4. ランダム抽出（raw）
        selected_raw = pick_random_articles(raw_articles, count=display_count)

        # 5. normalize（1〜2件だけ）
        selected = [normalizer.normalize(a, a.get("source")) for a in selected_raw]

        if not selected:
            st.warning("記事を抽出できませんでした。")
            st.stop()

        # 6. 表示
        st.subheader(f"表示件数：{len(selected)} 件")

        for a in selected:
            with st.container():

                st.markdown("### " + a["title"])
                st.write(a["summary"])

                if a.get("category"):
                    st.write(f"カテゴリ: {a['category']}")

                pub = a.get("published_at")
                if isinstance(pub, datetime):
                    st.write(f"公開日: {pub.date()}")

                if a.get("body"):
                    with st.expander("本文を表示"):
                        st.write(a["body"])

                st.markdown(
                    f'<a href="{a["url"]}" target="_blank" rel="noopener noreferrer">記事を開く</a>',
                    unsafe_allow_html=True
                )
                st.markdown("---")
