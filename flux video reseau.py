import cv2
import socket
import pickle
import struct

# Configurer le socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_ip = '192.168.1.74'
port = 1234
socket_address = (host_ip, port)

# Liaison du socket et écoute
server_socket.bind(socket_address)
server_socket.listen(1)  # Limiter le nombre de connexions simultanées à 1

print("En attente de la connexion du client...")
client_socket, addr = server_socket.accept()
print('Connexion depuis :', addr)

# Configurer la webcams
cap = cv2.VideoCapture(3)

try:
    while True:
        ret, photo = cap.read()

        # Redimensionner l'image à une taille spécifique (par exemple, 640x480)
        photo = cv2.resize(photo, (320, 240))

        # Encoder l'image redimensionnée
        data = pickle.dumps(photo)
        message_size = struct.pack("L", len(data))

        # Envoyer la taille du message et les données
        client_socket.sendall(message_size + data)

        # Attendre une courte période pour éviter une utilisation excessive du CPU
        cv2.waitKey(1)

except KeyboardInterrupt:
    pass

finally:
    # Fermer la connexion et libérer les ressources
    client_socket.close()
    cap.release()
    cv2.destroyAllWindows()
