from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, send, emit
from flask_mysqldb import MySQL
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import CSRFProtect
import bcrypt

app = Flask(__name__)
app.config["SECRET_KEY"] = "supersecretkey"

app.config["MYSQL_HOST"] = "127.0.0.1"  # Au lieu de "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "root"  # MAMP utilise souvent "root" par défaut
app.config["MYSQL_DB"] = "site"
app.config["MYSQL_PORT"] = 8889  # Ajoute ceci pour forcer le port MAMP
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
app.config["MYSQL_UNIX_SOCKET"] = "/Applications/MAMP/tmp/mysql/mysql.sock"


mysql = MySQL(app)
socketio = SocketIO(app, cors_allowed_origins="*")

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

users = {}  # Stocke les utilisateurs connectés
messages = []  # Stocke les messages temporairement


# Classe utilisateur pour Flask-Login
class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username


@login_manager.user_loader
def load_user(user_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cur.fetchone()
    cur.close()
    if user:
        return User(user["id"], user["username"])
    return None

@app.route("/", methods=['GET' , 'POST'])
def index():
    if request.method == 'POST':
        users = request.form['users']
        passw = request.form['pass']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT pseudo, password FROM users WHERE pseudo = %s and password= %s ', (users, passw ))
        ajout = cursor.fetchone() 
        if ajout: 
            return render_template("index.html") 
            
        else:
            return "Nom d'utilisateur ou mot de passe incorrect", 401 
        
        
    return render_template("login.html")

@app.route ("/register", methods=['GET', 'POST'])
def register():
   
    if request.method == 'POST':
        nom = request.form['username']
        pseudo = request.form['pseu']
        mot_regis= request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT username,pseu, mot_de FROM creates WHERE pseu = %s', (pseudo,))
        ajout1 = cursor.fetchone()
        if ajout1:  
            return "Nom d'utilisateur déjà pris", 401
        else:
          
            cursor.execute('INSERT INTO creates(username, pseu, mot_de) VALUES (%s, %s, %s)', (nom, pseudo, mot_regis))
            cursor.execute('INSERT INTO users (pseudo, password) VALUES (%s, %s)', (pseudo, mot_regis))

        mysql.connection.commit()  
        cursor.close()  
    return render_template("register.html")


    

# PAGE CHAT (PROTÉGÉE PAR LOGIN)
@app.route("/chat")
@login_required
def chat():
    return render_template("chat.html", username=current_user.username)


# LOGOUT
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


# SOCKET.IO EVENTS
@socketio.on("connect")
def handle_connect():
    if current_user.is_authenticated:
        users[request.sid] = current_user.username
        emit("update_users", {"users": list(users.values())}, broadcast=True)


@socketio.on("disconnect")
def handle_disconnect():
    username = users.pop(request.sid, None)
    if username:
        emit("update_users", {"users": list(users.values())}, broadcast=True)


@socketio.on("message")
def handle_message(data):
    username = users.get(request.sid, "Anonyme")
    send(f"{username}: {data}", broadcast=True)


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
