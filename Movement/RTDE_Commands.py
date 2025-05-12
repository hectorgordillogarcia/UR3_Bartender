import rtde_control
import rtde_receive
import rtde_io
import numpy as np
import time
from time import sleep



Sleeptime=0.5
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
    
def disconnect_robot():
    rtde_c.disconnect()
    
    
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

def MoveHome(speed):
    acceleration=1
    target_home=[-4.702066961918966, -1.556692199116089, -0.02610006369650364, -1.5276904863170166, 0.03778982162475586, -1.991497818623678] #Punto home (art)
    bOk=moveJ(target_home,speed,acceleration)

    return bOk

    
    

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
    acceleration=1

    z=0.09 #Altura aproximacion
    
    target_waiting=[-4.4865880648242396, -1.5787021122374476, -1.1955146789550781, -1.6177579365172328, 1.5906552076339722, -0.3840120474444788]#Punto sobre las latas esperando a que se seleccione una (art)
    target_place=[-1.2801521460162562, -1.9649402103819789, -0.40669602155685425, -2.2687469921507777, 1.5373504161834717, -0.1708005110370081] #Punto donde dejar las latas (con z más alto) (art)
    target_home=[-4.702066961918966, -1.556692199116089, -0.02610006369650364, -1.5276904863170166, 0.03778982162475586, -1.991497818623678] #Punto home (art)
    target_place_aprox=[-0.01481715293329484, -0.4292486261660905, 0.25364937298676193, -3.0995809022198375, -0.3138589113264997, 0.09018782271918903]#Punto aprox place(cart)
    target_pick_avoid=[-4.479692999516622, -1.8883339367308558, -0.3588854968547821, -2.422844549218649, 1.5980188846588135, -0.14949161211122686] #Corrdenadas para evitar las otras latas(art)
    
    aprox_height= 0.25364937298676193 # z aprox para todas las latas    
    TCP_rotation=[2.027830746211192, 2.332344155878057, -0.0032578819630350144] #rx,rx,yz of the tool
    target_pick_aprox.extend([aprox_height,*TCP_rotation])
        
    print(f"Aprox Target Pick:{target_pick_aprox}") 
    
    
    bOk=moveJ(target_waiting,speed,acceleration)
    if(bOk):
        bOk=moveJ_IK(target_pick_aprox,speed,acceleration)
    if(bOk):
        bOk=descendRobotZ(z,0.1,0.5)
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

def PickMovement(target_pick_aprox,speed):
    '''
    Hace solo el proceso de pick y se situa cerca de los spot de place
    '''
    acceleration=1
    z=0.09 #Altura aproximacion
    

    # PICK TARGETS
    target_waiting=[-4.4865880648242396, -1.5787021122374476, -1.1955146789550781, -1.6177579365172328, 1.5906552076339722, -0.3840120474444788]#Punto sobre las latas esperando a que se seleccione una (art)
    target_home=[-4.702066961918966, -1.556692199116089, -0.02610006369650364, -1.5276904863170166, 0.03778982162475586, -1.991497818623678] #Punto home (art)
    target_pick_avoid=[-4.479692999516622, -1.8883339367308558, -0.3588854968547821, -2.422844549218649, 1.5980188846588135, -0.14949161211122686] #Corrdenadas para evitar las otras latas(art)
    
    aprox_height= 0.25364937298676193 # altura donde dejar las latas   
    TCP_rotation=[2.027830746211192, 2.332344155878057, -0.0032578819630350144] #rx,rx,yz of the tool
    target_pick_aprox.extend([aprox_height,*TCP_rotation])

    #PLACE TARGETS
    target_place=[-1.2801521460162562, -1.9649402103819789, -0.40669602155685425, -2.2687469921507777, 1.5373504161834717, -0.1708005110370081] #Punto donde dejar las latas (con z más alto) (art)

    #RUN
    print(f"Aprox Target Pick:{target_pick_aprox}")
    
    bOk=moveJ(target_waiting,speed,acceleration)
    if(bOk):
        bOk=moveJ_IK(target_pick_aprox,speed,acceleration)
    if(bOk):
        bOk=descendRobotZ(z,0.1,0.5)
    if(bOk):
        bOk=CloseGrip()        
    if(bOk):
        bOk=ascendRobotZ(z,speed,acceleration)
    if(bOk):
        bOk=moveJ(target_pick_avoid,speed,acceleration)
    if(bOk):
        bOk=moveJ(target_place,speed,acceleration)

    return bOk

def GoToPlaceCheck(Position,speed):
    '''
    Va a la posicion donde comprueba con la RobotCam si el hueco esta libre
    '''
    acceleration=1
    spot1_check= [-0.6713736693011683, -2.2307025394835414, -0.30557548999786377, -1.8621145687498988, 1.5137308835983276, -3.343515698109762]
    spot2_check=[-0.9616254011737269, -2.230446001092428, -0.30562692880630493, -1.8544603786864222, 1.5558314323425293, -3.4482832590686243]
    spot3_check=[-1.2912572065936487, -2.230882307092184, -0.30519211292266846, -1.8942200146117152, 1.485101342201233, -3.166631285344259]
    spot4_check=[-1.6354077498065394, -2.2297684154906214, -0.3059040307998657, -1.858605524102682, 1.4845449924468994, -3.2415457407580774]
    spots_check = [spot1_check, spot2_check, spot3_check, spot4_check] #Coordenadas donde la camara revisa si hay hueco (articulares)

    moveJ(spots_check[Position], speed, acceleration)  # Go to position where camera checks

def PlaceCan(Position,speed):
    '''
    Coloca la lata en el spot definido
    '''
    acceleration=1
    z=0.09 #Altura aproximacion

    target_waiting=[-4.4865880648242396, -1.5787021122374476, -1.1955146789550781, -1.6177579365172328, 1.5906552076339722, -0.3840120474444788]#Punto sobre las latas esperando a que se seleccione una (art)

    spot1_place=[-0.6728633085833948, -2.23075070003652, -0.305356502532959, -2.1807872257628382, 1.570326805114746, -1.670053784047262]
    spot2_place=[-0.9643738905536097, -2.2303158245482386, -0.30557548999786377, -2.181622167626852, 1.564204454421997, -1.6701462904559534]
    spot3_place=[-1.2916091124164026, -2.2308742008604945, -0.3051762580871582, -2.180739542047018, 1.570370078086853, -1.670065704976217]
    spot4_place=[-1.6367858091937464, -2.2297517261900843, -0.30572381615638733, -2.181605478326315, 1.564192533493042, -1.6701529661761683]

    spots_place = [spot1_place, spot2_place, spot3_place, spot4_place] #Coordenadas donde se coloca la lata (articualares)

    #RUN
    bOk = moveJ(spots_place[Position], speed, acceleration)  # Go to place position if it's empty
    if(bOk):
        bOk=descendRobotZ(z,speed,acceleration)
    if(bOk):
        bOk=OpenGrip()
    if(bOk):
        bOk=ascendRobotZ(z,speed,acceleration)
    if(bOk):
        moveJ(target_waiting,speed,acceleration)
    if(bOk):
        print("Pick & Place logrado con exito")

