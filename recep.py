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

# Se connecter au serveurn
client_socket.connect(socket_address)
data = b""
payload_size = struct.calcsize("L")

# Définir la taille de la fenêtre OpenCV
cv2.namedWindow('Client Video', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Client Video', 1920, 1080)

def extract_dominant_colors(image, num_colors):
    border_width = 5
    top_border = image[:border_width, :, :]
    bottom_border = image[-border_width:, :, :]
    left_border = image[:, :border_width, :]
    right_border = image[:, -border_width:, :]

    # Appliquer un effet de "glow" sur chaque bordure
    top_border = cv2.GaussianBlur(top_border, (0, 0), 5)
    bottom_border = cv2.GaussianBlur(bottom_border, (0, 0), 5)
    left_border = cv2.GaussianBlur(left_border, (0, 0), 5)
    right_border = cv2.GaussianBlur(right_border, (0, 0), 5)


    cv2.imshow('top Borders', top_border)
    cv2.imshow('bottom Borders', bottom_border)
    cv2.imshow('left Borders', left_border)
    cv2.imshow('right Borders', right_border)
    
    # Convertir les couleurs des bords en liste
    # edge_colors = borders.reshape(-1, 3)
    
    # return edge_colors
count = 0
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
    count+=1
    
    colors= extract_dominant_colors(frame, 150)

    # Afficher le flux avec les couleurs principales aux quatre coins       
    # cv2.imshow('Client Video with Dominant Colors', color_display)

    
    cv2.imshow('Client Video', frame)
    # cv2.imshow('Client Video', frame)
    if cv2.waitKey(1) == 13:  # Appuyez sur Entrée pour quitter
        break

# Fermer la connexion et détruire la fenêtre OpenCV
client_socket.close()
cv2.destroyAllWindows()
