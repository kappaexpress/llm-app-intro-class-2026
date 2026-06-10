"""
Reasoning デモ: 同じ難問を `reasoning_effort` を変えて投げ、差を比較する

`gpt-5.4-nano` は推論対応モデルなので、`reasoning_effort` で
「どれくらい考えてから答えるか」を切り替えられる。

このスクリプトでは同じ質問を以下の2パターンで投げて、
レイテンシ・トークン数・回答の質を比べる:
  1) reasoning_effort="none"   ← 考えない。速い・安い
  2) reasoning_effort="high"   ← しっかり考える。遅い・高い

実行前にAPIキーをシェルで export しておくこと:
    export OPENAI_API_KEY=sk-...
    python reasoning_demo.py
"""

import time

from openai import OpenAI

client = OpenAI()

MODEL_NAME = "gpt-5.4-nano"

# 少し頭を使う論理パズル。none だと外しがち、high だと正答に近づく問題を選ぶ。
QUESTION = (
    "次の論理パズルに答えてください。\n"
    "太郎は花子の弟である。\n"
    "次郎は太郎の父である。\n"
    "三郎は次郎の兄である。\n"
    "花子から見て三郎はどんな関係(続柄)になりますか? 結論を一言で述べてから理由を書いてください。"
)


def run_with_effort(effort: str) -> None:
    """指定された reasoning_effort で1回 API を叩き、結果を表示する"""
    print("=" * 60)
    print(f"reasoning_effort = {effort!r}")
    print("=" * 60)

    # レイテンシ測定開始
    start = time.perf_counter()

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "user", "content": QUESTION},
        ],
        reasoning_effort=effort,
    )

    elapsed = time.perf_counter() - start

    # 返答本文
    print("[回答]")
    print(response.choices[0].message.content)
    print()

    # トークン消費の内訳
    # gpt-5.4-nano の usage には reasoning_tokens(モデルが内部で考えた分)も入っている
    usage = response.usage
    print("[トークン使用量]")
    print(f"  入力トークン      : {usage.prompt_tokens}")
    print(f"  出力トークン      : {usage.completion_tokens}")
    # reasoning_tokens は completion_tokens_details の中に入っているケースがある
    reasoning_tokens = None
    details = getattr(usage, "completion_tokens_details", None)
    if details is not None:
        reasoning_tokens = getattr(details, "reasoning_tokens", None)
    if reasoning_tokens is not None:
        print(f"  うち推論トークン  : {reasoning_tokens}")
    print(f"  合計トークン      : {usage.total_tokens}")
    print()

    # レイテンシ
    print(f"[レイテンシ] {elapsed:.2f} 秒")
    print()


def main() -> None:
    print("同じ質問を reasoning_effort='none' と 'high' で投げて比較します。")
    print()
    print("[問題]")
    print(QUESTION)
    print()

    # 1) 推論なし
    run_with_effort("none")

    # 2) しっかり推論
    run_with_effort("high")

    print("=" * 60)
    print("観察ポイント:")
    print("  - 'high' のほうがレイテンシが長くなる")
    print("  - 'high' のほうがトークン消費(特に reasoning_tokens)が増える")
    print("  - 難しい問題ほど 'high' で答えの質が上がる")
    print("  - チャット用途は基本 'none' か 'low' で十分。")
    print("    難しい質問だけ 'high'/'xhigh' に上げる、が定番の使い分け。")


if __name__ == "__main__":
    main()
