// ============================================
// Echo App - 復習用ミニアプリ
// LLMアプリケーション基礎 2026 - 第3回
// ============================================
//
// やること:
//   1. フォーム送信を受け取る
//   2. fetch で POST /api/echo を呼ぶ
//   3. レスポンスの echo を画面に表示する
//
// 復習ポイント: addEventListener / async-await / fetch / textContent

const form = document.getElementById("echo-form");
const input = document.getElementById("message-input");
const responseEl = document.getElementById("response");
const errorEl = document.getElementById("error-message");
const sendButton = form.querySelector(".send-button");

// 起動直後の表示
responseEl.classList.add("empty");

// フォーム送信のイベント
form.addEventListener("submit", async (event) => {
  // ブラウザのデフォルト送信(ページ遷移)を止める
  event.preventDefault();

  const message = input.value.trim();
  if (message === "") {
    return;
  }

  // 連打防止 + エラー表示をリセット
  sendButton.disabled = true;
  hideError();
  responseEl.classList.remove("empty");
  responseEl.textContent = "送信中...";

  try {
    // バックエンドの /api/echo に POST する
    const res = await fetch("/api/echo", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message }),
    });

    if (!res.ok) {
      // 422 (バリデーションエラー) などはここに来る
      throw new Error(`サーバーエラー: ${res.status}`);
    }

    const data = await res.json();

    // XSS対策で innerHTML ではなく textContent を使う
    responseEl.textContent = data.echo;

    // 入力欄をクリアして次の入力に備える
    input.value = "";
  } catch (err) {
    showError(err.message ?? "通信に失敗しました");
    responseEl.classList.add("empty");
    responseEl.textContent = "応答を取得できませんでした";
  } finally {
    sendButton.disabled = false;
    input.focus();
  }
});

function showError(message) {
  errorEl.textContent = message;
  errorEl.style.display = "block";
}

function hideError() {
  errorEl.textContent = "";
  errorEl.style.display = "none";
}
