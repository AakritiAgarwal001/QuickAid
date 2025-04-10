async function sendMessage() {
  const input = document.getElementById("user-input");
  const message = input.value.trim();
  if (!message) return;

  appendMessage("user", message);
  input.value = "";

  try {
    const res = await fetch("http://127.0.0.1:5000/api/message", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message })
    });
    const data = await res.json();
    appendMessage("ai", data.response || "Sorry, I couldn't understand that.");
  } catch {
    appendMessage("ai", "Error contacting AI backend.");
  }
}

function appendMessage(sender, text) {
  const chatBox = document.getElementById("chat-box");
  const messageElem = document.createElement("div");
  messageElem.className = `message ${sender}`;
  messageElem.innerText = text;
  chatBox.appendChild(messageElem);
  chatBox.scrollTop = chatBox.scrollHeight;
}
