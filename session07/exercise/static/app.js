/**
 * Chat App JavaScript - 第7回 (1会話・SQLite保存版)
 * LLMアプリケーション基礎
 *
 * 第6回からの変更点:
 *   - フロントは会話履歴を持たない (サーバの DB が持つ)
 *   - ページロード時に GET /api/messages で過去全件を取得して描画
 *   - 送信時は POST /api/messages にユーザー発言1件だけを送る
 *
 * このファイルがやること:
 *   1. ページロード時に過去メッセージを取得・描画
 *   2. ユーザーが送信したらサーバに POST して、AI の返答を画面に追加
 *   3. AI の返答待ち中は「考え中...」を表示
 */

// ============================================================
// 状態 (state)
// ============================================================

// API 送信中フラグ (連打防止)
let isSending = false;

// ============================================================
// メッセージの取得・描画
// ============================================================

/**
 * 過去のメッセージをサーバから取得して画面に並べる
 * (ページロード時に1回呼ぶ)
 */
async function loadMessages() {
  try {
    const response = await fetch("/api/messages");
    if (!response.ok) {
      showError("メッセージの取得に失敗しました");
      return;
    }
    const messages = await response.json();
    renderMessages(messages);
  } catch (error) {
    showError("通信エラーが発生しました");
  }
}

/**
 * メッセージ一覧を画面に表示する
 */
function renderMessages(messages) {
  const list = document.getElementById("message-list");
  list.innerHTML = "";

  if (messages.length === 0) {
    const empty = document.createElement("div");
    empty.className = "empty-state";
    empty.textContent = "下の入力欄からメッセージを送ってみよう";
    list.appendChild(empty);
    return;
  }

  messages.forEach((msg) => {
    appendMessage(msg.role, msg.content);
  });

  scrollToBottom();
}

/**
 * メッセージを1つ画面に追加する
 *   role: "user" または "assistant"
 *   extraClass: 追加のCSSクラス (例: "loading")
 *   返り値: 追加したメッセージのDOM要素
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
  // XSS対策で textContent を使う (innerHTML は使わない)
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
// メッセージ送信
// ============================================================

/**
 * メッセージを送信する
 *   1. ユーザーメッセージを画面に追加
 *   2. 「考え中...」を表示
 *   3. POST /api/messages を呼ぶ
 *   4. 「考え中...」を AI の返答で置き換える
 *
 * 重要: 過去の履歴は送らない (= サーバが DB から自分で取り出す)
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

  // 1. ユーザーメッセージを画面に即追加
  appendMessage("user", content);
  input.value = "";

  // 2. 「考え中...」をプレースホルダで表示
  const loadingElement = appendMessage("assistant", "考え中...", "loading");

  try {
    // 3. サーバに送る (本文1件だけ、履歴は送らない)
    const response = await fetch("/api/messages", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ content: content }),
    });

    if (!response.ok) {
      const error = await response.json();
      loadingElement.remove();
      showError(error.detail || "AIの返答取得に失敗しました");
      return;
    }

    const assistantMsg = await response.json();

    // 4. 「考え中...」を AI の返答で置き換える
    loadingElement.querySelector(".message-bubble").textContent =
      assistantMsg.content;
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

// フォーム送信 (送信ボタンを押したとき)
document.getElementById("chat-form").addEventListener("submit", (e) => {
  e.preventDefault();
  sendMessage();
});

// テキストエリアで Enter で送信、Shift+Enter で改行
document.getElementById("chat-input").addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
});

// ============================================================
// 初期化
// ============================================================

// ページが読み込まれたら、まず過去のメッセージを取得する
// (これで「リロードしても消えない」が実現する)
loadMessages();
