※ 本 README は成果物の説明を目的としており、pythonの学習成果は別紙「学習まとめ.txt」に記載している。

# 1. アプリ名
技術記事ランダム表示アプリ

# 2. このアプリを作った目的
本アプリは、Python の言語習得を目的とした自己研鑽の一環として作成した。
外部データ取得・HTML解析・データ整形・ロジック実装・UI構築など、
Python の基礎〜応用を一連の流れで実装し、理解の定着を図ることを目的としている。

そのうえで、アプリとして以下の価値を提供する。

- 技術情報に自然に触れられる仕組みを提供する
- Qiita / Zenn / 技術系 RSS から信頼性の高い情報を取得する
- ランダム表示により、普段触れない分野にも目が向くようにする

# 3. アプリの概要
本アプリは、Qiita・Zenn・技術系 RSS から技術記事を取得し、  
**カテゴリ選択 → 記事一覧 → 本文表示 → 読了時間表示**  
という流れで技術記事をランダム閲覧できる。

- 公開 API / RSS のみを利用
- 取得データを統一フォーマットに整形
- Streamlit によるシンプルな UI
- HTML から本文を抽出し、読了時間を推定
- 1〜2件の技術記事をランダムに表示

# 4. 機能
- 技術記事のランダム表示
- カテゴリ選択
- 記事カード表示（タイトル・概要・URL）
- 本文抽出（HTML パース）
- 読了時間の自動計算
- エラー時もアプリが停止しない構造

# 5. データ処理の流れ

## ● データ取得元
- Qiita（公開 API）
- Zenn（RSS）
- 技術系ブログの RSS

## ● データ構造（統一フォーマット）
- title
- summary
- category
- url
- source
- published_at

## ● 処理フロー
1. API / RSS にアクセス  
2. JSON / XML を解析  
3. 必要項目を抽出  
4. 統一フォーマットに整形  
5. ランダム表示ロジックに渡す  

# 6. UI の流れ（スクリーンショット）
`screenshots/` に格納

- 初期画面
- カテゴリ選択
- 記事一覧
- 本文表示
- 読了時間表示

# 7. テストで確認した内容（UI の流れに沿った形）

## ① 初期画面
- アプリが正常に起動し、カテゴリ選択 UI が表示されること
- データ取得エラーがあっても画面が落ちないこと

## ② カテゴリ選択
- 選択したカテゴリに応じて記事が取得されること
- API / RSS の取得が失敗してもアプリが停止しないこと

## ③ 記事一覧
- タイトル・概要・URL が正しく表示されること
- ランダム表示ロジックが意図通り動作すること
- 重複記事が表示されないこと

## ④ 本文表示
- HTML から本文が正しく抽出されること
- 不要タグが除去され、読みやすい形で表示されること

## ⑤ 読了時間表示
- 抽出した本文から読了時間が正しく計算されること
- 1件/2件の切り替えが意図通り動作すること

※ UI の各ステップ（初期画面 → カテゴリ選択 → 記事一覧 → 本文表示 → 読了時間表示）が意図通りに動作することを確認することで、アプリ全体が途切れなく動き、ユーザーが問題なく記事を閲覧できる品質を担保できる。

# 8. 使用技術
- Python
- Streamlit
- Requests / Feedparser
- BeautifulSoup4
- GitHub

# 9. フォルダ構成
```
/portfolio_python/
│
├─ README.md
├─ 学習まとめ.txt
│
├─ screenshots/
│   ├─ 01_initial/            # ① 初期画面（1枚）
│   │     └─ initial.png
│   │
│   ├─ 02_category/           # ② カテゴリ選択（2枚）
│   │     ├─ category_01.png
│   │     └─ category_02.png
│   │
│   ├─ 03_articles/           # ③ 記事一覧（6枚）
│   │     ├─ articles_01.png
│   │     ├─ articles_02.png
│   │     ├─ articles_03.png
│   │     ├─ articles_04.png
│   │     ├─ articles_05.png
│   │     └─ articles_06.png
│   │
│   ├─ 04_body/               # ④ 本文表示（1枚）
│   │     └─ body.png
│   │
│   └─ 05_readingtime/        # ⑤ 読了時間表示（2枚）
│         ├─ reading_01.png
│         └─ reading_02.png
│
└─ src/
├─ app.py
├─ config.py
├─ content_extractor.py
├─ data_fetcher.py
├─ fetch_qiita_articles.py
├─ fetch_zenn_articles.py
├─ fetcher_rss_articles.py
├─ normalize_article.py
└─ randomizer.py
```

# 10. 学習まとめ
※ 別紙 テキストファイル記載（1ページ）

# 11. 参考文献

■ 参考にした情報源（設計・実装の根拠）

### ● データ取得関連
Qiita API ドキュメント  
https://qiita.com/api/v2/docs

Zenn 公式 RSS フィード仕様  
https://zenn.dev/

一般的な RSS 仕様（W3C）  
https://validator.w3.org/feed/docs/rss2.html

### ● Python ライブラリ（データ処理・解析）
Requests（公式ドキュメント）  
https://requests.readthedocs.io/

Feedparser（公式ドキュメント）  
https://feedparser.readthedocs.io/

BeautifulSoup4（bs4）公式ドキュメント  
https://www.crummy.com/software/BeautifulSoup/bs4/doc/

### ● UI（Streamlit）
Streamlit 公式ドキュメント  
https://docs.streamlit.io/

### ● 設計・構造化の参考
Python のモジュール構成に関するベストプラクティス（Real Python）  
https://realpython.com/

例外処理・エラー処理のベストプラクティス（Python 公式）  
https://docs.python.org/3/tutorial/errors.html
