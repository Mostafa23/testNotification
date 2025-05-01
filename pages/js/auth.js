// DOM Elements
const authOverlay = document.getElementById('auth-overlay');
const emailInput = document.getElementById('email-input');
const registerBtn = document.getElementById('register-btn');
const loginBtn = document.getElementById('login-btn');
const loginSection = document.getElementById('login-section');
const authMessage = document.getElementById('auth-message');
const authLoader = document.getElementById('auth-loader');
const subscribeBtn = document.getElementById('subscribeBtn');

// Session token handling
const TOKEN_KEY = 'auth_token';
let userEmail = '';

// Check if user is already authenticated
window.addEventListener('DOMContentLoaded', async () => {
    const token = localStorage.getItem(TOKEN_KEY);
    if (token) {
        // Verify token with server
        showLoader(true);
        try {
            const response = await fetch(`/check-auth?token=${token}`);
            const data = await response.json();
            
            if (data.authenticated) {
                userEmail = data.email;
                hideAuthOverlay();
                enableSubscribeButton();
                showVisualNotification('Authentication', `Welcome back, ${userEmail}`);
            } else {
                localStorage.removeItem(TOKEN_KEY);
                showLoginOption();
            }
        } catch (error) {
            console.error('Auth check error:', error);
            showLoginOption();
        }
        showLoader(false);
    } else {
        showLoginOption();
    }
});

// Event Listeners
registerBtn.addEventListener('click', handleRegister);
loginBtn.addEventListener('click', handleLogin);

// Show login option if user has potentially registered before
function showLoginOption() {
    loginSection.style.display = 'block';
}

// Handle registration
async function handleRegister() {
    const email = emailInput.value.trim();
    if (!isValidEmail(email)) {
        showMessage('Please enter a valid email address', 'error');
        return;
    }
    
    showLoader(true);
    try {
        const response = await fetch('/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showMessage(data.message, 'success');
            showLoginOption();
        } else {
            showMessage(data.message || 'Registration failed', 'error');
        }
    } catch (error) {
        console.error('Registration error:', error);
        showMessage('Server error. Please try again later.', 'error');
    }
    showLoader(false);
}

// Handle login
async function handleLogin() {
    const email = emailInput.value.trim();
    if (!isValidEmail(email)) {
        showMessage('Please enter a valid email address', 'error');
        return;
    }
    
    showLoader(true);
    try {
        const response = await fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            localStorage.setItem(TOKEN_KEY, data.token);
            userEmail = email;
            hideAuthOverlay();
            enableSubscribeButton();
            showVisualNotification('Authentication', 'Login successful');
        } else {
            showMessage(data.message || 'Login failed', 'error');
        }
    } catch (error) {
        console.error('Login error:', error);
        showMessage('Server error. Please try again later.', 'error');
    }
    showLoader(false);
}

// Hide auth overlay after successful authentication
function hideAuthOverlay() {
    authOverlay.style.display = 'none';
}

// Enable subscribe button after authentication
function enableSubscribeButton() {
    subscribeBtn.disabled = false;
}

// Show success/error messages
function showMessage(message, type) {
    authMessage.textContent = message;
    authMessage.className = type === 'success' ? 'success-message' : 'error-message';
    
    // Clear message after 5 seconds
    setTimeout(() => {
        authMessage.textContent = '';
        authMessage.className = '';
    }, 5000);
}

// Show/hide loader
function showLoader(show) {
    authLoader.style.display = show ? 'block' : 'none';
}

// Email validation
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}