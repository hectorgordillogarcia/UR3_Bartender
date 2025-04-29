
import sys
import os
import numpy as np
import cv2


# Ruta a Movement
sys.path.append(os.path.join(os.getcwd(), '..', 'Movement'))

#Ruta a Vision/RealSense
sys.path.append(os.path.join(os.getcwd(), '..', 'Vision/RealSense'))

#Ruta a Vision/YOLO
sys.path.append(os.path.join(os.getcwd(), '..', 'Vision/YOLO'))

from Prediction_YOLO import getCanCentroid

def testCamera(SelectedDrink):
    '''
    Testea la visión usando la RealSense
    '''
    from realsense_utils import getCanCoordinates
    from realsense_utils import convertCoordinates
    from realsense_utils import capture_single_frame

    width=0.1
    height=0.1
    d_cam_robot=0.815
    
    #Call RealSense take picture
    [color_image, depth_frame, intrinsics]=capture_single_frame()


    #Call YOLO (funcion ...)
    result = getCanCentroid(color_image, SelectedDrink)
    if not result:
        return False
    x, y = result
    print(f"Centroide lata: x={x}, y={y}")


    #Call RealSense 
    point_coordinates = getCanCoordinates(x, y, width, height,intrinsics,depth_frame)  # Devuelve x'={point_coordinates[0]}, y'={point_coordinates[1]}, z'={point_coordinates[2]}"
    print(f"Centro de la lata (camara): x={point_coordinates[0]}, y={point_coordinates[1]}, z={point_coordinates[2]}")
    # Convertir las coordenadas al sistema de referencia del robot
    canRobotCoords = convertCoordinates(point_coordinates, [0, 0, d_cam_robot], [np.pi/2, 0, 0])
    print(f"Centro de la lata (robot): x'={canRobotCoords[0]}, y'={canRobotCoords[1]}, z'={canRobotCoords[2]}") 
    #Creo que x es las coordenadas de la lata hacia los lados del robot
    # z es la distancia de la lata al robot
    target_pick=[canRobotCoords[0],canRobotCoords[2]]


def testImage(SelectedDrink):
    '''
    Testea el YOLO usando una imagen introducida
    '''
    
    image_path = os.path.join(os.getcwd(), '..', 'Vision', 'YOLO', 'Pruebas5.png')

    # Cargar la imagen con OpenCV
    color_image = cv2.imread(image_path)


    #Call YOLO (funcion ...)
    result = getCanCentroid(color_image, SelectedDrink)
    if not result:
        return False
    x, y = result
    print(f"Centroide lata (YOLO): x={x}, y={y}")



def main():
    bebidas = {
        "1": "fanta",
        "2": "cocacola",
        "3": "aquarius"
    }
    while True:
        print("Seleccione una bebida:")
        print("1 - Fanta")
        print("2 - CocaCola")
        print("3 - Aquarius")
        seleccion = input("Introduzca 1, 2 o 3: ")

        if seleccion in bebidas:
            SelectedDrink = bebidas[seleccion]
            break
        else:
            print("Selección no válida. Intente de nuevo.")

    testCamera(SelectedDrink)
    # testImage(SelectedDrink)

if __name__ == "__main__":
    main()
