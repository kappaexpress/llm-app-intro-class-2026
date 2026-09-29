# 参考資料と確認日

確認日：2026-09-29。料金・対応機能・利用条件は開講前に確認してください。

## 授業構成の参照元

- [Webアプリケーション基礎2026](https://github.com/kappaexpress/web-app-intro-class-2026)
- [Python/FastAPIの回](https://github.com/kappaexpress/web-app-intro-class-2026/blob/main/session05/slides.md)
- [結合の演習](https://github.com/kappaexpress/web-app-intro-class-2026/tree/main/session07/exercise)
- [制作の回](https://github.com/kappaexpress/web-app-intro-class-2026/blob/main/session09/slides.md)

Marp形式、技術構成、完成品を改造する学習の流れを参考にしました。
本教材のコードと学習ノートは新規作成です。資料中の課題・案内は架空データです。

## APIとモデル

- [GPT-6 Luna](https://developers.openai.com/api/docs/models/gpt-6-luna)：モデルID、推論設定、機能
- [Text generation](https://developers.openai.com/api/docs/guides/text)：Responses API
- [Function calling](https://developers.openai.com/api/docs/guides/function-calling)：関数定義と結果の受け渡し
- [Embeddings](https://developers.openai.com/api/docs/guides/embeddings)：ベクトルの生成
- [OpenAIモデル](https://developers.openai.com/api/docs/models)
- [Claude](https://www.anthropic.com/claude)
- [Geminiモデル](https://ai.google.dev/gemini-api/docs/models)
- [Llamaの公式モデルリポジトリ](https://github.com/meta-llama/llama-models)

生成モデルはユーザー指定のgpt-6-lunaに統一し、reasoning.effort=noneを明示しています。
Embeddingは別の用途なのでtext-embedding-3-smallを使います。
価格をスライドへ固定せず、料金の算出方法を扱います。

## 背景

- [Attention Is All You Need (2017)](https://arxiv.org/abs/1706.03762)
- [Language Models are Few-Shot Learners (2020)](https://arxiv.org/abs/2005.14165)
- [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks (2020)](https://arxiv.org/abs/2005.11401)
- [ChatGPTの公開 (2022)](https://openai.com/index/chatgpt/)

スライドの該当箇所にも出典をコメントで付けています。
