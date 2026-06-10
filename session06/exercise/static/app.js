/**
 * Chat App JavaScript - 第6回版
 * LLMアプリケーション基礎
 *
 * このバージョンの設計:
 *  - フロント側の変数 messages に会話履歴を全部持つ
 *  - 送信のたびに「messages 全体」をサーバに送る
 *  - サーバはDB保存しない(=リロードで消える)
 *  - このため、毎回の送信で送るデータ量はだんだん増えていく
 *    DevTools の Network タブで実際に観察してみよう
 */

// ============================================================
// 状態(state)
// ============================================================

/**
 * 会話の履歴。要素は { role: "user" | "assistant", content: string }
 * 重要: system プロンプトは含めない(サーバ側で先頭に差し込む)
 *
 * ページをリロードすると、このオブジェクトは初期化される。
 * 第7回ではこれをサーバ側のDBに保存して永続化する。
 */
let messages = [];

// API送信中フラグ(重複送信を防ぐ)
let isSending = false;

// ============================================================
// メッセージの描画
// ============================================================

/**
 * メッセージを1つ画面に追加する
 * role: "user" または "assistant"
 * extraClass: 追加のCSSクラス(例: "loading")
 * 返り値: 追加したメッセージのDOM要素
 */
function appendMessage(role, content, extraClass = "") {
  const list = document.getElementById("message-list");

  // 空状態の表示が残っていたら消す
  const emptyState = list.querySelector(".empty-state");
  if (emptyState) {
    emptyState.remove();
  }

  const div = document.createElement("div");
  div.className = "message " + role + (extraClass ? " " + extraClass : "");

  const bubble = document.createElement("div");
  bubble.className = "message-bubble";
  // textContent を使うことで XSS を防ぐ
  // (innerHTML だとユーザー入力に含まれるHTMLが実行されてしまう危険がある)
  bubble.textContent = content;

  div.appendChild(bubble);
  list.appendChild(div);

  scrollToBottom();
  return div;
}

/**
 * メッセージ表示エリアを一番下までスクロールする
 */
function scrollToBottom() {
  const list = document.getElementById("message-list");
  list.scrollTop = list.scrollHeight;
}

// ============================================================
// メッセージの送信
// ============================================================

/**
 * メッセージを送信する
 *  1. 入力内容を取り出す
 *  2. messages 配列にユーザーメッセージを push
 *  3. 画面にユーザーメッセージを追加
 *  4. 「考え中...」のプレースホルダを表示
 *  5. fetch で /api/chat に messages 全体を送る
 *  6. 返答を messages 配列に push
 *  7. 「考え中...」を返答テキストで置き換える
 */
async function sendMessage() {
  // 連打防止
  if (isSending) return;

  const input = document.getElementById("chat-input");
  const content = input.value.trim();

  if (content === "") {
    showError("メッセージを入力してください");
    return;
  }

  isSending = true;
  setSendButtonEnabled(false);

  // 1 & 2. ユーザーメッセージを履歴に追加
  messages.push({ role: "user", content: content });

  // 3. 画面にユーザーメッセージを追加
  appendMessage("user", content);
  input.value = "";

  // 4. 「考え中...」をプレースホルダで表示
  const loadingElement = appendMessage("assistant", "考え中...", "loading");

  try {
    // 5. サーバに messages 全体を送る
    //    会話が長くなるほど、ここで送るデータも長くなっていく。
    //    DevTools → Network → /api/chat → Payload で確認できる。
    const response = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ messages: messages }),
    });

    if (!response.ok) {
      // エラー時は最後に追加した user メッセージを履歴から戻す
      // (画面側は残しておく方が状況が見えて親切)
      const error = await response.json().catch(() => ({}));
      loadingElement.remove();
      showError(error.detail || "AIの返答取得に失敗しました");
      return;
    }

    const data = await response.json();
    const reply = data.reply;

    // 6. 返答を履歴に追加
    messages.push({ role: "assistant", content: reply });

    // 7. 「考え中...」を返答テキストで置き換える
    loadingElement.querySelector(".message-bubble").textContent = reply;
    loadingElement.classList.remove("loading");
    scrollToBottom();
  } catch (error) {
    loadingElement.remove();
    showError("通信エラーが発生しました");
  } finally {
    isSending = false;
    setSendButtonEnabled(true);
  }
}

/**
 * 送信ボタンの有効/無効を切り替える
 */
function setSendButtonEnabled(enabled) {
  const button = document.querySelector(".send-button");
  button.disabled = !enabled;
}

// ============================================================
// エラー表示
// ============================================================

function showError(message) {
  const errorDiv = document.getElementById("error-message");
  errorDiv.textContent = message;
  errorDiv.style.display = "block";
  // 5秒後に自動で消す
  setTimeout(() => {
    errorDiv.style.display = "none";
  }, 5000);
}

// ============================================================
// イベントリスナー
// ============================================================

// フォーム送信(送信ボタンを押したとき)
document.getElementById("chat-form").addEventListener("submit", (e) => {
  e.preventDefault();
  sendMessage();
});

// テキストエリアで Enterキーで送信、Shift+Enterで改行
document.getElementById("chat-input").addEventListener("keydown", (e) => {
  // e.isComposing は日本語入力(IME)で変換中なら true。
  // 変換を確定するためのEnterで送信されてしまわないようにチェックする
  if (e.key === "Enter" && !e.shiftKey && !e.isComposing) {
    e.preventDefault();
    sendMessage();
  }
});

// ============================================================
// デバッグ用: コンソールから messages を覗けるようにする
// 講義で「DevToolsで messages の中身を見る」演習をするために公開しておく
// ============================================================
window.__debug = {
  // 現在の履歴を見る関数: ブラウザのConsoleで __debug.show() と叩く
  show: () => {
    console.log("現在の messages 配列:", messages);
    console.log("発言数:", messages.length);
    return messages;
  },
};
