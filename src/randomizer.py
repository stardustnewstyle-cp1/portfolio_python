#randomizer.py
import random

#指定件数の記事をランダムに抽出する
#・articles:list[dict] 整形済の記事リスト
#・count:抽出件数　1 or 2
def pick_random_articles(articles, count=1):

    if not articles:
        return []
    
    #countが不正な場合は1にする
    if count not in [1, 2]:
        count = 1
    
    pick_count = min(count, len(articles))

    try:
        #重複なしでランダム抽出
        return random.sample(articles, pick_count)
    except Exception:
        #例外発生時は空リストを返す
        return []