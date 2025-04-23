# Este es el programa launcher. Sólo será necesario ejecutar este .py para entregar una lata deseada


# En caso de que nuestras funciones de realsense o yolo cualquier otra estén en carpetas distintas usaremos:
# import sys
# # Añade la ruta absoluta de la carpeta 'hafo'
# sys.path.append('/ruta/a/tu/carpeta/')

# # Ahora puedes importar la función
# from archivo_py import funcion_deseada
import sys
import os
import numpy as np


# Ruta a Movement
sys.path.append(os.path.join(os.getcwd(), '..', 'Movement'))

#Ruta a Vision/RealSense
sys.path.append(os.path.join(os.getcwd(), '..', 'Vision/RealSense'))

#Ruta a Vision/YOLO
sys.path.append(os.path.join(os.getcwd(), '..', 'Vision/YOLO'))


# Ahora puedes importar la función desde movement.py
from RTDE_Commands import PickAndPlace
from realsense_utils import capture_single_frame
from realsense_utils import getCanCoordinates
from realsense_utils import convertCoordinates
from Prediction_YOLO import getCanCentroid


def waiterRobot():
    width=0.05
    height=0.05
    d_cam_robot=0.8  #Cambiar
    speed=3.14
    #Call GUI (funcion ...) #aqui que nos diga la bebida deseada
    #Mientras no hay interfaz probaremos con esto:
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
        seleccion = input("Pulse 1, 2 o 3: ")

        if seleccion in bebidas:
            SelectedDrink = bebidas[seleccion]
            break
        else:
            print("Selección no válida. Intente de nuevo.")

    #Call RealSense take picture
    [img, depth_frame, intrinsics]=capture_single_frame()

    #Call YOLO (funcion ...)
    [x,y]=getCanCentroid(img,SelectedDrink)
    print(f"Centroide lata {SelectedDrink}: x={x}, y={y}")

    #Call RealSense 
    point_coordinates = getCanCoordinates(x, y, width, height,intrinsics,depth_frame)  # Devuelve x'={point_coordinates[0]}, y'={point_coordinates[1]}, z'={point_coordinates[2]}"
    print(f"Centro de la lata (camara): x={point_coordinates[0]}, y={point_coordinates[1]}, z={point_coordinates[2]}")
    # Convertir las coordenadas al sistema de referencia del robot
    canRobotCoords = convertCoordinates(point_coordinates, [0, 0, d_cam_robot], [np.pi/2, 0, 0])
    print(f"Centro de la lata (robot): x'={canRobotCoords[0]}, y'={canRobotCoords[1]}, z'={canRobotCoords[2]}") 
    #Creo que x es las coordenadas de la lata hacia los lados del robot
    # y z es la distancia de la lata al robot
    target_pick=[canRobotCoords[0],canRobotCoords[2]]


    #Call Robot RTDE (funcion PickAndPlace(speed)
    PickAndPlace(target_pick,speed)
        

def main():
    waiterRobot()

if __name__ == "__main__":
    main()
