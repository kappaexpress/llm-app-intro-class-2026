# 第8回 exercise — chat-app 完成版

LLMアプリケーション基礎 の最終回 (第8回) 時点での chat-app スナップショットです。
リポジトリ直下の `chat-app/` と同じ内容になっています。

## このバージョンでできること

- **複数会話の管理**: 左のサイドバーに会話一覧。新規作成・切り替え・削除が可能
- **会話ごとの履歴**: 各会話に紐づくメッセージを SQLite に永続化
- **マルチターン会話**: 過去のやり取りを全部 OpenAI API に渡すので、AI は文脈を覚えている
- **会話ごとのシステムプロンプト**: `conversations.system_prompt` カラムを持つ (デフォルト値で運用)
- **Reasoning モード**: `gpt-5.4-nano` の `reasoning_effort` を設定可能 (デフォルト `low`)
- **エラー表示 / 削除確認 / 空状態の表示** 等の仕上げ済み

## 起動方法

### 1. 依存パッケージのインストール (初回のみ)

```bash
pip install -r ../../requirements.txt
```

(devcontainer を使っている場合は `postCreateCommand` で済んでいます)

### 2. OpenAI API キーをシェルにエクスポート

```bash
export OPENAI_API_KEY=sk-...     # 講師から配布されたキー
```

`export` は **現在のシェルにのみ** 有効です。ターミナルを開き直したらやり直してください。
**コード中に直書きしない / コミットしない** こと。

### 3. 起動

```bash
cd session08/exercise
python main.py
```

ブラウザで http://localhost:8000 にアクセス。

## ファイル構成

```
session08/exercise/
├── main.py            # FastAPI バックエンド (会話 + メッセージ API)
├── static/
│   ├── index.html     # サイドバー + チャット画面
│   ├── style.css      # 2カラムレイアウトのスタイル
│   └── app.js         # 会話の取得/作成/削除/切替 + メッセージ送信
└── chat.db            # 起動時に自動生成される SQLite データベース (gitignore 推奨)
```

## 第8回で追加された機能

第7回 (1会話・SQLite保存) からの差分:

1. **`conversations` テーブルの追加**
   - `id`, `title`, `system_prompt`, `created_at`
2. **`messages` テーブルに `conversation_id` 外部キーを追加**
   - 各メッセージがどの会話に属するかを保持
3. **新しい API エンドポイント**
   - `GET    /api/conversations` — 一覧
   - `POST   /api/conversations` — 新規作成
   - `DELETE /api/conversations/{id}` — 削除 (中のメッセージも一緒に削除)
   - `GET    /api/conversations/{id}/messages` — その会話のメッセージ一覧
   - `POST   /api/conversations/{id}/messages` — メッセージ送信 + AI 返答
4. **サイドバー UI**
   - 会話一覧表示・新規作成ボタン・削除ボタン・アクティブ表示
5. **フロントの状態管理**
   - `currentConversationId` で今どの会話を見ているかを保持
6. **削除確認 / 空状態 / エラー表示**

## API 仕様 (概要)

| メソッド | パス                               | 役割                                  |
| -------- | ---------------------------------- | ------------------------------------- |
| GET      | `/api/conversations`               | 会話一覧 (新しい順)                   |
| POST     | `/api/conversations`               | 新しい会話を作成                      |
| DELETE   | `/api/conversations/{id}`          | 会話を削除 (メッセージも一緒に)       |
| GET      | `/api/conversations/{id}/messages` | その会話のメッセージ一覧 (古い順)     |
| POST     | `/api/conversations/{id}/messages` | メッセージを送り、AI の返答を受け取る |

詳細は起動後に http://localhost:8000/docs (Swagger UI) で確認できます。

## カスタマイズのヒント

- **ペルソナを変える**: 会話作成時に `system_prompt` を指定すれば、その会話だけ別の人格にできる
  ```bash
  curl -X POST http://localhost:8000/api/conversations \
    -H "Content-Type: application/json" \
    -d '{"title": "コード相談", "system_prompt": "あなたは経験豊富なPython専門家です。"}'
  ```
- **Reasoning を上げる**: `main.py` の `REASONING_EFFORT = "low"` を `"high"` や `"xhigh"` に変えるだけで、難しい質問への回答品質が変わる (その分レイテンシ・コストは上がる)
- **モデルを変える**: `MODEL_NAME` を別のモデル ID に差し替えるだけで切り替え可能
