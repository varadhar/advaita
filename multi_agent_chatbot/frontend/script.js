let sessionId = null;
const API_BASE = "http://localhost:8000";

const exChat = document.getElementById("existentialist-chat");
const adChat = document.getElementById("advaita-chat");
const modChat = document.getElementById("moderator-chat");
const userInput = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");
const modeSelect = document.getElementById("mode-select");
const sessionIdDisplay = document.getElementById("session-id-display");
const newSessionBtn = document.getElementById("new-session");

async function initSession() {
    try {
        const res = await fetch(`${API_BASE}/session`);
        const data = await res.json();
        sessionId = data.session_id;
        sessionIdDisplay.textContent = sessionId;
        clearChats();
    } catch (err) {
        console.error("Failed to init session:", err);
    }
}

function clearChats() {
    exChat.innerHTML = "";
    adChat.innerHTML = "";
    modChat.innerHTML = "";
}

function appendMessage(container, role, content) {
    const msgDiv = document.createElement("div");
    msgDiv.className = `message ${role === 'user' ? 'user-message' : 'agent-message'}`;
    msgDiv.textContent = content;
    container.appendChild(msgDiv);
    container.scrollTop = container.scrollHeight;
}

async function sendMessage() {
    const message = userInput.value.trim();
    if (!message) return;

    const mode = modeSelect.value;
    userInput.value = "";

    // Append user message to all relevant panes for context
    appendMessage(exChat, "user", message);
    appendMessage(adChat, "user", message);
    if (mode === "debate") {
        appendMessage(modChat, "user", message);
    }

    try {
        const res = await fetch(`${API_BASE}/chat`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                message,
                mode,
                session_id: sessionId
            })
        });

        const data = await res.json();

        if (data.mode === "parallel") {
            appendMessage(exChat, "agent", data.data.existentialist);
            appendMessage(adChat, "agent", data.data.advaita);
        } else if (data.mode === "debate") {
            appendMessage(exChat, "agent", data.data.existentialist);
            appendMessage(adChat, "agent", data.data.advaita_rebuttal);
            appendMessage(exChat, "agent", `Counter: ${data.data.existentialist_counter}`);
            appendMessage(modChat, "agent", data.data.moderator_synthesis);
        }
    } catch (err) {
        console.error("Chat error:", err);
        const errorMsg = "Error: Could not reach the philosophical masters.";
        appendMessage(modChat, "agent", errorMsg);
    }
}

sendBtn.addEventListener("click", sendMessage);
userInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") sendMessage();
});
newSessionBtn.addEventListener("click", initSession);

// Initialize session on load
initSession();
