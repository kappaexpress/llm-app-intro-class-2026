"""
echo API - 復習用ミニアプリ
LLMアプリケーション基礎 - 第3回

このバックエンドが担当すること:
  1. POST /api/echo で受け取った文字列をオウム返しする
  2. フロントエンド(static/)を / で配信する

LLM/OpenAI はまだ出てきません。
前コースで扱った FastAPI + Pydantic + StaticFiles の復習回です。
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

# --- FastAPIアプリ ---
app = FastAPI(title="Echo App")

# CORS設定(開発しやすいように全許可)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Pydanticモデル(リクエストボディの型) ---


class EchoRequest(BaseModel):
    """/api/echo で受け取るボディ"""

    # 空文字は弾く / 長すぎる入力も弾く
    message: str = Field(min_length=1, max_length=1000)


# --- APIエンドポイント ---


@app.post("/api/echo")
def echo(req: EchoRequest):
    """
    受け取った message をそのまま echo として返すだけ。

    例:
      リクエスト: {"message": "こんにちは"}
      レスポンス: {"echo": "こんにちは"}
    """
    return {"echo": req.message}


# --- 静的ファイル配信 ---
# フロントエンド(static/index.html, style.css, app.js)を / で配信する
# 注意: "/" へのマウントはあらゆるURLにマッチするため、
# 必ずAPIエンドポイントの定義より「後」に書くこと(先に書くとAPIが呼べなくなる)
app.mount("/", StaticFiles(directory="static", html=True), name="static")


if __name__ == "__main__":
    import uvicorn

    # ホスト 0.0.0.0 で Codespaces のポートフォワードに乗る
    uvicorn.run(app, host="0.0.0.0", port=8000)
