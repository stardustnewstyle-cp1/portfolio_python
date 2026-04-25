# content_extractor.py
import re
import requests
from bs4 import BeautifulSoup
from config import USER_AGENT


# =========================
# HTML取得
# =========================
def fetch_html(url, source=None):
    headers = {"User-Agent": USER_AGENT}

    for _ in range(3):  # リトライ3回
        try:
            res = requests.get(url, headers=headers, timeout=10)
            res.raise_for_status()
            return res.text
        except Exception:
            continue

    print(f"fetch_html error: failed to fetch {url}")
    return ""


# =========================
# 本文候補抽出
# =========================
def extract_content_candidates(html):
    if not html:
        return []

    soup = BeautifulSoup(html, "html.parser")
    candidates = []

    # 優先タグ
    priority_tags = ["article", "main", "section"]
    fallback_tags = ["div"]

    # 優先タグ → fallback の順で抽出
    for tag_name in priority_tags + fallback_tags:
        for tag in soup.find_all(tag_name):

            text = tag.get_text("\n").strip()
            if len(text) < 50:
                continue

            p_count = len(tag.find_all("p"))
            if p_count < 1:
                continue

            link_count = len(tag.find_all("a"))
            class_id = " ".join((tag.get("class") or []) + [tag.get("id") or ""])

            candidates.append({
                "text": text,
                "p_count": p_count,
                "link_count": link_count,
                "class_id": class_id,
                "html": str(tag),
            })

    return candidates


# =========================
# スコアリング
# =========================
def score_content_block(block):
    text = block["text"]
    length = len(text)
    p_count = block["p_count"]
    link_density = block["link_count"] / max(p_count, 1)

    score = 0

    # 適度な長さ
    if 200 <= length <= 2000:
        score += 3
    elif length > 3000:
        score -= 2  # 長すぎる場合はペナルティ

    # 段落数
    if 3 <= p_count <= 20:
        score += 3

    # リンク密度（広告除外）
    if link_density < 0.1:
        score += 2
    elif link_density > 0.3:
        score -= 2

    # class/id に本文っぽいキーワード
    if contains_keywords(block["class_id"]):
        score += 2

    # 関連記事などのノイズ
    if "関連記事" in text:
        score -= 2

    # 行数が多いほど本文らしい
    if len(text.split("\n")) > 5:
        score += 1

    return score


def contains_keywords(class_id):
    keywords = ["article", "content", "main", "post", "entry", "body"]
    return any(k in class_id.lower() for k in keywords)


# =========================
# 最良ブロック選択
# =========================
def select_best_content_block(candidates):
    if not candidates:
        return ""
    best = max(candidates, key=score_content_block)
    return best["text"]


# =========================
# 本文整形
# =========================
def normalize_body(text):
    if not text:
        return ""

    soup = BeautifulSoup(text, "html.parser")

    # ノイズ除去
    for tag in soup(["script", "style", "nav", "footer", "aside"]):
        tag.decompose()

    # テキスト抽出
    text = soup.get_text("\n")

    # 改行整形（2行に統一）
    text = re.sub(r"\n{2,}", "\n\n", text)

    # 行頭・行末の空白除去
    text = "\n".join(line.strip() for line in text.split("\n"))

    # 空行を除外して段落化
    paragraphs = [p for p in text.split("\n\n") if p.strip()]
    return "\n\n".join(paragraphs)


# =========================
# 要約生成
# =========================
def summarize_paragraphs(body):
    paragraphs = body.split("\n\n")
    summaries = []

    for p in paragraphs:
        sentences = re.split(r"[。.!?]", p)
        if sentences and len(sentences[0]) > 20:
            summaries.append(sentences[0])
        if len(summaries) >= 5:
            break

    return " / ".join(summaries)


def decide_summary(title, summary_raw, body):
    if summary_raw and len(summary_raw) >= 20:
        return summary_raw

    body_summary = summarize_paragraphs(body)
    return body_summary if body_summary else title
