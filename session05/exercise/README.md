# 第5回 演習: FastAPI で Chat バックエンド

LLMアプリケーション基礎 - 第5回のスナップショット。
**バックエンドのみ** 動く状態。フロントエンドは第6回で実装する。

## このディレクトリの内容

```
exercise/
├── main.py              # FastAPI アプリ本体 (POST /api/chat)
├── static/
│   ├── index.html       # プレースホルダ (第6回で書き換える)
│   └── style.css        # プレースホルダ用の最小スタイル
└── README.md            # このファイル
```

## 起動手順

### 1. APIキーを環境変数にセット

ターミナルで以下を実行 (講師から配布されたキーを使う):

```bash
export OPENAI_API_KEY=sk-...
```

注意:

- `export` は **現在のシェルにのみ** 有効。ターミナルを開き直したら毎回必要
- `.env` ファイル方式は本コースでは **使わない**
- コミットしない・他人に見せない

セットされているか確認:

```bash
echo $OPENAI_API_KEY
```

### 2. サーバを起動

```bash
python main.py
```

`http://localhost:8000` で待ち受け開始。

## Swagger UI で動作確認

1. ブラウザで http://localhost:8000/docs を開く
2. `POST /api/chat` をクリックして展開
3. **Try it out** ボタンを押す
4. Request body を編集:

   ```json
   { "message": "こんにちは" }
   ```

5. **Execute** を押す
6. 下の Response 欄に AI の返答が表示されることを確認

レスポンス例:

```json
{
  "reply": "こんにちは!何かお手伝いできることはありますか?"
}
```

## エラー時の確認

わざとキーを無効にして起動すると 500 が返ることを確認できる:

```bash
export OPENAI_API_KEY=sk-invalid-key
python main.py
```

Swagger UI で叩くと:

```json
{
  "detail": "AI APIの呼び出しに失敗しました: ..."
}
```

## 第5回時点での制約

- 会話履歴は持たない (毎回単発)
- DBも無い
- フロント (チャット画面) は無い (プレースホルダのみ)

→ これらは第6回以降で順次追加していく。

## 次回 (第6回) でやること

- HTML/CSS でチャット画面を作る
- `fetch` で `/api/chat` を呼んで画面に表示
- 会話履歴をフロント側に持ち、毎回まるごと送る (マルチターン化)
