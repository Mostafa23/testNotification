let isSubscribed = false;
let userId = "";
const subscribeBtn = document.getElementById("subscribeBtn");
const log = document.getElementById('log');

// Get user ID from localStorage or generate a new one if not exists
if (!localStorage.getItem("userId")) {
    userId = crypto.randomUUID();
    localStorage.setItem("userId", userId);
} else {
    userId = localStorage.getItem("userId");
}

// Initialize WebSocket connection
let ws = null;

// Connect to WebSocket after authentication
function connectWebSocket() {
    if (ws) {
        try {
            ws.close();
        } catch (e) {
            console.error("Error closing existing WebSocket:", e);
        }
    }
    
    // Create new WebSocket connection
    ws = new WebSocket(`ws://${location.host}/ws/client/${userId}`);
    
    ws.onopen = function() {
        console.log("userId:", userId);
        console.log("WebSocket connection established.");
    };
    
    ws.onmessage = function(event) {
        const msg = JSON.parse(event.data);
    
        if (msg.type === "notification") {
            displayMassage(msg.message);
        }
    };
    
    ws.onerror = function(error) {
        console.log("WebSocket error:", error);
    };
    
    ws.onclose = function(event) {
        console.log("WebSocket closed:", event);
        console.log("Close code:", event.code, "Reason:", event.reason);
    
        showVisualNotification("Connection closed (" + event.code + ")", event.reason);
        
        // Try to reconnect after a delay if authentication overlay is not visible
        if (document.getElementById('auth-overlay').style.display === 'none') {
            setTimeout(connectWebSocket, 3000);
        }
    };
}

// Initialize connection only after authentication (handled in auth.js)
// The hideAuthOverlay function in auth.js will trigger this
document.addEventListener('authComplete', () => {
    connectWebSocket();
});

// Connect if auth is already complete (user is logged in)
if (document.getElementById('auth-overlay').style.display === 'none') {
    connectWebSocket();
}

function subscription() {
    if (!ws || ws.readyState !== WebSocket.OPEN) {
        showVisualNotification("Error", "Not connected to server");
        return;
    }
    
    isSubscribed = !isSubscribed;
    subscribeBtn.innerText = isSubscribed ? "Unsubscribe" : "Subscribe";
    ws.send(isSubscribed ? "subscribe" : "unsubscribe");

    showVisualNotification("Subscription Status", isSubscribed ? "Subscribed" : "Unsubscribed");
}

function showVisualNotification(title, message) {
    const notify = document.createElement('div');
    notify.textContent = `${title}: ${message}`;
    notify.classList.add('notification');
    document.body.appendChild(notify);

    setTimeout(() => notify.remove(), 5000);
}

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