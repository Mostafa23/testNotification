const log = document.getElementById('messages');
const countSubscribers = document.getElementById("count-subscribers");
const countClients = document.getElementById("count-clients");
const ws = new WebSocket(`ws://${location.host}/ws/server`);

// Flag to check if counts have been requested after reconnect
let countsRequested = false;

ws.onopen = () => {
    console.log("WebSocket connection established");

    if (!countsRequested) {
        sendCount();
    }
};

ws.onmessage = (event) => {
    const msg = JSON.parse(event.data);
    if (msg.type === "counts") {
        countSubscribers.textContent = msg.subscribers;
        countClients.textContent = msg.clients;
    }

    if (msg.type === "notifications") {
        msg.notifications.forEach(notification => {
            displayMassage(notification.message);
        });
    }
};    

ws.onerror = (error) => {
    console.error("WebSocket error:", error);
};

ws.onclose = () => {
    console.warn("WebSocket connection closed");
};

function send() {
    if (countSubscribers.textContent === "0") {
        return alert("No subscribers to notify!");
    }

    const msgInput = document.getElementById("msg");
    const msg = msgInput.value;
    if (!msg) return alert("Message is empty!");

    if (ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({ action: "notify", message: msg }));

        displayMassage(msg);
        msgInput.value = "";
    } else {
        alert("WebSocket is not open yet!");
    }
}

// Re-send count request after reload once WebSocket is open
window.addEventListener("load", () => {
    if (ws.readyState === WebSocket.OPEN) {
        sendCount();
    } else {
        ws.addEventListener("open", () => {
            if (!countsRequested) {
                sendCount();
            }
        });
    }
});

// function to send count
function sendCount() {
    ws.send(JSON.stringify({ action: "count" }));
    ws.send(JSON.stringify({ action: "get_notifications" }));
    countsRequested = true;
}

// function to display notification messages
function displayMassage(msg) {
    const messageCard = document.createElement('div');
    messageCard.className = 'message-card fade-in';

    const messageText = document.createElement('div');
    messageText.className = 'message-text';
    messageText.textContent = msg;

    messageCard.appendChild(messageText);
    log.appendChild(messageCard);
    log.scrollTop = log.scrollHeight;
}