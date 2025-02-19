var socket = io.connect("http://10.6.40.14:5000");  // Remplace par ton IP

let username = "";

function setUsername() {
    username = document.getElementById("username").value;
    if (username.trim() !== "") {
        document.getElementById("loginContainer").classList.add("hidden");
        document.getElementById("chatContainer").classList.remove("hidden");
        document.getElementById("messages").innerHTML = "";  // Efface les messages
        socket.emit("set_username", { username: username });
    }
}

function quitChat() {
    socket.emit("quit_chat");
    document.getElementById("chatContainer").classList.add("hidden");
    document.getElementById("loginContainer").classList.remove("hidden");
}

socket.on("message", function(msg) {
    var messagesDiv = document.getElementById("messages");
    var messageElement = document.createElement("p");

    if (msg.startsWith("🟢") || msg.startsWith("🔴")) {
        messageElement.style.fontStyle = "italic";
        messageElement.style.color = "gray";
    }

    messageElement.textContent = msg;
    messageElement.onclick = function () {
        document.getElementById("message").value = "@" + msg.split(":")[0] + " ";
    };
    messagesDiv.appendChild(messageElement);

    messagesDiv.scrollTop = messagesDiv.scrollHeight;
});

// Met à jour la liste des utilisateurs connectés
socket.on("update_users", function(data) {
    var userList = document.getElementById("userList");
    userList.innerHTML = "";
    data.users.forEach(user => {
        var userItem = document.createElement("li");
        userItem.textContent = user;
        userList.appendChild(userItem);
    });
});

// Envoi du message
function sendMessage() {
    var messageInput = document.getElementById("message");
    var message = messageInput.value;
    if (message.trim() !== "") {
        socket.send(message);
        messageInput.value = "";
    }
}

// Sélecteur d’emoji fonctionnel ✅
document.addEventListener("DOMContentLoaded", function () {
    var emojiPicker = document.getElementById("emoji-picker");
    var emojiBtn = document.getElementById("emoji-btn");

    // Affichage/Masquage du sélecteur d’emojis
    emojiBtn.addEventListener("click", function (event) {
        event.stopPropagation();
        emojiPicker.style.display = (emojiPicker.style.display === "block") ? "none" : "block";
    });

    // Ajoute un emoji au champ texte
    emojiPicker.innerHTML = "😀 😂 😍 😎 🤔 😡 😭 🥰 🔥 💯 🚀".split(" ").map(emoji => 
        `<span style="cursor: pointer; font-size: 20px; margin: 5px;" onclick="addEmoji('${emoji}')">${emoji}</span>`
    ).join("");

    // Ferme le sélecteur si on clique ailleurs
    document.addEventListener("click", function () {
        emojiPicker.style.display = "none";
    });

    // Empêche la fermeture quand on clique dans le sélecteur
    emojiPicker.addEventListener("click", function (event) {
        event.stopPropagation();
    });
});

// Fonction pour ajouter un emoji au champ de texte
function addEmoji(emoji) {
    var messageInput = document.getElementById("message");
    messageInput.value += emoji;
}