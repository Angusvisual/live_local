import cv2
import socket
import pickle
import struct
import numpy as np
from skimage import color

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
    # Convertir l'image en mode couleur LAB pour mieux représenter la perception humaine
    lab_image = cv2.cvtColor(image, cv2.COLOR_BGR2Lab)

    # Réduire les dimensions de l'image pour accélérer le traitement
    small_image = cv2.resize(lab_image, (100, 100))

    # À présent, 'small_image' est une image de petite taille que vous pouvez utiliser pour extraire les couleurs dominantes
    colors = small_image.reshape(-1, 3)

    # Trier les couleurs par luminosité décroissante
    luminosity = color.rgb2gray(colors)
    sorted_indices = luminosity.argsort()[::-1]
    sorted_colors = colors[sorted_indices]

    # Supprimer les doublons
    _, unique_indices = np.unique(sorted_colors, axis=0, return_index=True)
    unique_dominant_colors = sorted_colors[unique_indices]

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
