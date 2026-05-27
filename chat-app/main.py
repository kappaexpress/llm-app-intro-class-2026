"""
チャットアプリ バックエンド - 完成版
LLMアプリケーション基礎 2026 - 第8回まで実装した最終形

このバックエンドは次の3つを担当します:
  1. SQLiteに会話とメッセージを保存する
  2. OpenAI APIを呼んでAIの返答を取得する
  3. フロントエンド(static/)を配信する
"""

import sqlite3
from contextlib import contextmanager

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

# 使うモデル名(GPT-5.4 クラスで最も安価。Reasoning 対応)
MODEL_NAME = "gpt-5.4-nano"

# Reasoning の強さ。"none" / "low" / "medium" / "high" / "xhigh"
# チャット用途では "none"〜"low" でコストとレイテンシを抑えるのが基本
# "none" は推論を完全にスキップする最速モード
REASONING_EFFORT = "low"

# デフォルトのシステムプロンプト(AIの振る舞いを指示する文)
DEFAULT_SYSTEM_PROMPT = (
    "あなたは親切で丁寧なアシスタントです。日本語で回答してください。"
)

# --- FastAPIアプリ ---
app = FastAPI(title="Chat App")

# CORS設定(開発しやすいように全許可)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- データベース設定 ---
DATABASE = "chat.db"


def init_db():
    """データベースとテーブルを初期化する"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # 会話テーブル: 1つのチャット会話を表す
    # 例: { id: 1, title: "Pythonの質問", system_prompt: "...", created_at: "..." }
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            system_prompt TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # メッセージテーブル: 各会話の中の1つの発言
    # role は "user" か "assistant"
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conversation_id INTEGER NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (conversation_id) REFERENCES conversations(id)
        )
    """)

    conn.commit()
    conn.close()


@contextmanager
def get_db_connection():
    """データベース接続をコンテキストマネージャで管理する"""
    conn = sqlite3.connect(DATABASE)
    # 結果を辞書のように扱えるようにする
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


# --- Pydanticモデル(リクエストボディの型) ---


class ConversationCreate(BaseModel):
    """新しい会話を作るときのリクエストボディ"""

    # title は省略可能。指定がなければ「新しい会話」になる
    title: str = Field(default="新しい会話", max_length=100)
    # system_prompt も省略可能。デフォルトを使う
    system_prompt: str = Field(default=DEFAULT_SYSTEM_PROMPT, max_length=2000)


class MessageCreate(BaseModel):
    """メッセージを送るときのリクエストボディ"""

    content: str = Field(min_length=1, max_length=4000)


# --- APIエンドポイント: 会話 ---


@app.get("/api/conversations")
def get_conversations():
    """会話の一覧を取得する(新しい順)"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, title, created_at
            FROM conversations
            ORDER BY id DESC
        """)
        rows = cursor.fetchall()
        return [
            {"id": row["id"], "title": row["title"], "created_at": row["created_at"]}
            for row in rows
        ]


@app.post("/api/conversations", status_code=201)
def create_conversation(conversation: ConversationCreate):
    """新しい会話を作成する"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO conversations (title, system_prompt) VALUES (?, ?)",
            (conversation.title, conversation.system_prompt),
        )
        conn.commit()
        conversation_id = cursor.lastrowid
        return {
            "id": conversation_id,
            "title": conversation.title,
        }


@app.delete("/api/conversations/{conversation_id}")
def delete_conversation(conversation_id: int):
    """会話を削除する(中のメッセージも一緒に削除)"""
    with get_db_connection() as conn:
        cursor = conn.cursor()

        # 存在チェック
        cursor.execute(
            "SELECT * FROM conversations WHERE id = ?", (conversation_id,)
        )
        existing = cursor.fetchone()
        if existing is None:
            raise HTTPException(status_code=404, detail="Conversation not found")

        # この会話に属するメッセージを先に消す
        cursor.execute(
            "DELETE FROM messages WHERE conversation_id = ?", (conversation_id,)
        )
        cursor.execute(
            "DELETE FROM conversations WHERE id = ?", (conversation_id,)
        )
        conn.commit()
        return {"message": "Conversation deleted", "id": conversation_id}


# --- APIエンドポイント: メッセージ ---


@app.get("/api/conversations/{conversation_id}/messages")
def get_messages(conversation_id: int):
    """指定された会話のメッセージ一覧を取得する(古い順)"""
    with get_db_connection() as conn:
        cursor = conn.cursor()

        # 会話の存在チェック
        cursor.execute(
            "SELECT * FROM conversations WHERE id = ?", (conversation_id,)
        )
        if cursor.fetchone() is None:
            raise HTTPException(status_code=404, detail="Conversation not found")

        cursor.execute(
            """
            SELECT id, role, content, created_at
            FROM messages
            WHERE conversation_id = ?
            ORDER BY id
            """,
            (conversation_id,),
        )
        rows = cursor.fetchall()
        return [
            {
                "id": row["id"],
                "role": row["role"],
                "content": row["content"],
                "created_at": row["created_at"],
            }
            for row in rows
        ]


@app.post("/api/conversations/{conversation_id}/messages", status_code=201)
def send_message(conversation_id: int, user_message: MessageCreate):
    """
    ユーザーのメッセージを送り、AIの返答を受け取る

    流れ:
      1. 会話の存在をチェックし、systemプロンプトを取得
      2. ユーザーのメッセージをDBに保存
      3. この会話の過去メッセージ全部 + system を OpenAI API に送る
      4. AIの返答をDBに保存
      5. AIの返答を返す
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()

        # 1. 会話の存在チェック + system_prompt を取り出す
        cursor.execute(
            "SELECT * FROM conversations WHERE id = ?", (conversation_id,)
        )
        conversation = cursor.fetchone()
        if conversation is None:
            raise HTTPException(status_code=404, detail="Conversation not found")

        # 2. ユーザーメッセージをDBに保存
        cursor.execute(
            "INSERT INTO messages (conversation_id, role, content) VALUES (?, ?, ?)",
            (conversation_id, "user", user_message.content),
        )
        conn.commit()

        # 3. この会話の過去メッセージを全部取り出す(今追加したユーザーメッセージも含む)
        cursor.execute(
            """
            SELECT role, content
            FROM messages
            WHERE conversation_id = ?
            ORDER BY id
            """,
            (conversation_id,),
        )
        past_rows = cursor.fetchall()

        # OpenAI API に渡す形式:
        # [{"role": "system", "content": "..."},
        #  {"role": "user", "content": "..."},
        #  {"role": "assistant", "content": "..."}, ...]
        messages_for_api = [
            {"role": "system", "content": conversation["system_prompt"]},
        ]
        for row in past_rows:
            messages_for_api.append(
                {"role": row["role"], "content": row["content"]}
            )

        # 4. OpenAI API を呼び出す
        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=messages_for_api,
                reasoning_effort=REASONING_EFFORT,
            )
        except Exception as e:
            # API呼び出し失敗
            raise HTTPException(
                status_code=500,
                detail=f"AI APIの呼び出しに失敗しました: {e}",
            )

        # AIの返答テキストを取り出す
        assistant_content = response.choices[0].message.content

        # 5. AIの返答をDBに保存
        cursor.execute(
            "INSERT INTO messages (conversation_id, role, content) VALUES (?, ?, ?)",
            (conversation_id, "assistant", assistant_content),
        )
        conn.commit()
        assistant_message_id = cursor.lastrowid

        # 6. クライアントに返す
        return {
            "id": assistant_message_id,
            "role": "assistant",
            "content": assistant_content,
        }


# --- 静的ファイル配信 ---
# フロントエンド(static/index.html, style.css, app.js)を / で配信する
app.mount("/", StaticFiles(directory="static", html=True), name="static")


# --- アプリ起動時にDBを初期化 ---
init_db()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
