const apiUrl = window.location.origin;

// Section to Register on the website and become a user
document.getElementById('registerForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    fetch(`${apiUrl}/register`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username: username, email: email, password: password })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        if (data.message === 'User registered successfully') {
            window.location.href = 'login.html';
        }
    })
    .catch(error => console.error('Error:', error));
});

// Section to Login to website
document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    fetch(`${apiUrl}/login`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, password })
    })
    .then(response => response.json())
    .then(data => {
        if (data.token) {
            localStorage.setItem('token', data.token);
            window.location.href = 'chatInterface.html';
        } else {
            alert(data.message);
        }
    })
    .catch(error => console.error('Error:', error));
});

// Section of webpage to submit Chats
document.getElementById('messageForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const message = document.getElementById('message').value;
    const token = localStorage.getItem('token');

    fetch(`${apiUrl}/send_message`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ content: message })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        document.getElementById('message').value = '';
        loadMessages();
    })
    .catch(error => console.error('Error:', error));
});

function loadMessages() {
    const token = localStorage.getItem('token');
    fetch(`${apiUrl}/get_messages`, {  
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`
        }
    })
    .then(response => response.json())
    .then(data => {
        const chatWindow = document.getElementById('chatWindow');
        chatWindow.innerHTML = '';
        data.forEach(message => {
            const messageElement = document.createElement('div');
            messageElement.textContent = `${message.timestamp}: ${message.content}`;
            chatWindow.appendChild(messageElement);
        });
    })
    .catch(error => console.error('Error:', error));
}

// Load messages when the chat page loads
if (window.location.pathname.endsWith('chatInterface.html')) {
    document.addEventListener('DOMContentLoaded', loadMessages);
}
