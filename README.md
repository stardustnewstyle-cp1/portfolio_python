※ 本 README は成果物の説明を目的としており、pythonの学習成果は別紙「学習まとめ.txt」に記載している。

1. アプリ名
技術記事ランダム表示アプリ
2. このアプリを作った目的
本アプリは、Python を実務レベルで習得するための自己学習の一環として、外部データ取得・データ整形・ロジック実装・UI 表示までを一連で実装することを目的として開発した。  
この構成にすることで、API 連携、データ処理、HTML 解析、例外処理、UI 構築など、Python の基礎〜応用を体系的に学習できるように設計している。
そのうえで、アプリとして以下の価値を提供する。

・技術情報に自然に触れられる仕組みを提供する

・Qiita / Zenn / 技術系 RSS から信頼性の高い情報を取得する

・ランダム表示により、普段触れない分野にも目が向くようにする

3. アプリの概要
本アプリは、Qiita・Zenn・技術系 RSS から技術記事を取得し、カテゴリ選択 → 記事一覧 → 本文表示 → 読了時間表示
という流れで技術記事をランダム閲覧できる。

・公開 API / RSS のみを利用

・取得データを統一フォーマットに整形

・Streamlit によるシンプルな UI

・HTML から本文を抽出し、読了時間を推定

・1〜2件の技術記事をランダムに表示

4. 機能
技術記事のランダム表示

カテゴリ選択

記事カード表示（タイトル・概要・URL）

本文抽出（HTML パース）

読了時間の自動計算

エラー時もアプリが停止しない構造

5. データ処理の流れ
● データ取得元
Qiita（公開 API）

Zenn（RSS）

技術系ブログの RSS

● データ構造（統一フォーマット）
title

summary

category

url

source

published\_at

● 処理フロー
API / RSS にアクセス

JSON / XML を解析

必要項目を抽出

統一フォーマットに整形

ランダム表示ロジックに渡す

6. UI の流れ（スクリーンショット）
screenshots/ に格納

初期画面

カテゴリ選択

記事一覧

本文表示

読了時間表示

7.テストで確認した内容（UI の流れに沿った形）
① 初期画面
アプリが正常に起動し、カテゴリ選択 UI が表示されること

データ取得エラーがあっても画面が落ちないこと

② カテゴリ選択
選択したカテゴリに応じて記事が取得されること

API / RSS の取得が失敗してもアプリが停止しないこと

③ 記事一覧
タイトル・概要・URL が正しく表示されること

ランダム表示ロジックが意図通り動作すること

重複記事が表示されないこと

④ 本文表示
HTML から本文が正しく抽出されること

不要タグが除去され、読みやすい形で表示されること

⑤ 読了時間表示
抽出した本文から読了時間が正しく計算されること

1件/2件の切り替えが意図通り動作すること

※ UI の各ステップ（初期画面 → カテゴリ選択 → 記事一覧 → 本文表示 → 読了時間表示）が意図通りに動作することを確認することで、アプリ全体が途切れなく動き、
ユーザーが問題なく記事を閲覧できる品質を担保できる。

8. 使用技術
Python

Streamlit

Requests / Feedparser

BeautifulSoup4

GitHub

フォルダ構成
/portfolio\_python/
│
├─ README.md
├─ 学習まとめ.txt
│
├─ screenshots/
│   ├─ 01\_initial/            # ① 初期画面（1枚）
│   │     └─ initial.png
│   │
│   ├─ 02\_category/           # ② カテゴリ選択（2枚）
│   │     ├─ category\_01.png
│   │     └─ category\_02.png
│   │
│   ├─ 03\_articles/           # ③ 記事一覧（6枚）
│   │     ├─ articles\_01.png
│   │     ├─ articles\_02.png
│   │     ├─ articles\_03.png
│   │     ├─ articles\_04.png
│   │     ├─ articles\_05.png
│   │     └─ articles\_06.png
│   │
│   ├─ 04\_body/               # ④ 本文表示（1枚）
│   │     └─ body.png
│   │
│   └─ 05\_readingtime/        # ⑤ 読了時間表示（2枚）
│         ├─ reading\_01.png
│         └─ reading\_02.png
│
└─ src/

&#x20;    ├─ app.py

&#x20;    ├─ config.py

&#x20;    ├─ content\_extractor.py

&#x20;    ├─ data\_fetcher.py

&#x20;    ├─ fetch\_qiita\_articles.py

&#x20;    ├─ fetch\_zenn\_articles.py

&#x20;    ├─ fetcher\_rss\_articles.py 

&#x20;    ├─ normalize\_article.py    

&#x20;    └─ randomizer.py

10.学習まとめ
※ 別紙 PDF（1ページ）

11.参考文献

■ 参考にした情報源（設計・実装の根拠）
本アプリの要件定義および全体設計を行うにあたり、以下の公式ドキュメントおよび技術記事を参考にした。

● データ取得関連
Qiita API ドキュメント  
　API 仕様、レスポンス構造、パラメータの確認に使用
　https://qiita.com/api/v2/docs (qiita.com in Bing)

Zenn 公式 RSS フィード仕様  
　RSS 形式の構造理解、XML パースの確認に使用
　https://zenn.dev/

一般的な RSS 仕様（W3C）  
　RSS 2.0 のフィールド構造の理解に使用
　https://validator.w3.org/feed/docs/rss2.html (validator.w3.org in Bing)

● Python ライブラリ（データ処理・解析）
Requests（公式ドキュメント）  
　API への HTTP アクセス方法の確認
　https://requests.readthedocs.io/

Feedparser（公式ドキュメント）  
　RSS の解析方法の確認
　https://feedparser.readthedocs.io/

BeautifulSoup4（bs4）公式ドキュメント  
　HTML 解析、タグ抽出、不要要素の除去方法の確認
　https://www.crummy.com/software/BeautifulSoup/bs4/doc/ (crummy.com in Bing)

● UI（Streamlit）
Streamlit 公式ドキュメント  
　UI コンポーネント、レイアウト、Expander の使い方の確認
　https://docs.streamlit.io/

● 設計・構造化の参考
Python のモジュール構成に関するベストプラクティス（Real Python）  
　ファイル分割、責務分離の考え方の参考
　https://realpython.com/

例外処理・エラー処理のベストプラクティス（Python 公式）  
　try/except の設計、例外の種類の理解
　https://docs.python.org/3/tutorial/errors.html (docs.python.org in Bing)

