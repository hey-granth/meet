class RoomChatApp {
    constructor() {
        this.baseURL = 'http://localhost:8000';
        this.wsURL = 'ws://localhost:8000';
        this.currentUser = null;
        this.currentRoom = null;
        this.socket = null;

        this.init();
    }

    init() {
        this.setupEventListeners();
        this.checkAuthStatus();
    }

    setupEventListeners() {
        // Auth tab switching
        document.getElementById('login-tab').addEventListener('click', () => this.switchTab('login'));
        document.getElementById('register-tab').addEventListener('click', () => this.switchTab('register'));

        // Form submissions
        document.getElementById('login-form').addEventListener('submit', (e) => this.handleLogin(e));
        document.getElementById('register-form').addEventListener('submit', (e) => this.handleRegister(e));
        document.getElementById('create-room-form').addEventListener('submit', (e) => this.handleCreateRoom(e));
        document.getElementById('join-room-form').addEventListener('submit', (e) => this.handleJoinRoom(e));
        document.getElementById('message-form').addEventListener('submit', (e) => this.handleSendMessage(e));

        // Button clicks
        document.getElementById('logout-btn').addEventListener('click', () => this.handleLogout());
        document.getElementById('leave-room-btn').addEventListener('click', () => this.leaveRoom());
        document.getElementById('copy-code-btn').addEventListener('click', () => this.copyRoomCode());
    }

    switchTab(tab) {
        const loginTab = document.getElementById('login-tab');
        const registerTab = document.getElementById('register-tab');
        const loginForm = document.getElementById('login-form');
        const registerForm = document.getElementById('register-form');

        if (tab === 'login') {
            loginTab.classList.add('active');
            registerTab.classList.remove('active');
            loginForm.classList.remove('hidden');
            registerForm.classList.add('hidden');
        } else {
            registerTab.classList.add('active');
            loginTab.classList.remove('active');
            registerForm.classList.remove('hidden');
            loginForm.classList.add('hidden');
        }
    }

    async checkAuthStatus() {
        try {
            const response = await fetch(`${this.baseURL}/auth/`, {
                credentials: 'include'
            });

            if (response.ok) {
                const data = await response.json();
                this.currentUser = data.user;
                this.showScreen('dashboard');
            } else {
                this.showScreen('auth');
            }
        } catch (error) {
            console.error('Auth check failed:', error);
            this.showScreen('auth');
        }
    }

    async handleLogin(e) {
        e.preventDefault();
        this.showLoading(true);

        const username = document.getElementById('login-username').value;
        const password = document.getElementById('login-password').value;

        try {
            const response = await fetch(`${this.baseURL}/login/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
                body: JSON.stringify({ username, password })
            });

            const data = await response.json();

            if (response.ok) {
                this.currentUser = data.user;
                this.showToast('Login successful!', 'success');
                this.showScreen('dashboard');
            } else {
                this.showError('auth-error', data.error || 'Login failed');
            }
        } catch (error) {
            console.error('Login error:', error);
            this.showError('auth-error', 'Network error. Please try again.');
        } finally {
            this.showLoading(false);
        }
    }

    async handleRegister(e) {
        e.preventDefault();
        this.showLoading(true);

        const username = document.getElementById('register-username').value;
        const email = document.getElementById('register-email').value;
        const password = document.getElementById('register-password').value;
        const password2 = document.getElementById('register-password2').value;

        if (password !== password2) {
            this.showError('auth-error', 'Passwords do not match');
            this.showLoading(false);
            return;
        }

        try {
            const response = await fetch(`${this.baseURL}/register/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
                body: JSON.stringify({ username, email, password, password2 })
            });

            const data = await response.json();

            if (response.ok) {
                this.showToast('Registration successful! Please login.', 'success');
                this.switchTab('login');
                document.getElementById('register-form').reset();
            } else {
                this.showError('auth-error', data.error || 'Registration failed');
            }
        } catch (error) {
            console.error('Registration error:', error);
            this.showError('auth-error', 'Network error. Please try again.');
        } finally {
            this.showLoading(false);
        }
    }

    async handleLogout() {
        this.showLoading(true);

        try {
            await fetch(`${this.baseURL}/logout/`, {
                method: 'POST',
                credentials: 'include'
            });

            this.currentUser = null;
            this.currentRoom = null;
            this.disconnectWebSocket();
            this.showToast('Logged out successfully', 'success');
            this.showScreen('auth');
        } catch (error) {
            console.error('Logout error:', error);
            this.showToast('Logout failed', 'error');
        } finally {
            this.showLoading(false);
        }
    }

    async handleCreateRoom(e) {
        e.preventDefault();
        this.showLoading(true);

        const name = document.getElementById('room-name').value;

        try {
            const response = await fetch(`${this.baseURL}/create-room/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
                body: JSON.stringify({ name })
            });

            const data = await response.json();

            if (response.ok) {
                this.currentRoom = data;
                this.showToast('Room created successfully!', 'success');
                this.enterRoom();
            } else {
                this.showError('dashboard-error', data.error || 'Failed to create room');
            }
        } catch (error) {
            console.error('Create room error:', error);
            this.showError('dashboard-error', 'Network error. Please try again.');
        } finally {
            this.showLoading(false);
        }
    }

    async handleJoinRoom(e) {
        e.preventDefault();
        this.showLoading(true);

        const code = document.getElementById('room-code').value;

        try {
            const response = await fetch(`${this.baseURL}/join-room/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
                body: JSON.stringify({ code })
            });

            const data = await response.json();

            if (response.ok) {
                this.currentRoom = data;
                this.showToast('Joined room successfully!', 'success');
                this.enterRoom();
            } else {
                this.showError('dashboard-error', data.error || 'Failed to join room');
            }
        } catch (error) {
            console.error('Join room error:', error);
            this.showError('dashboard-error', 'Network error. Please try again.');
        } finally {
            this.showLoading(false);
        }
    }

    enterRoom() {
        document.getElementById('room-title').textContent = this.currentRoom.name;
        document.getElementById('room-code-display').textContent = `Code: ${this.currentRoom.code}`;

        this.showScreen('room');
        this.connectWebSocket();
        this.clearMessages();
    }

    leaveRoom() {
        this.currentRoom = null;
        this.disconnectWebSocket();
        this.showScreen('dashboard');
        this.clearForms();
    }

    connectWebSocket() {
        if (this.socket) {
            this.socket.close();
        }

        const wsUrl = `${this.wsURL}/ws/room/${this.currentRoom.code}/`;
        this.socket = new WebSocket(wsUrl);

        this.updateConnectionStatus('connecting', 'Connecting...');

        this.socket.onopen = () => {
            console.log('WebSocket connected');
            this.updateConnectionStatus('connected', 'Connected');
        };

        this.socket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            this.handleWebSocketMessage(data);
        };

        this.socket.onclose = () => {
            console.log('WebSocket disconnected');
            this.updateConnectionStatus('disconnected', 'Disconnected');
        };

        this.socket.onerror = (error) => {
            console.error('WebSocket error:', error);
            this.updateConnectionStatus('error', 'Connection Error');
        };
    }

    disconnectWebSocket() {
        if (this.socket) {
            this.socket.close();
            this.socket = null;
        }
    }

    handleWebSocketMessage(data) {
        switch (data.type) {
            case 'message':
                this.addMessage(data.message, data.user, data.user === this.currentUser);
                break;
            case 'user_joined':
                this.showToast(`${data.user} joined the room`, 'success');
                break;
            case 'user_left':
                this.showToast(`${data.user} left the room`, 'error');
                break;
            default:
                console.log('Unknown message type:', data.type);
        }
    }

    handleSendMessage(e) {
        e.preventDefault();

        const messageInput = document.getElementById('message-input');
        const message = messageInput.value.trim();

        if (!message || !this.socket || this.socket.readyState !== WebSocket.OPEN) {
            return;
        }

        this.socket.send(JSON.stringify({
            type: 'message',
            message: message,
            user: this.currentUser
        }));

        messageInput.value = '';
    }

    addMessage(message, user, isOwn) {
        const messagesContainer = document.getElementById('messages');
        const messageElement = document.createElement('div');
        messageElement.className = `message ${isOwn ? 'own' : 'other'}`;

        if (!isOwn) {
            const senderElement = document.createElement('div');
            senderElement.className = 'message-sender';
            senderElement.textContent = user;
            messageElement.appendChild(senderElement);
        }

        const textElement = document.createElement('div');
        textElement.textContent = message;
        messageElement.appendChild(textElement);

        messagesContainer.appendChild(messageElement);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    clearMessages() {
        document.getElementById('messages').innerHTML = '';
    }

    copyRoomCode() {
        if (this.currentRoom) {
            navigator.clipboard.writeText(this.currentRoom.code).then(() => {
                this.showToast('Room code copied to clipboard!', 'success');
            }).catch(() => {
                this.showToast('Failed to copy room code', 'error');
            });
        }
    }

    updateConnectionStatus(status, text) {
        const indicator = document.getElementById('connection-indicator');
        const textElement = document.getElementById('connection-text');

        indicator.className = `status-indicator ${status}`;
        textElement.textContent = text;
    }

    showScreen(screenName) {
        const screens = document.querySelectorAll('.screen');
        screens.forEach(screen => screen.classList.add('hidden'));

        document.getElementById(`${screenName}-screen`).classList.remove('hidden');
    }

    showLoading(show) {
        const loading = document.getElementById('loading');
        if (show) {
            loading.classList.remove('hidden');
        } else {
            loading.classList.add('hidden');
        }
    }

    showError(elementId, message) {
        const errorElement = document.getElementById(elementId);
        errorElement.textContent = message;
        errorElement.classList.remove('hidden');

        setTimeout(() => {
            errorElement.classList.add('hidden');
        }, 5000);
    }

    showToast(message, type = 'info') {
        const toastContainer = document.getElementById('toast-container');
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        toast.textContent = message;

        toastContainer.appendChild(toast);

        setTimeout(() => {
            toast.remove();
        }, 3000);
    }

    clearForms() {
        document.getElementById('create-room-form').reset();
        document.getElementById('join-room-form').reset();
        document.getElementById('message-input').value = '';

        // Clear error messages
        document.querySelectorAll('.error-message').forEach(el => {
            el.classList.add('hidden');
        });
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new RoomChatApp();
});

const patchFrontendForBackend = () => {
    // After login, set window.currentUser manually
    window.handleLogin = async (username, password) => {
        const res = await fetch('/login/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            credentials: 'include',
            body: JSON.stringify({ username, password })
        });

        if (res.ok) {
            window.currentUser = username; // Manually set username
            showRooms();
        } else {
            alert('Login failed');
        }
    };

    // Fix room creation handling
    window.handleCreateRoom = async () => {
        const res = await fetch('/create-room/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            credentials: 'include',
        });

        if (res.ok) {
            const data = await res.json();
            const roomCode = data.room_code || data.code || 'UNKNOWN';
            showChat({ code: roomCode, name: `Room ${roomCode}` });
        }
    };

    // Fix join room handling
    window.handleJoinRoom = async (code) => {
        const res = await fetch('/join-room/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            credentials: 'include',
            body: JSON.stringify({ code })
        });

        if (res.ok) {
            showChat({ code, name: `Room ${code}` });
        } else {
            alert('Invalid room code');
        }
    };
};

// Helper to get CSRF cookie
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

patchFrontendForBackend();