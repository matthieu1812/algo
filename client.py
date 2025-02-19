import socket
import threading

# Paramètres du serveur
serveur_ip = "10.6.40.66"  # Remplace par l'IP de ton serveur
port = 5000

# Création du socket client
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((serveur_ip, port))

# Fonction pour recevoir les messages
def recevoir_messages():
    while True:
        try:
            message = client.recv(1024).decode()
            if message:
                print("\n" + message)
        except:
            print("Connexion interrompue.")
            client.close()
            break

# Lancer un thread pour écouter les messages
threading.Thread(target=recevoir_messages, daemon=True).start()

# Boucle pour envoyer les messages
print("Tapez vos messages et appuyez sur Entrée pour envoyer.")
while True:
    message = input("")
    if message.lower() == "quit":
        break
    client.send(message.encode())

client.close()
