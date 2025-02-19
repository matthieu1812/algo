import socket
import threading

# Configuration du serveur
hote = "10.6.40.66"  # Écoute toutes les interfaces réseau
port = 5000
clients = []

# Création du socket serveur
serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serveur.bind((hote, port))
serveur.listen(5)
print(f"Serveur démarré sur {hote}:{port}")

# Diffusion des messages à tous les clients connectés
def broadcast(message, client_exclu=None):
    for client in clients:
        if client != client_exclu:
            try:
                client.send(message)
            except:
                clients.remove(client)

# Gestion des clients
def handle_client(client, adresse):
    print(f"Nouvelle connexion : {adresse}")
    clients.append(client)
    try:
        while True:
            message = client.recv(1024)
            if not message:
                break
            print(f"{adresse} dit: {message.decode()}")
            broadcast(message, client)
    except:
        pass
    finally:
        print(f"{adresse} déconnecté")
        clients.remove(client)
        client.close()

# Accepter les connexions entrantes
while True:
    client, adresse = serveur.accept()
    threading.Thread(target=handle_client, args=(client, adresse)).start()
