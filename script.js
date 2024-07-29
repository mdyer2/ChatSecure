const apiUrl = window.location.origin;

// Fetch and display users
function loadUsers() {
    fetch(`${apiUrl}/users`, {
        method: 'GET',
    })
    .then(response => response.json())
    .then(data => {
        const receiverSelect = document.getElementById('receiverSelect');
        data.forEach(user => {
            const option = document.createElement('option');
            option.value = user.id;
            option.textContent = user.username;
            receiverSelect.appendChild(option);
        });
    })
    .catch(error => console.error('Error:', error));
}

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
        body: JSON.stringify({ username, email, password })
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
    const receiverId = document.getElementById('receiverSelect').value;
    const token = localStorage.getItem('token');

    fetch(`${apiUrl}/send_message`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ receiver_id: receiverId, content: message })
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
    fetch(`${apiUrl}/get_messages/1`, {  // Replace 1 with the actual receiver_id
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

// Load users when the chat page loads
if (window.location.pathname.endsWith('chatInterface.html')) {
    document.addEventListener('DOMContentLoaded', loadUsers);
    document.addEventListener('DOMContentLoaded', loadMessages);
}
