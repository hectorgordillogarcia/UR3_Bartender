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
import json
import time

# Ruta a Movement
sys.path.append(os.path.join(os.getcwd(), '..', 'Movement'))

#Ruta a Vision/RealSense
sys.path.append(os.path.join(os.getcwd(), '..', 'Vision/RealSense'))

#Ruta a Vision/YOLO
sys.path.append(os.path.join(os.getcwd(), '..', 'Vision/YOLO'))


# Ahora puedes importar la función desde movement.py
from RTDE_Commands import PickAndPlace
from RTDE_Commands import connect_robot
from realsense_utils import capture_single_frame
from realsense_utils import getCanCoordinates
from realsense_utils import convertCoordinates
from Prediction_YOLO import getCanCentroid

ELECCION_FILE= "eleccion.json"

def waiterRobot(SelectedDrink):
    width=0.1
    height=0.1
    d_cam_robot=0.763  #Cambiar
    speed=2.9
    #Call GUI (funcion ...) #aqui que nos diga la bebida deseada
    

    #Call RealSense take picture
    [img, depth_frame, intrinsics]=capture_single_frame()


    #Call YOLO (funcion ...)
    result = getCanCentroid(img, SelectedDrink)
    if not result:
        return False
    x, y = result
    print(f"Centroide lata (YOLO): x={x}, y={y}")

    #Call RealSense 
    point_coordinates = getCanCoordinates(x, y, width, height,intrinsics,depth_frame)  # Devuelve x'={point_coordinates[0]}, y'={point_coordinates[1]}, z'={point_coordinates[2]}"
    print(f"Centro de la lata (camara): x={point_coordinates[0]}, y={point_coordinates[1]}, z={point_coordinates[2]}")
    # Convertir las coordenadas al sistema de referencia del robot
    canRobotCoords = convertCoordinates(point_coordinates, [0, 0, d_cam_robot], [np.pi/2, 0, 0])
    print(f"Centro de la lata (robot): x'={canRobotCoords[0]}, y'={canRobotCoords[1]}, z'={canRobotCoords[2]}") 
    #Creo que x es las coordenadas de la lata hacia los lados del robot
    # y z es la distancia de la lata al robot
    target_pick=[-canRobotCoords[0],canRobotCoords[1]]
    

    print(f"Trarget Pick: x'={target_pick[0]}, y'={target_pick[1]},") 

    #Call Robot RTDE (funcion PickAndPlace(target_pick,speed))
    PickAndPlace(target_pick,speed)
    return True
        

def main():
    connect_robot()
    print("Sistema de visión y brazo robótico listo. Esperando órdenes desde eleccion.py...")
    with open(ELECCION_FILE, "w") as f_out:
        json.dump({"estado": "libre"}, f_out)
    while True:
        try:
            with open(ELECCION_FILE, "r") as f:
                data = json.load(f)
                if data.get("estado") == "ocupado":
                    bebida = data.get("eleccion")
                    print(f"Orden recibida: {bebida}")
                    success = waiterRobot(bebida)
                    print(success)
                    if success:
                        print("siucess")
                        with open(ELECCION_FILE, "w") as f_out:
                            json.dump({"estado": "libre"}, f_out)
                    else:
                        print("siucess")
                        with open(ELECCION_FILE, "w") as f_out:
                            json.dump({"estado": "libre"}, f_out)

        except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
            print("Esperando archivo válido o elección...")

        time.sleep(1)

if __name__== "__main__":
    main()
