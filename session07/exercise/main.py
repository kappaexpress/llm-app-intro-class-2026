"""
チャットアプリ バックエンド - 第7回 (1会話・SQLite保存版)
LLMアプリケーション基礎

第6回からの変更点:
  - フロントが持っていた会話履歴を SQLite (chat.db) に移した
  - リロード・サーバ再起動しても会話が消えなくなった
  - まだ会話は1つだけ (conversations テーブルは無し)。次回追加する

このバックエンドは次の3つを担当します:
  1. SQLite の messages テーブルに会話履歴を保存する
  2. OpenAI API を呼んで AI の返答を取得する
  3. フロントエンド (static/) を配信する
"""

import sqlite3

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from openai import OpenAI
from pydantic import BaseModel, Field

# --- OpenAIクライアントの初期化 ---
# 環境変数 OPENAI_API_KEY を自動で読み取ってクライアントを作る
# 起動前にシェルで以下を実行してキーをセットしておくこと:
#   export OPENAI_API_KEY=sk-...
# (キーをコードに直接書かないこと。export は現在のシェルにのみ有効)
client = OpenAI()

# 使うモデル名 (GPT-5.4 クラスで最も安価。Reasoning 対応)
MODEL_NAME = "gpt-5.4-nano"

# Reasoning の強さ。"none" / "low" / "medium" / "high" / "xhigh"
# チャット用途では "none"〜"low" でコストとレイテンシを抑えるのが基本
REASONING_EFFORT = "low"

# システムプロンプト (AIの振る舞いを指示する文)
# 今回はまだ会話が1つだけなので、サーバ側の固定値で十分
# 第8回で会話ごとに変えられるよう DB に持たせる
DEFAULT_SYSTEM_PROMPT = (
    "あなたは親切で丁寧なアシスタントです。日本語で回答してください。"
)

# --- FastAPI アプリ ---
app = FastAPI(title="Chat App (session07)")

# CORS 設定 (開発しやすいように全許可)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- データベース設定 ---
# DB ファイルはアプリと同じディレクトリに chat.db として作られる
# このファイルを消すと履歴は全部リセットされる
DATABASE = "chat.db"


def init_db():
    """
    データベースとテーブルを初期化する
    アプリ起動時に1回だけ呼ぶ。

    IF NOT EXISTS なので、既に存在する場合は何もしない。
    つまり毎回安全に呼べる (起動のたびにテーブルが消えたりはしない)。
    """
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # メッセージテーブル: 1つの発言 = 1レコード
    #   role:       "user" または "assistant"
    #   content:    発言の本文
    #   created_at: 作成時刻 (省略時はDBが自動で現在時刻を入れる)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


# --- Pydantic モデル (リクエストボディの型) ---


class MessageCreate(BaseModel):
    """メッセージを送るときのリクエストボディ"""

    # 空文字はNG。長すぎるメッセージも弾く
    content: str = Field(min_length=1, max_length=4000)


# --- API エンドポイント ---


@app.get("/api/messages")
def get_messages():
    """
    保存されている全メッセージを古い順で返す。
    フロントはページロード時にこれを呼んで履歴を画面に並べる。
    """
    conn = sqlite3.connect(DATABASE)
    # row_factory を設定すると、結果を row["role"] のように列名で取り出せる
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, role, content, created_at
        FROM messages
        ORDER BY id
    """)
    rows = cursor.fetchall()

    conn.close()
    return [
        {
            "id": row["id"],
            "role": row["role"],
            "content": row["content"],
            "created_at": row["created_at"],
        }
        for row in rows
    ]


@app.post("/api/messages", status_code=201)
def send_message(user_message: MessageCreate):
    """
    ユーザーのメッセージを送り、AI の返答を受け取る。

    流れ:
      1. ユーザーメッセージを DB に保存
      2. DB から過去メッセージ全件を取り出す (たった今保存したものも含む)
      3. 先頭に system プロンプトを付けて OpenAI に送る
      4. AI の返答を DB に保存
      5. AI の返答を返す
    """
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # 1. ユーザーメッセージを DB に保存
    # ? プレースホルダを使うことで SQL インジェクションを防ぐ
    cursor.execute(
        "INSERT INTO messages (role, content) VALUES (?, ?)",
        ("user", user_message.content),
    )
    conn.commit()

    # 2. 過去メッセージを全件、古い順で取り出す
    cursor.execute("SELECT role, content FROM messages ORDER BY id")
    past_rows = cursor.fetchall()

    # 3. OpenAI API に渡す形式に組み立てる
    # 先頭に system を1つ + 過去のメッセージ全部
    messages_for_api = [
        {"role": "system", "content": DEFAULT_SYSTEM_PROMPT},
    ]
    for row in past_rows:
        messages_for_api.append({"role": row["role"], "content": row["content"]})

    # 4. OpenAI API を呼び出す
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages_for_api,
            reasoning_effort=REASONING_EFFORT,
        )
    except Exception as e:
        # API 呼び出し失敗時は 500 を返す
        conn.close()
        raise HTTPException(
            status_code=500,
            detail=f"AI APIの呼び出しに失敗しました: {e}",
        )

    # AI の返答テキストを取り出す
    assistant_content = response.choices[0].message.content

    # 5. AI の返答を DB に保存
    cursor.execute(
        "INSERT INTO messages (role, content) VALUES (?, ?)",
        ("assistant", assistant_content),
    )
    conn.commit()
    assistant_message_id = cursor.lastrowid

    conn.close()

    # 6. クライアントに返す
    return {
        "id": assistant_message_id,
        "role": "assistant",
        "content": assistant_content,
    }


# --- 静的ファイル配信 ---
# フロントエンド (static/index.html, style.css, app.js) を / で配信する
# 注意: "/" へのマウントはあらゆるURLにマッチするため、
# 必ずAPIエンドポイントの定義より「後」に書くこと(先に書くとAPIが呼べなくなる)
app.mount("/", StaticFiles(directory="static", html=True), name="static")


# --- アプリ起動時に DB を初期化 ---
# テーブルがまだ無ければ作る。あれば何もしない。
init_db()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
