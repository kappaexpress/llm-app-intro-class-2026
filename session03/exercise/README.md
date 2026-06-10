# 第3回 演習: Echo API + 簡易UI

入力した文字列をサーバーがそのまま返すだけのミニアプリ。
**LLM / OpenAI API はまだ使いません。** 前コースで触った FastAPI + fetch を思い出すための復習回です。

## ファイル構成

```
exercise/
├── main.py              # FastAPI バックエンド
├── static/
│   ├── index.html       # 入力フォーム + 応答表示
│   ├── style.css
│   └── app.js           # fetch で /api/echo を呼ぶ
└── README.md            # このファイル
```

## 起動方法

このディレクトリに移動して、`python main.py` を実行するだけ。

```bash
cd session03/exercise
python main.py
```

サーバーが起動したら、Codespaces のポート 8000 をブラウザで開く。

> **OpenAI APIキーは不要です。** この回ではまだ LLM を呼びません。
> `export OPENAI_API_KEY=...` も **やる必要なし**。

## 動作確認

1. ブラウザで開いた画面に文字列を入力して「送信」を押す
2. 入力した文字列がそのまま「サーバーからの応答」に表示される
3. DevTools の Network タブで `/api/echo` への POST と JSON レスポンスを確認

curl でも叩ける。

```bash
curl -X POST http://localhost:8000/api/echo \
  -H "Content-Type: application/json" \
  -d '{"message": "こんにちは"}'
# => {"echo":"こんにちは"}
```

Swagger UI は `http://localhost:8000/docs` から見られる。

## 思い出しポイント

- `FastAPI()` のインスタンスを作ると、`@app.post(...)` でルートを定義できる
- `BaseModel` を継承してリクエストの型を書くと、JSON のパースとバリデーションが自動
- フロントは `fetch(url, { method, headers, body })` で叩く。`await res.json()` でJSONを取り出す
- 表示時は **`textContent`** を使う(XSS対策)
- `StaticFiles` を `/` にマウントすることで `index.html` を直接配信できる
