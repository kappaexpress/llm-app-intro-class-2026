# LLMアプリケーション基礎 2026 — 講義計画

Webアプリケーション基礎 2026（TODOアプリ完成まで）を修了した受講生向けの続編。
LLMの基礎を学びながら、最終的に **複数会話の保存・切り替えができるシンプルなChatGPT風アプリ** を完成させる。

## コース全体方針

- **使用API**: OpenAI API（ChatGPT、`openai` Python SDK）
- **技術スタック**: 前コースを踏襲（FastAPI + Vanilla HTML/CSS/JS + SQLite）
- **最終成果物**: `chat-app/`
  - 会話一覧サイドバー、複数会話の新規作成・切替・削除
  - 会話履歴のSQLite永続化
  - システムプロンプトは内部対応（UIは最後20分で軽く紹介）
  - ストリーミング応答は **扱わない**
- **発展テーマ**（Tool use / Function calling / RAG / エージェント）は第8回最後の20分で **概念スライドのみ**
- **演習スタイル**: 各回 `session0X/exercise/` に、その回までで実装済みの chat-app スナップショットを置く（第3回除く）。受講生は前回の自分のコードから続けてもよいし、`exercise/` をコピーしてもよい

## ディレクトリ構成（予定）

```
llm-app-intro-class-2026/
├── lecture.md                # 本ファイル
├── requirements.txt          # fastapi, uvicorn, openai, python-dotenv
├── .gitignore                # .env, *.db, __pycache__
├── .devcontainer/            # postCreateCommand で pip install 済
├── knowledgebase/
│   └── web-app-intro-class-2026/  # 前コース教材（参照用）
├── chat-app/                 # 最終完成形（作成済み）
│   ├── main.py
│   ├── .env.example
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

| 回 | テーマ | exercise/ の状態 |
|---|---|---|
| 1 | LLM入門 / コース全体像 | なし（claude.ai / ChatGPT で体感） |
| 2 | プロンプトエンジニアリング | プロンプト集（テキストのみ） |
| 3 | 復習回（Web基礎） | 復習用ミニアプリ |
| 4 | OpenAI APIに初めて触れる | CLIスクリプト（`python chat.py`） |
| 5 | FastAPIでChatバックエンド | chat-app の **バックエンドのみ** 版 |
| 6 | チャットUI + マルチターン会話 | chat-app の **1会話・メモリ保持** 版 |
| 7 | 履歴の永続化（SQLite） | chat-app の **1会話・DB保存** 版 |
| 8 | 複数会話の切り替え + 仕上げ | **chat-app 完成版** |

---

## 第1回: LLM入門 / コース全体像

### ゴール
LLMが何をする道具なのかを掴み、このコースで作るものをイメージできる

### 前半
- コース全体像と最終成果物のデモ（完成版 chat-app を見せる）
- LLMとは何か — 言語モデル、次のトークンを予測する仕組み
- トークン・コンテキストウィンドウの直感
- 知識カットオフ、ハルシネーション

### 後半
- 主要モデルの俯瞰（ChatGPT / Claude / Gemini）と特徴
- LLMの得意/不得意
- ChatGPT のWeb版を実際に触る
- 第2回以降の流れ説明

### 演習
- ChatGPT に色々な質問を投げてみて、得意/不得意を体感する

---

## 第2回: プロンプトエンジニアリング

### ゴール
良い結果を出すプロンプトの書き方を、コードを書く前に「言葉で」マスターする

### 前半
- プロンプトとは / 良いプロンプトと悪いプロンプト
- 役割の指示（「あなたは〜です」）
- 具体的な指示・出力フォーマット指定

### 後半
- system プロンプトと user プロンプトの違い（概念）
- Few-shot プロンプト（例を見せる）
- 構造化出力（JSON で返させる）
- Chain of Thought の触り

### 演習
- ChatGPT 上でプロンプト改善ワーク（同じ目的を達成するプロンプトを3パターン書いて比較）

---

## 第3回: 復習回（Web基礎）

### ゴール
コーディングを再開する前に、前コースで扱った FastAPI / fetch / SQLite を思い出す
（LLMはこの回ではまだ扱わず、純粋にWeb基礎の復習に集中する）

### 前半
- 開発環境の起動確認（Codespaces / devcontainer）
- FastAPI のおさらい — 最小Hello、`POST` + Pydantic
- フロントからの fetch / async-await のおさらい

### 後半
- SQLite のおさらい — `sqlite3` モジュールの使い方
- ミニ演習: 受け取った文字列をオウム返しする `/api/echo` を作って、フロントから fetch で呼ぶ

### 演習
- echo API + 簡易UI を完成させる（OpenAI API はまだ使わない）

---

## 第4回: OpenAI APIに初めて触れる

### ゴール
Python から OpenAI API を呼んで返答が返ってくる体験をする

### 前半
- OpenAI APIの概要 / 料金体系の概要
- APIキーの取得方法
- **APIキーの安全な管理①** — `.env` ファイル / `python-dotenv` / `.gitignore`
- `pip install openai`

### 後半
- 最小スクリプトで1往復（`chat.completions.create`）
- `model` / `messages` / `max_tokens` / `temperature` の意味
- トークン消費とコストの見方
- 「やってはいけないこと」: GitHubにキーを上げる、フロントに直接書く

### 演習
- ターミナルから対話するCLIスクリプトを書く（`python chat.py`）

---

## 第5回: FastAPIでChatバックエンドを作る

### ゴール
OpenAI APIをFastAPIでラップし、HTTP経由でAIに話しかけられるようにする

### 前半
- なぜバックエンド経由にする必要があるか（**APIキー保護②**）
- `POST /api/chat` の設計
- Pydantic でリクエスト/レスポンスを定義

### 後半
- 環境変数からAPIキーを読む
- エラーハンドリング（API失敗時の500応答）
- Swagger UI で動作確認
- フロントエンドに **絶対にAPIキーを渡さない** 設計の確認

### 演習
- `POST /api/chat` を実装し、Swagger UI から動作確認する

### exercise/ の状態
- chat-app のバックエンドだけが動く状態（フロントエンドはまだ空 or プレースホルダ）

---

## 第6回: チャットUI + マルチターン会話

### ゴール
ブラウザで動くチャット画面を作り、AIが「前の発言を覚えている」状態を実現する

### 前半
- チャットUIの設計（メッセージバブル、入力欄）
- HTML/CSS でチャット画面を組む
- fetch でバックエンドに送って表示する（1往復）

### 後半
- マルチターン会話の概念 — `messages` 配列に履歴を積む
- フロント側で履歴を保持し、毎回まるごと送る
- コンテキストウィンドウの限界の話

### 演習
- 1会話の中で過去の発言を踏まえた応答ができる状態まで仕上げる

### exercise/ の状態
- chat-app: 1会話・メモリ保持（リロードで消える）

---

## 第7回: 履歴の永続化（SQLite）

### ゴール
サーバを再起動しても会話履歴が消えないようにする

### 前半
- なぜ永続化が必要か
- DBスキーマ設計 — `messages` テーブル（id, role, content, created_at）
- `init_db()` でテーブル作成

### 後半
- メッセージ送信時にDBに保存（user / assistant 両方）
- 起動時に過去メッセージを読み込んで表示
- 過去メッセージを `messages` 配列に詰めてAPIに送る

### 演習
- リロード／再起動しても会話が残る状態にする

### exercise/ の状態
- chat-app: 1会話・SQLite保存

---

## 第8回: 複数会話の切り替え + 仕上げ

### ゴール
ChatGPT風の「複数会話を切り替えて使える」アプリを完成させる

### 前半（メインテーマ）
- `conversations` テーブルを追加（id, title, created_at）
- `messages` に `conversation_id` 外部キー
- API追加: 会話一覧/作成/削除、会話ごとのメッセージ取得
- サイドバーUI（会話一覧 / 新しい会話ボタン / 削除）

### 後半（メインテーマ）
- 会話の切り替えとアクティブ表示
- 削除確認、空状態の表示
- chat-app 完成形のレビュー

### 最後20分（軽め）
- システムプロンプトでペルソナを変える（`conversations` に `system_prompt` カラム、デフォルト値で運用）
- 発展テーマの **概念スライドのみ** 紹介:
  - Tool use / Function calling — AIにツールを使わせる
  - RAG（Retrieval Augmented Generation）— 自分のドキュメントを参照させる
  - エージェント — 自律的にタスクを進めるLLM
- このコース修了後に何ができるようになったか、次に何を学ぶといいか

### exercise/ の状態
- chat-app 完成版（このリポジトリ直下の `chat-app/` と同じ内容）
