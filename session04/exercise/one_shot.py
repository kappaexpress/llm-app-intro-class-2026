"""
最小スクリプト: OpenAI API と 1往復だけ会話する

第4回の最初に動かすやつです。
これが動けば「自分のPythonコードからLLMが呼べた」ということ。

実行前にAPIキーをシェルで export しておくこと:
    export OPENAI_API_KEY=sk-...
    python one_shot.py
"""

from openai import OpenAI

# OpenAI クライアントを作る。
# 引数を渡さない場合、環境変数 OPENAI_API_KEY を自動で読みに行ってくれる。
# (キーをコードに直接書かないこと!)
client = OpenAI()

# 使うモデル名。今日のメインは gpt-5.4-nano (安価・Reasoning対応)
MODEL_NAME = "gpt-5.4-nano"

# API を呼び出す
# messages は会話履歴を表す配列。今回は user の発言1個だけ。
response = client.chat.completions.create(
    model=MODEL_NAME,
    messages=[
        {
            "role": "user",
            "content": "こんにちは。あなたは誰ですか?短く自己紹介してください。",
        },
    ],
)

# response.choices[0].message.content に AI の返答テキストが入っている
print("=== AIの返答 ===")
print(response.choices[0].message.content)
print()

# usage にはトークン消費量が入っている。コスト感を掴むために最初から見る習慣を。
print("=== トークン消費 ===")
print(f"入力: {response.usage.prompt_tokens} トークン")
print(f"出力: {response.usage.completion_tokens} トークン")
print(f"合計: {response.usage.total_tokens} トークン")
