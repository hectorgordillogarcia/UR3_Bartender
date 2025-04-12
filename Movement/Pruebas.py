from RTDE_Commands import connect_robot
from RTDE_Commands import getActualJointPosition
from RTDE_Commands import FreeMovement
from RTDE_Commands import EndFreeMovement
from RTDE_Commands import moveJ
from RTDE_Commands import setTcp
from RTDE_Commands import descendRobotZ
from RTDE_Commands import ascendRobotZ
from RTDE_Commands import getActualTCPPose
from RTDE_Commands import CloseGrip
from RTDE_Commands import OpenGrip
from RTDE_Commands import getActualTCPPose
from RTDE_Commands import moveJ_IK

from time import sleep




connect_robot()
speed=3.14
acceleration=40

# FreeMovement()
# OpenGrip()
# setTcp(0.095)
#getActualTCPPose()
EndFreeMovement()


# target=getActualTCPPose()
# descendRobotZ(0.05,speed,acceleration)
target_waiting=[-4.4865880648242396, -1.5787021122374476, -1.1955146789550781, -1.6177579365172328, 1.5906552076339722, -0.3840120474444788]#Punto sobre las latas esperando a que se seleccione una (art)
target_place=[-1.2801521460162562, -1.9649402103819789, -0.40669602155685425, -2.2687469921507777, 1.5373504161834717, -0.1708005110370081] #Punto donde dejar las latas (con z más alto) (art)
target_home=[-4.702066961918966, -1.556692199116089, -0.02610006369650364, -1.5276904863170166, 0.03778982162475586, -1.991497818623678] #Punto home (art)
target_pick_aprox=[0.042948067349069474, 0.3990026124820103, 0.25364937298676193, -0.2407990643944119, 3.0269388437851883, -0.007000186691514396]#Punto aprox pick(cart) /Lo da la camara
target_place_aprox=[-0.01481715293329484, -0.4292486261660905, 0.25364937298676193, -3.0995809022198375, -0.3138589113264997, 0.09018782271918903]#Punto aprox place(cart)
target_pick_avoid=[-4.479692999516622, -1.8883339367308558, -0.3588854968547821, -2.422844549218649, 1.5980188846588135, -0.14949161211122686] #Corrdenadas para evitar las otras latas(art)


# moveJ(target_home, speed, acceleration)
# sleep(0.2)
# moveJ(target_waiting, speed, acceleration)
# sleep(1)
# moveJ_IK(target_pick_aprox,speed,acceleration)
# sleep(1)
# descendRobotZ(0.09,speed,acceleration)
# sleep(1)
# CloseGrip()
# sleep(1)
# ascendRobotZ(0.09,speed,acceleration)
# sleep(1)
# moveJ(target_pick_avoid,speed,acceleration)
# sleep(1)
# moveJ(target_place, speed, acceleration)
# sleep(1)
# moveJ_IK(target_place_aprox,speed,acceleration)
# sleep(1)
# descendRobotZ(0.09,speed,acceleration)
# sleep(1)
# OpenGrip()
# sleep(1)
# ascendRobotZ(0.09,speed,acceleration)
# sleep(5)
# moveJ_IK(target_place_aprox,speed,acceleration)
# sleep(1)
# moveJ(target_place,speed,acceleration)
# sleep(1)
# moveJ(target_home, speed, acceleration)
# sleep(0.2)
# print("LLEGADA")
# getActualJointPosition()

