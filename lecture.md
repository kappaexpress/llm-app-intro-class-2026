# LLMアプリケーション基礎 — 講義計画

Webアプリケーション基礎 2026（TODOアプリ完成まで）を修了した受講生向けの続編。
LLMの基礎を学びながら、最終的に **複数会話の保存・切り替えができるシンプルなChatGPT風アプリ** を完成させる。

## コース全体方針

- **使用API**: OpenAI API（`openai` Python SDK）
- **使用モデル**: `gpt-5.4-nano`（[公式ドキュメント](https://developers.openai.com/api/docs/models/gpt-5.4-nano)）
  - GPT-5.4 クラスで最も安価。分類・抽出・チャットなど高ボリュームな用途向け
  - 入力 $0.20 / 出力 $1.25（1Mトークン）、コンテキスト 400K、最大出力 128K
  - **Reasoning（推論）対応モデル** — 必要に応じて「考えてから答える」モードを使える
- **技術スタック**: 前コースを踏襲（FastAPI + Vanilla HTML/CSS/JS + SQLite）
- **最終成果物**: `chat-app/`
  - 会話一覧サイドバー、複数会話の新規作成・切替・削除
  - 会話履歴のSQLite永続化
  - システムプロンプトは内部対応（UIは最後20分で軽く紹介）
  - ストリーミング応答は **扱わない**
- **発展テーマ**（Tool use / Function calling / RAG / エージェント）は第8回最後の20分で **概念スライドのみ**
- **APIキー**: **講師から配布**する方式（受講生個人での取得は不要）。配布されたキーは `python main.py` 起動前にシェルで `export OPENAI_API_KEY=sk-...` として環境変数にセットして使う(`.env` は使わない方針)。絶対に外部共有・コミットしない。講師側は OpenAI ダッシュボードで月予算上限を設定して暴走を防ぐ運用とする
- **演習スタイル**: 各回 `session0X/exercise/` に、その回までで実装済みの chat-app スナップショットを置く（第3回除く）。受講生は前回の自分のコードから続けてもよいし、`exercise/` をコピーしてもよい

## ディレクトリ構成（予定）

```
llm-app-intro-class-2026/
├── lecture.md                # 本ファイル
├── requirements.txt          # fastapi, uvicorn, openai
├── .gitignore                # *.db, __pycache__
├── .devcontainer/            # postCreateCommand で pip install 済
├── knowledgebase/
│   └── web-app-intro-class-2026/  # 前コース教材（参照用）
├── chat-app/                 # 最終完成形（作成済み）
│   ├── main.py
│   └── static/
│       ├── index.html
│       ├── style.css
│       └── app.js
├── your-app/                 # 受講生が育てる作業用
├── share-images/             # 共有画像（必要に応じて）
├── session01/
│   ├── slides.md
│   └── images/
├── session02/
│   ├── slides.md
│   ├── exercise/             # プロンプト集（テキスト）
│   └── images/
├── session03/
│   ├── slides.md
│   ├── exercise/             # 復習用ミニアプリ
│   └── images/
├── session04/
│   ├── slides.md
│   ├── exercise/             # CLIスクリプト
│   └── images/
├── session05/
│   ├── slides.md
│   ├── exercise/             # chat-app: backend only
│   └── images/
├── session06/
│   ├── slides.md
│   ├── exercise/             # chat-app: 1会話・メモリ保持
│   └── images/
├── session07/
│   ├── slides.md
│   ├── exercise/             # chat-app: 1会話・SQLite保存
│   └── images/
└── session08/
    ├── slides.md
    ├── exercise/             # chat-app: 完成形
    └── images/
```

## 8回構成一覧
