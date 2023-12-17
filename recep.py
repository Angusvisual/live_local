import cv2
import socket
import pickle
import struct
import numpy as np

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

def extract_dominant_colors(image, num_colors):
    dominant_colors_list = []

    colors = image.reshape(-1, image.shape[-1])
    dominant_colors = np.unique(colors, axis=0)

    # Trier les couleurs par luminosité décroissante
    sorted_colors = sorted(dominant_colors, key=lambda c: np.dot(c, [0.299, 0.587, 0.114]), reverse=True)

    dominant_colors_list.extend(sorted_colors)

    # Supprimer les doublons
    unique_dominant_colors = np.unique(dominant_colors_list, axis=0)

    # Sélectionner les n premières couleurs (si disponible)
    selected_colors = unique_dominant_colors[:num_colors]

    return selected_colors

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
    colors= extract_dominant_colors([frame], 150)

    color_display = np.zeros((50, len(colors), 3), dtype=np.uint8)
    for i,color in enumerate(colors):
        color_display[:, i, :] = color
    

    # Afficher le flux avec les couleurs principales aux quatre coins       
    cv2.imshow('Client Video with Dominant Colors', color_display)

    
    cv2.imshow('Client Video', frame)
    # cv2.imshow('Client Video', frame)
    if cv2.waitKey(1) == 13:  # Appuyez sur Entrée pour quitter
        break

# Fermer la connexion et détruire la fenêtre OpenCV
client_socket.close()
cv2.destroyAllWindows()
