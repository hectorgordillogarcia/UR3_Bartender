
import sys
import os

# Ruta a Movement
sys.path.append(os.path.join(os.getcwd(), '..', 'Movement'))

#Ruta a Vision/RealSense
sys.path.append(os.path.join(os.getcwd(), '..', 'Vision/RealSense'))

#Ruta a Vision/YOLO
sys.path.append(os.path.join(os.getcwd(), '..', 'Vision/YOLO'))

from realsense_main import GetRobotCoord
from realsense_utils import capture_single_frame
from Prediction_YOLO import getCanCentroid

def testCamera(SelectedDrink):

    width=0.1
    height=0.1
    d_cam_robot=0.8
    
    #Call RealSense take picture
    [color_image, depth_frame, intrinsics]=capture_single_frame()

    #Call YOLO to get x,y

    centroid=getCanCentroid(color_image,SelectedDrink)
    if centroid is False:
        return False
    
    x=centroid[0]
    y=centroid[1]
    #Call RealSense (funcion GetRobotCoord(x_normalized,y_normalized,window_width,window_height,d_cam_robot))
    target_pick=GetRobotCoord(x,y,width,height,d_cam_robot,intrinsics,depth_frame)

def main():
    validDrinks = ["fanta", "cocacola", "aquarius"]
    while True:
        SelectedDrink = input("Seleccione fanta, cocacola o aquarius: ").lower()
        if SelectedDrink in validDrinks:
            break
        else:
            print("Bebida no disponible. Intente de nuevo.")

    testCamera(SelectedDrink)

if __name__ == "__main__":
    main()