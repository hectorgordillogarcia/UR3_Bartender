# Este es el programa launcher. Sólo será necesario ejecutar este .py para entregar una lata deseada


# En caso de que nuestras funciones de realsense o yolo cualquier otra estén en carpetas distintas usaremos:
# import sys
# # Añade la ruta absoluta de la carpeta 'hafo'
# sys.path.append('/ruta/a/tu/carpeta/')

# # Ahora puedes importar la función
# from archivo_py import funcion_deseada
import sys
import os

# Ruta a Movement
sys.path.append(os.path.join(os.getcwd(), '..', 'Movement'))

#Ruta a Vision/RealSense
sys.path.append(os.path.join(os.getcwd(), '..', 'Vision/RealSense'))

#Ruta a Vision/YOLO
sys.path.append(os.path.join(os.getcwd(), '..', 'Vision/YOLO'))


# Ahora puedes importar la función desde movement.py
from RTDE_Commands import PickAndPlace
from realsense_main import GetRobotCoord


def waiterRobot():
    #Call GUI (funcion ...)
    #Call YOLO (funcion ...)
    #Call RealSense (funcion GetRobotCoord(x_normalized,y_normalized,window_width,window_height,d_cam_robot))
    #Call Robot RTDE (funcion PickAndPlace(speed)

    pass #pass auxiliar, borrar cuando se introduzcan los comandos
        

def main():
    waiterRobot()


if __name__ == "__main__":
    main()