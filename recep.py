import cv2
import socket
import pickle
import struct

# Configurer le socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_ip = '192.168.1.74'
port = 1234
socket_address = (host_ip, port)

# Se connecter au serveur
client_socket.connect(socket_address)
data = b""
payload_size = struct.calcsize("L")

# Définir la taille de la fenêtre OpenCV
cv2.namedWindow('Client Video', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Client Video', 1920, 1080)

while True:
    while len(data) < payload_size:
        packet = client_socket.recv(4 * 1024)
        if not packet:
            break
        data += packet

    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("L", packed_msg_size)[0]

    while len(data) < msg_size:
        data += client_socket.recv(4 * 1024)

    frame_data = data[:msg_size]
    data = data[msg_size:]
    frame = pickle.loads(frame_data)

    # Afficher le flux de la webcam
    cv2.imshow('Client Video', frame)
    if cv2.waitKey(1) == 13:  # Appuyez sur Entrée pour quitter
        break

# Fermer la connexion et détruire la fenêtre OpenCV
client_socket.close()
cv2.destroyAllWindows()
