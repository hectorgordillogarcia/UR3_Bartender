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
from RTDE_Commands import disconnect_robot


from time import sleep




connect_robot()
# disconnect_robot()
speed=3.14
acceleration=40

# FreeMovement()
# OpenGrip()
# setTcp(0.095)
#getActualTCPPose()
# EndFreeMovement()

# target=getActualTCPPose()
# descendRobotZ(0.05,speed,acceleration)
target_waiting=[-4.4865880648242396, -1.5787021122374476, -1.1955146789550781, -1.6177579365172328, 1.5906552076339722, -0.3840120474444788]#Punto sobre las latas esperando a que se seleccione una (art)
target_place=[-1.2801521460162562, -1.9649402103819789, -0.40669602155685425, -2.2687469921507777, 1.5373504161834717, -0.1708005110370081] #Punto donde dejar las latas (con z más alto) (art)
target_home=[-4.702066961918966, -1.556692199116089, -0.02610006369650364, -1.5276904863170166, 0.03778982162475586, -1.991497818623678] #Punto home (art)
target_pick_aprox=[0.04505563001505332, 0.39932209660698537, 0.253729100513867, 2.027830746211192, 2.332344155878057, -0.0032578819630350144]#Punto aprox pick(cart) /Lo da la camara
target_place_aprox=[-0.01481715293329484, -0.4292486261660905, 0.25364937298676193, -3.0995809022198375, -0.3138589113264997, 0.09018782271918903]#Punto aprox place(cart)
target_pick_avoid=[-4.479692999516622, -1.8883339367308558, -0.3588854968547821, -2.422844549218649, 1.5980188846588135, -0.14949161211122686] #Corrdenadas para evitar las otras latas(art)


spot1_look= [-0.6713736693011683, -2.2307025394835414, -0.30557548999786377, -1.8621145687498988, 1.5137308835983276, -3.343515698109762]
spot2_look=[-0.9616254011737269, -2.230446001092428, -0.30562692880630493, -1.8544603786864222, 1.5558314323425293, -3.4482832590686243]
spot3_look=[-1.2912572065936487, -2.230882307092184, -0.30519211292266846, -1.8942200146117152, 1.485101342201233, -3.166631285344259]
spot4_look=[-1.6354077498065394, -2.2297684154906214, -0.3059040307998657, -1.858605524102682, 1.4845449924468994, -3.2415457407580774]



spot1_take=[-0.6728633085833948, -2.23075070003652, -0.305356502532959, -2.1807872257628382, 1.570326805114746, -1.670053784047262]
spot2_take=[-0.9643738905536097, -2.2303158245482386, -0.30557548999786377, -2.181622167626852, 1.564204454421997, -1.6701462904559534]
spot3_take=[-1.2916091124164026, -2.2308742008604945, -0.3051762580871582, -2.180739542047018, 1.570370078086853, -1.670065704976217]
spot4_take=[-1.6367858091937464, -2.2297517261900843, -0.30572381615638733, -2.181605478326315, 1.564192533493042, -1.6701529661761683]






moveJ(target_home, speed, acceleration)
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
getActualJointPosition()





# moveJ(spot3_look, 1, acceleration)
# sleep(1)
# moveJ(spot3_take,1,acceleration)
# sleep(1)
# descendRobotZ(0.09,1,acceleration)
# sleep(1)
# ascendRobotZ(0.09,1,acceleration)
# sleep(1)
# getActualJointPosition()