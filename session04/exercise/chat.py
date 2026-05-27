"""
CLIチャットスクリプト: ターミナルから AI と対話する

第4回の演習の本体。
ユーザーの入力 → API呼び出し → 返答表示 をループする。
`messages` 配列に履歴を積んでいくので、AI は前の発言を覚えている。

実行前にAPIキーをシェルで export しておくこと:
    export OPENAI_API_KEY=sk-...
    python chat.py

終了方法:
    `exit` と入力する / Ctrl+C を押す
"""

from openai import OpenAI

# OpenAI クライアントを作る。環境変数 OPENAI_API_KEY を自動で読み取る。
client = OpenAI()

# 使うモデル名
MODEL_NAME = "gpt-5.4-nano"

# system プロンプト: AI の役割・性格を最初に指示する。
# このスクリプトでは雑談向けに軽めに設定。
SYSTEM_PROMPT = (
    "あなたは親切で丁寧な日本語アシスタントです。"
    "回答はできるだけ簡潔に、要点を絞って答えてください。"
)


def main() -> None:
    # 会話履歴を保持する配列。
    # API を呼ぶたびに、この配列を丸ごと送信する。
    # 最初に system プロンプトを入れておく(1回だけでよい)。
    messages: list[dict] = [
        {"role": "system", "content": SYSTEM_PROMPT},
    ]

    print(
        "AIチャットを開始します。終了するには 'exit' と入力するか Ctrl+C を押してください。"
    )
    print("-" * 60)

    while True:
        # ユーザーの入力を受け取る
        # Ctrl+C や Ctrl+D で抜けたときも綺麗に終了させる
        try:
            user_input = input("あなた: ")
        except (KeyboardInterrupt, EOFError):
            print()  # 改行
            print("チャットを終了します。")
            break

        # 'exit' で終了
        if user_input.strip().lower() == "exit":
            print("チャットを終了します。")
            break

        # 空行はスキップ(API に空文字を送らない)
        if not user_input.strip():
            continue

        # 履歴にユーザーの発言を追加
        messages.append({"role": "user", "content": user_input})

        # API を呼ぶ。失敗してもループは続けるように try/except で包む。
        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=messages,
            )
        except Exception as e:
            # API エラーが起きたら表示してループに戻る。
            # 直前に積んだ user メッセージは履歴から取り除いておく
            # (送れていない発言を「送ったこと」にしないため)
            print(f"[エラー] API呼び出しに失敗しました: {e}")
            messages.pop()
            continue

        # AI の返答テキストを取り出す
        reply = response.choices[0].message.content

        # 表示する
        print(f"AI: {reply}")
        print()

        # 履歴に AI の返答も追加する。
        # こうすると次のターンで「AI が直前に何を言ったか」も踏まえた応答になる。
        messages.append({"role": "assistant", "content": reply})


if __name__ == "__main__":
    main()
