
import sys
import os
import numpy as np
import cv2
from realsense_utils import capture_single_frame


#Ruta a Vision/RealSense
sys.path.append(os.path.join(os.getcwd(), '..', 'Vision/RealSense'))

def situateCamera():
    # Añadir la ruta a sys.path
    sys.path.append(os.path.join(os.getcwd(), '..', 'Vision/RealSense'))
    
    # Capturar imagen con RealSense
    color_image, depth_frame, intrinsics = capture_single_frame()
    
    # Obtener dimensiones de la imagen
    height, width, _ = color_image.shape
    center_x, center_y = width // 2, height // 2

    # Dibujar un círculo rojo en el centro de la imagen
    cv2.circle(color_image, (center_x, center_y), 5, (0, 0, 255), -1)

    # Usar la misma ruta para guardar la imagen
    save_dir = os.path.join(os.getcwd(), '..', 'Vision/RealSense')
    save_path = os.path.join(save_dir, "PosicionCamara.png")

    # Guardar imagen
    cv2.imwrite(save_path, color_image)


def main():
    situateCamera()

if __name__ == "__main__":
    main()
