from realsense_utils import getCanCoordinates
from realsense_utils import convertCoordinates
import numpy as np

# Definir las coordenadas normalizadas
x_normalized = 0.5  # Coordenada X normalizada (entre 0 y 1)
y_normalized = 0.6  # Coordenada Y normalizada (entre 0 y 1)
window_width = 0.1  # Anchura de la ventana en la que buscamos el punto más cercano a la cámara (entre 0 y 1)
window_height = 0.1  # Altura de la ventana en la que buscamos el punto más cercano a la cámara (entre 0 y 1)
d_cam_robot = 0.6  # Distancia entre la cámara y el robot 

# Obtener las coordenadas 3D en el sistema de referencia de la cámara
point_coordinates = getCanCoordinates(x_normalized, y_normalized, window_width, window_height)
print(f"centro de la lata (cámara): x'={point_coordinates[0]}, y'={point_coordinates[1]}, z'={point_coordinates[2]}")

# Convertir las coordenadas al sistema de referencia del robot
point_coordinates_robot = convertCoordinates(point_coordinates, [0, 0, d_cam_robot], [np.pi/2, 0, 0])
print(f"centro de la lata (robot): x'={point_coordinates_robot[0]}, y'={point_coordinates_robot[1]}, z'={point_coordinates_robot[2]}")