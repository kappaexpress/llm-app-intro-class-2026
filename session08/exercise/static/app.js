/**
 * Chat App JavaScript - 完成版
 * LLMアプリケーション基礎
 *
 * このファイルは次のことをします:
 *  - 会話一覧の取得/作成/削除/切り替え
 *  - 選択中の会話のメッセージ表示と送信
 *  - AIの返答待ち中の「考え中...」表示
 */

// ============================================================
// 状態(state)
// ============================================================

// 今選択中の会話ID (まだ選んでなければ null)
let currentConversationId = null;

// API送信中フラグ (重複送信を防ぐ)
let isSending = false;

// ============================================================
// 会話一覧の取得・描画
// ============================================================

/**
 * 会話の一覧をサーバから取得して、サイドバーに表示する
 */
async function loadConversations() {
  try {
    const response = await fetch("/api/conversations");
    if (!response.ok) {
      showError("会話一覧の取得に失敗しました");
      return;
    }
    const conversations = await response.json();
    renderConversations(conversations);
  } catch (error) {
    showError("通信エラーが発生しました");
  }
}

/**
 * サイドバーに会話の一覧を表示する
 * XSS対策のため createElement + textContent を使う
 */
function renderConversations(conversations) {
  const list = document.getElementById("conversation-list");
  list.innerHTML = "";

  conversations.forEach((conv) => {
    const li = document.createElement("li");
    li.className = "conversation-item";
    // 今選択中の会話は強調表示する
    if (conv.id === currentConversationId) {
      li.classList.add("active");
    }

    // タイトル部分(クリックで会話を開く)
    const title = document.createElement("span");
    title.className = "conversation-title";
    title.textContent = conv.title;
    title.addEventListener("click", () => selectConversation(conv.id));

    // 削除ボタン
    const deleteBtn = document.createElement("button");
    deleteBtn.className = "conversation-delete";
    deleteBtn.textContent = "✕";
    deleteBtn.addEventListener("click", (e) => {
      // クリックが親(タイトル)に伝わって会話が開かないようにする
      e.stopPropagation();
      deleteConversation(conv.id);
    });

    li.appendChild(title);
    li.appendChild(deleteBtn);
    list.appendChild(li);
  });
}

// ============================================================
// 会話の作成・選択・削除
// ============================================================

/**
 * 新しい会話を作成する
 */
async function createConversation() {
  try {
    const response = await fetch("/api/conversations", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      // 空オブジェクトでOK(サーバ側でデフォルトのタイトルとシステムプロンプトが入る)
      body: JSON.stringify({}),
    });

    if (!response.ok) {
      showError("会話の作成に失敗しました");
      return;
    }

    const newConv = await response.json();
    // 作った会話を今の会話に切り替える
    currentConversationId = newConv.id;
    await loadConversations();
    await loadMessages(newConv.id);
  } catch (error) {
    showError("通信エラーが発生しました");
  }
}

/**
 * 会話を選択(切り替え)する
 */
async function selectConversation(conversationId) {
  currentConversationId = conversationId;
  // サイドバーの選択状態の見た目を更新するため再描画
  await loadConversations();
  // 選択した会話のメッセージを読み込む
  await loadMessages(conversationId);
}

/**
 * 会話を削除する
 */
async function deleteConversation(conversationId) {
  if (!confirm("この会話を削除しますか?")) {
    return;
  }

  try {
    const response = await fetch(`/api/conversations/${conversationId}`, {
      method: "DELETE",
    });

    if (!response.ok) {
      showError("会話の削除に失敗しました");
      return;
    }

    // 削除したのが今選択中の会話なら、選択を解除する
    if (currentConversationId === conversationId) {
      currentConversationId = null;
      clearMessages();
    }
    await loadConversations();
  } catch (error) {
    showError("通信エラーが発生しました");
  }
}

// ============================================================
// メッセージの取得・描画・送信
// ============================================================

/**
 * 指定された会話のメッセージ一覧を読み込んで表示する
 */
async function loadMessages(conversationId) {
  try {
    const response = await fetch(
      `/api/conversations/${conversationId}/messages`,
    );
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

  // メッセージが1件もない場合のガイド表示
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
  bubble.textContent = content;

  div.appendChild(bubble);
  list.appendChild(div);

  scrollToBottom();
  return div;
}

/**
 * メッセージ表示エリアを空にする(初期状態のガイドに戻す)
 */
function clearMessages() {
  const list = document.getElementById("message-list");
  list.innerHTML = "";
  const empty = document.createElement("div");
  empty.className = "empty-state";
  empty.textContent =
    "左のメニューから会話を選ぶか、「+ 新しい会話」を押してください。";
  list.appendChild(empty);
}

/**
 * メッセージ表示エリアを一番下までスクロールする
 */
function scrollToBottom() {
  const list = document.getElementById("message-list");
  list.scrollTop = list.scrollHeight;
}

/**
 * メッセージを送信する
 *  1. ユーザーメッセージを画面に追加
 *  2. 「考え中...」を表示
 *  3. サーバに送って AI の返答を待つ
 *  4. 「考え中...」を AI の返答で置き換える
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

  // 会話が選ばれてなければ自動で新しく作る
  if (currentConversationId === null) {
    await createConversation();
    if (currentConversationId === null) {
      // 作成に失敗していたら中断
      return;
    }
  }

  isSending = true;
  setSendButtonEnabled(false);

  // 1. ユーザーメッセージを画面に追加
  appendMessage("user", content);
  input.value = "";

  // 2. 「考え中...」をプレースホルダで表示
  const loadingElement = appendMessage("assistant", "考え中...", "loading");

  try {
    // 3. サーバに送って AI の返答を待つ
    const response = await fetch(
      `/api/conversations/${currentConversationId}/messages`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ content: content }),
      },
    );

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

// 「+ 新しい会話」ボタン
document.getElementById("new-chat-button").addEventListener("click", () => {
  createConversation();
});

// フォーム送信(送信ボタンを押したとき)
document.getElementById("chat-form").addEventListener("submit", (e) => {
  e.preventDefault();
  sendMessage();
});

// テキストエリアで Enterキーで送信、Shift+Enterで改行
document.getElementById("chat-input").addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
});

// ============================================================
// 初期化
// ============================================================

// ページが読み込まれたら、まず会話一覧を取得する
loadConversations();
