"""
チャットアプリ バックエンド - 第6回版
LLMアプリケーション基礎

このバックエンドは次の2つだけを担当します:
  1. OpenAI APIを呼んでAIの返答を取得する
  2. フロントエンド(static/)を配信する

第6回時点ではまだ「DB保存」も「複数会話の管理」もしません。
会話の履歴(messages 配列)はフロント側が持っていて、毎回まるごと送ってくる
ことを前提にしています。つまりブラウザをリロードすると会話は消えます。
履歴の永続化は第7回で扱います。
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from openai import OpenAI
from pydantic import BaseModel, Field

# --- OpenAIクライアントの初期化 ---
# 環境変数 OPENAI_API_KEY を自動で読み取ってクライアントを作る
# 起動前にシェルで以下を実行してキーをセットしておくこと:
#   export OPENAI_API_KEY=sk-...
client = OpenAI()

# 使うモデル名(GPT-5.4 クラスで最も安価。Reasoning 対応)
MODEL_NAME = "gpt-5.4-nano"

# Reasoning の強さ。"none" / "low" / "medium" / "high" / "xhigh"
# チャット用途では "none"〜"low" でコストとレイテンシを抑えるのが基本
# "none" は推論を完全にスキップする最速モード
REASONING_EFFORT = "low"

# システムプロンプト(AIの振る舞いを指示する文)
# サーバ側で「先頭に必ず差し込む」のがポイント。
# フロントからは送られてこないので、ここで一元管理する。
SYSTEM_PROMPT = "あなたは親切で丁寧なアシスタントです。日本語で回答してください。"

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


# --- Pydanticモデル(リクエスト/レスポンスの型) ---


class Message(BaseModel):
    """1つの発言を表す。role は "user" か "assistant"。"""

    role: str = Field(pattern="^(user|assistant)$")
    content: str = Field(min_length=1, max_length=4000)


class ChatRequest(BaseModel):
    """フロントから送られてくる会話履歴。

    例:
      {
        "messages": [
          {"role": "user",      "content": "こんにちは"},
          {"role": "assistant", "content": "こんにちは!"},
          {"role": "user",      "content": "今の話を覚えてる?"}
        ]
      }

    最後の要素が必ず "user" のメッセージである想定。
    """

    messages: list[Message] = Field(min_length=1)


class ChatResponse(BaseModel):
    """AIの返答(assistant の content だけ返す)"""

    reply: str


# --- APIエンドポイント ---


@app.post("/api/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    """
    フロントから受け取った会話履歴を、システムプロンプトと一緒に
    OpenAI API に丸ごと渡して返答をもらう。

    流れ:
      1. system プロンプトを先頭に差し込む
      2. その後ろにフロントから受け取った messages を全部つなげる
      3. OpenAI API を呼ぶ
      4. assistant の返答テキストだけ取り出して返す
    """
    # 1 & 2. OpenAI API に渡す配列を組み立てる
    #   [{"role": "system",    "content": "あなたは..."},
    #    {"role": "user",      "content": "..."},
    #    {"role": "assistant", "content": "..."},
    #    {"role": "user",      "content": "..."}]
    messages_for_api = [{"role": "system", "content": SYSTEM_PROMPT}]
    for m in req.messages:
        messages_for_api.append({"role": m.role, "content": m.content})

    # 3. OpenAI API を呼び出す
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

    # 4. assistant の返答テキストを取り出して返す
    assistant_content = response.choices[0].message.content
    return ChatResponse(reply=assistant_content)


# --- 静的ファイル配信 ---
# フロントエンド(static/index.html, style.css, app.js)を / で配信する
# 注意: "/" へのマウントはあらゆるURLにマッチするため、
# 必ずAPIエンドポイントの定義より「後」に書くこと(先に書くとAPIが呼べなくなる)
app.mount("/", StaticFiles(directory="static", html=True), name="static")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
