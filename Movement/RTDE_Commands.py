import rtde_control
import rtde_receive
import rtde_io
import numpy as np
import time
from time import sleep

Sleeptime=0.3
# En este codigo python aparecen todas las funciones útiles de rtde que emplearemos en el ur3.
# Para utilizar cualquiera de ellas añade a tus primeras líneas de tu archivo python:
#     from RTDE_Commands import funcion_a_usar
# Todas las funciones empleadas vienen bien detalladas en el RTDE_Commands_Documentation.md  Escrita por nosotros.


def connect_robot():
    """
    Conecta con el robot. Inicializa interfaces de control, recepción e IO.
    """
    global rtde_c
    global rtde_r 
    global rtde_i_o
    rtde_c = rtde_control.RTDEControlInterface("169.254.12.28")
    rtde_r = rtde_receive.RTDEReceiveInterface("169.254.12.28")
    rtde_i_o = rtde_io.RTDEIOInterface("169.254.12.28")

    if(rtde_c.isConnected() and rtde_r.isConnected()):
        print("Robot connected successfully")
        return True
    else:
        print("Unable to connect to the robot")
        return False
    
def FreeMovement():
    """
Libera todas las articulaciones del robot para poder mover manualmente el robot con total libertad.  
    """
    rtde_c.freedriveMode()

def EndFreeMovement():
    """
    Deshabilita el libre movimiento de las articulaciones para poder utilizar moveJ,...
    """
    rtde_c.endFreedriveMode()


def CloseGrip():
    """
    Cerrar pinza.
    """
    print("Closing gripper")
    rtde_i_o.setToolDigitalOut(0,False)
    rtde_i_o.setToolDigitalOut(1,True)
    sleep(Sleeptime)
    if(rtde_r.getDigitalInState(1),True):
        print("Gripper closed")
        return True
    else: 
        return False


def OpenGrip():
    """
    Abrir pinza.
    """
    print("Opening gripper")
    rtde_i_o.setToolDigitalOut(1,False)
    rtde_i_o.setToolDigitalOut(0,True)
    sleep(Sleeptime)
    if(rtde_r.getDigitalInState(1),False):
        print("Gripper opened")
        return True
    else:
        return False


def moveL(target,speed,acceleration):
    """
    Movimientos lineales a la posición cartesiana (x,y,z,rx,ry,rz) del robot usando cinematica inversa.
    """
    print(f"Moving in linear direction to target {target}")
    rtde_c.moveL(target,speed,acceleration)
    sleep(Sleeptime)
    print("Target achieved") 
    return True


def moveL_FK(target_q,speed,acceleration):
    """
    Movimientos lineales dando como parámetros las posiciones articulares del robot usando cinematica inversa.
    """
    print(f"Moving in linear direction to target {target_q}")
    rtde_c.moveL(target_q,speed,acceleration)
    sleep(Sleeptime)
    print("Target achieved")
    return True


def moveJ_IK(target,speed,acceleration):
    """
    Muevo el robot a la posición cartesiana (x,y,z,rx,ry,rz). La librería calcula la cinemática inversa y manda moveJ al robot.
    """
    if rtde_c.getInverseKinematicsHasSolution(target):
        print(f"Moving joints to {target} using inverse Kinematics ")
        rtde_c.moveJ_IK(target, 0.2, 0.2)
        sleep(Sleeptime)
        print("Target achieved")
        return True          
    else: 
        print("Kinematics could not been resolved")
        return False
    

def moveJ(target_q,speed,acceleration):
    """
    Muevo el robot a la posición articular dando como entrada las posiciones articulares.
    """
    print(f"Moving joints to target {target_q}")
    rtde_c.moveJ(target_q,speed,acceleration)
    sleep(Sleeptime)
    print("Target achieved")
    return True


def getActualJointPosition():
    """
    Obtengo las posición actual de las articulaciones del robot (para usar moveJ).
    """
    jointPositions=rtde_r.getActualQ()
    print(f"Actual joint positions: {jointPositions}")
    return jointPositions


def getActualTCPPose():
    """
    Obtengo las coordenadas de la herramienta (x,y,z,rx,ry,rz).
    """
    TCPPose=rtde_r.getActualTCPPose()
    print(f"Actual Position of the tool: {TCPPose}")
    return TCPPose


def descendRobotZ(z,speed,acceleration):
    """
    Desciendo el robot de forma lineal para coger/dejar la lata.
    """
    target=getActualTCPPose()
    target[2]-=z
    print(f"Descending robot {z} meters in z")
    moveL(target,speed,acceleration)
    sleep(Sleeptime)
    print(f"Target reached")
    return True       
       

def ascendRobotZ(z,speed,acceleration):
    """
    Asciendo el robot de forma lineal después de coger/dejar la lata.
    """
    target=getActualTCPPose()
    target[2]+=z
    print(f"Ascending robot {z} meters in z")
    moveL(target,speed,acceleration)
    sleep(Sleeptime)
    print(f"Target reached")
    return True         
     

def setTcp(z_offset):
    """
    Permite establecer la nueva posición del TCP al usar una pinza más larga introduciendo cuanto más larga es esta pinza.
    """
    target=([0.0, 0.0, z_offset, 0.0, 0.0, 0.0])

    rtde_c.setTcp(target)
    new_tpcPose=rtde_c.getTCPOffset()
    sleep(Sleeptime)
    print(f"Offset updated to {z_offset}")
    return True


def PickAndPlace(target_pick_aprox,speed):
    """
    Ejecuta una rutina de pick and place:
    - Conecta con el robot.
    - Establece offset TCP.
    - Se mueve a posición de espera.
    - Obtiene coordenadas de la lata.
    - Se mueve sobre ella, baja, agarra, sube.
    - Va a la bandeja, baja, suelta, sube.
    - Vuelve a home.
    """
    acceleration=40

    z=0.09 #Altura aproximacion
    
    target_waiting=[-4.4865880648242396, -1.5787021122374476, -1.1955146789550781, -1.6177579365172328, 1.5906552076339722, -0.3840120474444788]#Punto sobre las latas esperando a que se seleccione una (art)
    target_place=[-1.2801521460162562, -1.9649402103819789, -0.40669602155685425, -2.2687469921507777, 1.5373504161834717, -0.1708005110370081] #Punto donde dejar las latas (con z más alto) (art)
    target_home=[-4.702066961918966, -1.556692199116089, -0.02610006369650364, -1.5276904863170166, 0.03778982162475586, -1.991497818623678] #Punto home (art)
    target_place_aprox=[-0.01481715293329484, -0.4292486261660905, 0.25364937298676193, -3.0995809022198375, -0.3138589113264997, 0.09018782271918903]#Punto aprox place(cart)
    target_pick_avoid=[-4.479692999516622, -1.8883339367308558, -0.3588854968547821, -2.422844549218649, 1.5980188846588135, -0.14949161211122686] #Corrdenadas para evitar las otras latas(art)
    
    aprox_height= 0.25364937298676193 # z aprox para todas las latas    
    TCP_rotation=[-0.2407990643944119, 3.0269388437851883, -0.007000186691514396] #rx,rx,yz of the tool
    target_pick_aprox.extend([aprox_height,TCP_rotation])
        

    bOk=connect_robot()
    if(bOk):
        bOk=moveJ(target_waiting,speed,acceleration)
    if(bOk):
        bOk=moveJ_IK(target_pick_aprox,speed,acceleration)
    if(bOk):
        bOk=descendRobotZ(z,speed,acceleration)
    if(bOk):
        bOk=CloseGrip()        
    if(bOk):
        bOk=ascendRobotZ(z,speed,acceleration)
    if(bOk):
        bOk=moveJ(target_pick_avoid,speed,acceleration)
    if(bOk):
        bOk=moveJ(target_place,speed,acceleration)
    if(bOk):
        bOk=moveJ_IK(target_place_aprox,speed,acceleration)
    if(bOk):
        bOk=descendRobotZ(z,speed,acceleration)
    if(bOk):
        bOk=OpenGrip()
    if(bOk):
        bOk=ascendRobotZ(z,speed,acceleration)
    if(bOk):
        moveJ(target_waiting,speed,acceleration)
    if(bOk):
        print("Pick & Place done succesfully")

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