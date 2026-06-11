# LLMアプリケーション基礎 2026

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/kappaexpress/llm-app-intro-class-2026)

Webアプリケーション基礎 2026 の続編。LLMの基礎を学びながら、最終的に
**複数会話の保存・切り替えができるシンプルなChatGPT風アプリ**(`chat-app/`)を完成させる全8回のコースです。

- 講義計画の詳細: [lecture.md](lecture.md)
- 技術スタック: FastAPI + Vanilla HTML/CSS/JS + SQLite + OpenAI API(`gpt-5.4-nano`)

---

## 初回だけ: Codespace を作る

1. 上の **Open in GitHub Codespaces** バッジをクリック(または リポジトリの `Code` → `Codespaces` → `Create codespace on main`)
2. VS Code が開いて環境構築が終わるまで待つ(必要なライブラリは自動でインストールされます。手動の `pip install` は不要)
3. 2回目以降は新しく作らず、同じ Codespace を **再開** して使う

## 毎回の授業のはじめかた

毎回この手順で始めます。

### 1. ターミナルを開く

`` Ctrl + ` ``(バッククォート)でターミナルを開く。

### 2. 今日の教材を作業フォルダにコピーする(任意)

前回の自分のコードの続きから進めてもOK。最初から揃った状態で始めたいときは、
その回のスナップショットを `your-app/` にコピーする:

```bash
# 例: 第6回の場合
cp -r session06/exercise/* your-app/
```

### 3. APIキーをセットする(第4回以降)

講師から配布されたキーをターミナルで環境変数にセットする:

```bash
export OPENAI_API_KEY=sk-...
```

- `export` は **今開いているターミナルにのみ** 有効。ターミナルを開き直したら毎回やり直す
- キーは他人に見せない・送らない・コードに書かない・コミットしない
- `.env` ファイルは本コースでは使わない

セットできたか確認:

```bash
echo $OPENAI_API_KEY
```

### 4. アプリを起動する

```bash
cd your-app
python main.py
```

ポート8000が転送され、ブラウザが自動で開きます。
(第4回だけはサーバではなくCLIスクリプト: `python chat.py` など)

## 各回の教材

| 回 | テーマ | 演習教材と動かし方 |
|---|---|---|
| 1 | LLM入門 / コース全体像 | `session01/exercise/` — ChatGPT / claude.ai 上で体感(コードなし) |
| 2 | プロンプトエンジニアリング | `session02/exercise/` — プロンプト集。ChatGPT 上でワーク |
| 3 | 復習回(Web基礎) | `session03/exercise/` — 復習用ミニアプリ。`python main.py`(APIキー不要) |
| 4 | OpenAI APIに初めて触れる | `session04/exercise/` — CLIスクリプト。`python one_shot.py` → `python chat.py` |
| 5 | FastAPIでChatバックエンド | `session05/exercise/` — バックエンドのみ。`python main.py` → ブラウザで `/docs` |
| 6 | チャットUI + マルチターン | `session06/exercise/` — 1会話・メモリ保持版。`python main.py` |
| 7 | 履歴の永続化(SQLite) | `session07/exercise/` — 1会話・DB保存版。`python main.py` |
| 8 | 複数会話の切り替え + 仕上げ | `session08/exercise/` — 完成形(`chat-app/` と同じ)。`python main.py` |

各 `exercise/` の中の `README.md` に、その回の詳しい手順が書いてあります。

## 授業が終わったら

1. サーバを `Ctrl + C` で停止する
2. Codespace を **Stop** する(左下の `Codespaces` メニュー → `Stop Current Codespace`)
   - 起動したまま放置すると無料枠(コア時間)を消費し続けます

## うまく動かないとき

### 「AI APIの呼び出しに失敗しました」/ `AuthenticationError`(500エラー)

APIキーが未セットかタイポ。`echo $OPENAI_API_KEY` で確認して `export` をやり直し、サーバを再起動する。

### ターミナルを開き直したら動かなくなった

`export` は前のターミナルにしか効いていない。新しいターミナルでもう一度 `export OPENAI_API_KEY=sk-...` する。

### コードを変えたのに画面が変わらない

1. ファイルを保存したか確認(タブに ● が付いていたら未保存)
2. `python main.py` は自動で再読み込みしない。`Ctrl + C` で止めてもう一度起動する
3. ブラウザをリロードする

### `Address already in use`(ポート8000が使用中)

別のターミナルでサーバが起動したまま。そちらを `Ctrl + C` で止める。見つからないときは:

```bash
pkill -f "python main.py"
```

### `ModuleNotFoundError: No module named 'openai'` など

ライブラリが入っていない。手動でインストールする:

```bash
pip install --break-system-packages -r requirements.txt
```

### チャット履歴(DB)を最初からやり直したい

サーバを止めてからDBファイルを消す。次回起動時に空のDBが自動で作り直される:

```bash
rm chat.db
```

---

## 講師向けメモ: Prebuilds の設定

Codespace の初回ビルド(数分)を授業前に済ませておくと、受講生は数十秒で起動できます。

1. GitHub のリポジトリページ → `Settings` → `Codespaces`
2. `Set up prebuild` をクリック
3. Branch: `main`、Region は受講生に近いリージョンを選択、トリガーは既定(push毎)のままでOK
4. `pip install` は `onCreateCommand` で実行されるため、ライブラリのインストールまで Prebuild に含まれます
