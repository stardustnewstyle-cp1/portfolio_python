#fetch_qiita_articles.py
#APIアクセス
import requests

def fetch_qiita_articles():
    url = "https://qiita.com/api/v2/items"
    params = {"per_page": 30, "page": 1}

#レスポンス取得
      
    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
    except Exception as e:
        print(f"Error fetching Qiita articles: {e}")
        return []

#JSONパース 
    try:
     items = response.json()
    except ValueError:
       print("Error parsing JSON response")
       return []
#各記事を抽出
    articles = []
    for item in items:
        summary = (item.get("body") or "").replace("\n", " ")[:200]
        tags = item.get("tags", [])
        category = ", ".join(tag.get("name", "")for tag in tags)
#標準構造に整形
        article = {
            "title": item["title"],
            "summary": summary,
            "category": category,
            "url": item["url"],
            "source": "qiita",
            "published_at": item["created_at"]
        }
        articles.append(article)

#リストで返す
    return articles
