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
from realsense_utils import capture_single_frame
from Prediction_YOLO import getCanCentroid


def waiterRobot():
    width=0.05
    height=0.05
    d_cam_robot=1
    speed=3.14
    #Call GUI (funcion ...) #aqui que nos diga la bebida deseada
    desiredDrink="fanta"

    #Call RealSense take picture
    [color_image, depth_frame, intrinsics]=capture_single_frame()

    #Call YOLO (funcion ...)
    [x,y]=getCanCentroid(color_image,desiredDrink)

    #Call RealSense (funcion GetRobotCoord(x_normalized,y_normalized,window_width,window_height,d_cam_robot))
    target_pick=GetRobotCoord(x,y,width,height,d_cam_robot)

    #Call Robot RTDE (funcion PickAndPlace(speed)
    PickAndPlace(target_pick,speed)
        

def main():
    waiterRobot()

if __name__ == "__main__":
    main()