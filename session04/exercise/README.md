# 第4回 演習: OpenAI APIに初めて触れる

Pythonから OpenAI API を呼んで、ターミナルで AI と対話できる CLI を作ります。

## 事前準備

### 1. ライブラリのインストール

devcontainer を使っていれば既に入っています。手元で確認:

```bash
python -c "import openai; print(openai.__version__)"
```

入っていなければ:

```bash
pip install openai
```

### 2. APIキーをシェルの環境変数にセット

講師から配布された APIキーをシェルで `export` します。

```bash
export OPENAI_API_KEY=sk-...   # ← 配布されたキーをここに
```

> [!IMPORTANT]
>
> - `export` は **今開いているシェルにのみ** 有効です。新しいターミナルを開いたら再度実行してください。
> - APIキーは **絶対にコードに書かない / git にコミットしない / 他人に共有しない** こと。
> - `.env` ファイル方式は本コースでは使いません(コミット事故を避けるため、毎回手で `export` する運用に統一しています)。

セットできたか確認:

```bash
echo $OPENAI_API_KEY
# sk-... と表示されればOK
```

## 各スクリプトの説明

### `one_shot.py` — 最小スクリプト(1往復)

一番シンプルな例。AI に1回だけ話しかけて返答とトークン消費量を表示する。

```bash
python one_shot.py
```

これが動けば「自分のコードから LLM を呼ぶ」第一歩クリア。

### `chat.py` — CLIチャット(マルチターン)

ターミナルから AI と対話できるスクリプト。`messages` 配列に履歴を積んでいくので、AI は前の発言を覚えている。

```bash
python chat.py
```

```
あなた: こんにちは
AI: こんにちは!今日はどうしましたか?
あなた: Pythonの内包表記を教えて
AI: Pythonの内包表記は ...
あなた: さっきの例で偶数だけ取り出すには?
AI: 先ほどの内包表記に if を足すと ...    ← 前の発言を覚えている
あなた: exit
```

終了するには:

- `exit` と入力する
- `Ctrl+C` を押す

### `reasoning_demo.py` — Reasoning 体感デモ

同じ難問を `reasoning_effort="none"` と `"high"` の両方で投げて、

- レイテンシ
- トークン消費量(推論トークンも含む)
- 回答の質

の差を比較する。

```bash
python reasoning_demo.py
```

**観察ポイント:**

- `high` のほうが時間がかかる
- `high` のほうがトークン(特に reasoning_tokens)を多く消費する
- そのぶん難しい問題には強い

> チャット用途は基本 `none` か `low` で十分。難しい質問だけ `high`/`xhigh`、が定番の使い分け。

## トラブルシューティング

### `openai.AuthenticationError`

APIキーがセットされていない、または間違っています。

```bash
echo $OPENAI_API_KEY   # 空ならセットされていない
export OPENAI_API_KEY=sk-...
```

### ターミナルを開き直したら動かなくなった

`export` は現在のシェルにのみ有効です。新しいターミナルでは再度 `export` してください。これは仕様です(キーがファイルに残らない安全側の運用)。

### `ModuleNotFoundError: No module named 'openai'`

`pip install openai` を実行してください。

## 使用モデル

`gpt-5.4-nano` を使います。

- 入力 $0.20 / 出力 $1.25(1Mトークン)
- コンテキスト 400K / 最大出力 128K
- Reasoning 対応(`none` / `low` / `medium` / `high` / `xhigh`)
