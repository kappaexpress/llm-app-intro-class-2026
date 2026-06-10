"""
チャットアプリ バックエンド - 第5回版 (バックエンドのみ)
LLMアプリケーション基礎

このバックエンドは次の2つを担当します:
  1. OpenAI APIを呼んでAIの返答を取得する
  2. 静的ファイル(フロントエンド)を配信する

第5回時点での制約:
  - 会話履歴は保持しない (毎回新規・単発の質問応答)
  - DBもまだ無い
  - フロントエンドは次回(第6回)で作る (今は static/index.html はプレースホルダ)
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from openai import OpenAI
from pydantic import BaseModel

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
REASONING_EFFORT = "low"

# システムプロンプト(AIの振る舞いを指示する文)
# 第5回時点では固定の定数として持つ
# 第8回で「会話ごとに変える」発想に発展する
SYSTEM_PROMPT = "あなたは親切で丁寧なアシスタントです。日本語で回答してください。"


# --- FastAPIアプリ ---
app = FastAPI(title="Chat App (Session 5)")

# CORS設定(開発しやすいように全許可)
# 本番では allow_origins を絞るべきだが、学習用なので全許可
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Pydanticモデル(リクエスト/レスポンスの型) ---


class ChatRequest(BaseModel):
    """/api/chat のリクエストボディ"""

    # ユーザーからの質問・発言
    message: str


class ChatResponse(BaseModel):
    """/api/chat のレスポンスボディ"""

    # AIからの返答
    reply: str


# --- APIエンドポイント ---


@app.post("/api/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    """
    ユーザーの message を1往復で AI に投げ、返答を返す

    流れ:
      1. system プロンプト + user メッセージを組み立てる
      2. OpenAI API を呼ぶ (失敗したら 500)
      3. 返答テキストを取り出して ChatResponse として返す

    注意:
      - 会話履歴は持たない。前のメッセージを覚えていないのが正しい挙動
      - マルチターン化は第6回で行う
    """
    # OpenAI API に渡す messages 配列を組み立てる
    messages_for_api = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": request.message},
    ]

    # OpenAI API を呼び出す
    # 失敗 (ネットワーク・認証エラー・レート制限など) は 500 にラップして返す
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages_for_api,
            reasoning_effort=REASONING_EFFORT,
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"AI APIの呼び出しに失敗しました: {e}",
        )

    # AIの返答テキストを取り出す
    reply_text = response.choices[0].message.content

    # ChatResponse 型で返す (FastAPI が JSON にシリアライズしてくれる)
    return ChatResponse(reply=reply_text)


# --- 静的ファイル配信 ---
# フロントエンド(static/index.html, style.css)を / で配信する
# 第5回時点では中身はプレースホルダ。第6回でチャット画面を実装する
# 注意: "/" へのマウントはあらゆるURLにマッチするため、
# 必ずAPIエンドポイントの定義より「後」に書くこと(先に書くとAPIが呼べなくなる)
app.mount("/", StaticFiles(directory="static", html=True), name="static")


if __name__ == "__main__":
    import uvicorn

    # 0.0.0.0 で待ち受けることで、Codespaces などからもアクセスできる
    uvicorn.run(app, host="0.0.0.0", port=8000)
