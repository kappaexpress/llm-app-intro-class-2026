# 第7回 exercise — chat-app (1会話・SQLite保存版)

LLMアプリケーション基礎 - 第7回「履歴の永続化 (SQLite)」のスナップショット。

## このスナップショットの状態

- 単一会話のチャットアプリ
- 会話履歴は **SQLite (`chat.db`)** に保存される
- **ブラウザリロード・サーバ再起動しても会話が消えない**
- まだ複数会話の切り替えは無し (次回第8回で追加)

## 起動手順

1. プロジェクトルートで依存パッケージをインストール (一度だけ):

   ```bash
   pip install -r ../../requirements.txt
   ```

2. シェルに OpenAI API キーをセット (講師から配布されたキーを使う):

   ```bash
   export OPENAI_API_KEY=sk-...
   ```

   `export` は **現在のシェルにのみ** 有効。ターミナルを開き直したらもう一度やる。

3. このディレクトリに移動して起動:

   ```bash
   cd session07/exercise
   python main.py
   ```

4. ブラウザで <http://localhost:8000> を開く。

## 「消えないこと」を確認する手順

1. 起動してブラウザを開き、何往復か AI と会話する
2. **ブラウザのタブをリロード** (F5 / Cmd+R)
   → 過去の会話がそのまま表示される
3. ターミナルで **`Ctrl+C` でサーバを止める**
4. もう一度 `python main.py` で起動 → ブラウザをリロード
   → 過去の会話がまだ残っている

第6回の「メモリ保持」版だと 2 でも消えていたが、今回は残る。

## DB ファイル (`chat.db`)

- 初回起動時に **自動で作られる** (`init_db()` が `CREATE TABLE IF NOT EXISTS` を実行)
- このファイルを消すと履歴は完全にリセットされる
- `.gitignore` で除外されているので、コミット対象にはならない

## DB の中身を覗く

別ターミナルから:

```bash
# 全件表示
sqlite3 chat.db "SELECT * FROM messages;"

# 見やすく整形して
sqlite3 chat.db "SELECT id, role, substr(content, 1, 40), created_at FROM messages;"

# テーブル定義を確認
sqlite3 chat.db ".schema messages"
```

## ファイル構成

```
session07/exercise/
├── main.py              # FastAPI + SQLite + OpenAI 呼び出し
├── README.md            # このファイル
└── static/
    ├── index.html       # 1カラムのチャット画面 (サイドバー無し)
    ├── style.css        # スタイル
    └── app.js           # フロントのロジック (履歴はサーバ任せ)
```

## API エンドポイント

| メソッド | パス            | 役割                                                                                  |
| -------- | --------------- | ------------------------------------------------------------------------------------- |
| GET      | `/api/messages` | 保存されている全メッセージを古い順で返す                                              |
| POST     | `/api/messages` | ユーザー発言1件を受け取り、DB保存 → 過去全件を OpenAI に送る → AI返答をDB保存して返す |

Swagger UI (<http://localhost:8000/docs>) からも確認可能。

## トラブルシュート

- **`OPENAI_API_KEY` not set** → `export OPENAI_API_KEY=sk-...` を忘れていないか
- **`no such table: messages`** → `init_db()` の呼び出しを消していないか
- **「考え中...」のまま動かない** → サーバ側のターミナルで例外を確認 (キー間違い・残高切れなど)
- **会話をリセットしたい** → サーバを止めて `chat.db` を削除してから再起動
