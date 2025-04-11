from realsense_utils import getCanCoordinates
from realsense_utils import convertCoordinates
import numpy as np

def GetRobotCoord(x_normalized,y_normalized,window_width,window_height,d_cam_robot):
    # Definir las coordenadas normalizadas
    # x_normalized   # Coordenada X normalizada (entre 0 y 1)
    # y_normalized # Coordenada Y normalizada (entre 0 y 1)
    # window_width  # Anchura de la ventana en la que buscamos el punto más cercano a la cámara (entre 0 y 1)
    # window_height # Altura de la ventana en la que buscamos el punto más cercano a la cámara (entre 0 y 1)
    # d_cam_robot # Distancia entre la cámara y el robot 

    # Obtener las coordenadas 3D en el sistema de referencia de la cámara
    point_coordinates = getCanCoordinates(x_normalized, y_normalized, window_width, window_height)
    print(f"centro de la lata (cámara): x'={point_coordinates[0]}, y'={point_coordinates[1]}, z'={point_coordinates[2]}")

    # Convertir las coordenadas al sistema de referencia del robot
    point_coordinates_robot = convertCoordinates(point_coordinates, [0, 0, d_cam_robot], [np.pi/2, 0, 0])
    print(f"centro de la lata (robot): x'={point_coordinates_robot[0]}, y'={point_coordinates_robot[1]}, z'={point_coordinates_robot[2]}")
    return point_coordinates_robot