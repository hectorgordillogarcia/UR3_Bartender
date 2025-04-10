import rtde_control
import rtde_receive
import rtde_io
import numpy as np
import time


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
    

def check_timeout(condition,affirmation):
    """
    Esperar hasta que la acción se ejecute dentro de un tiempo determinado.
    Parámetros: 
        condition: condición a esperar (función).
        affirmation: si True quiere decir que usas if, sino usas if not.
    """
    timeout=5.0
    interval=0.1
    start_time=time.time()
    if affirmation:
        while condition():
            if time.time()-start_time > timeout:
                print ("Waiting time exceded")
                return False
            time.sleep(interval)
    else:
        while not condition():
            if time.time()-start_time > timeout:
                print ("Waiting time exceded")
                return False
            time.sleep(interval)
            
    return True


def CloseGrip():
    """
    Cerrar pinza.
    """
    print("Closing gripper")
    rtde_i_o.setToolDigitalOut(0,False)
    if(check_timeout(lambda: rtde_r.getDigitalInState(0),True)):
        return False
    rtde_i_o.setToolDigitalOut(1,True)
    if(check_timeout(lambda: rtde_r.getDigitalInState(1),False)):
        return False
    print("Gripper closed")
    return True


def OpenGrip():
    """
    Abrir pinza.
    """
    print("Opening gripper")
    rtde_i_o.setToolDigitalOut(1,False)
    if(check_timeout(lambda: rtde_r.getDigitalInState(1),True)):
        return False
    rtde_i_o.setToolDigitalOut(0,True)
    if(check_timeout(lambda: rtde_r.getDigitalInState(1),False)):
        return False
    print("Gripper opened")
    return True


def moveL(target,speed,acceleration):
    """
    Movimientos lineales a la posición cartesiana (x,y,z,rx,ry,rz) del robot usando cinematica inversa.
    """
    print(f"Moving in linear direction to target {target}")
    rtde_c.moveL(target,speed,acceleration)
    if(check_timeout(lambda: np.allclose(getActualTCPPose(),target,atol=1e-3),False)):
        return False
    print("Target achieved") 
    return True


def moveL_FK(target_q,speed,acceleration):
    """
    Movimientos lineales dando como parámetros las posiciones articulares del robot usando cinematica inversa.
    """
    print(f"Moving in linear direction to target {target_q}")
    rtde_c.moveL(target_q,speed,acceleration)
    if(check_timeout(lambda: np.allclose(getActualTCPPose(),target_q,atol=1e-3),False)):
        return False
    print("Target achieved")
    return True


def moveJ_IK(target,speed,acceleration):
    """
    Muevo el robot a la posición cartesiana (x,y,z,rx,ry,rz). La librería calcula la cinemática inversa y manda moveJ al robot.
    """
    if rtde_c.getInverseKinematicsHasSolution(target):
        print(f"Moving joints to {target} using inverse Kinematics ")
        rtde_c.moveJ_IK(target, 0.2, 0.2)
        if(check_timeout(lambda: np.allclose(getActualTCPPose(),target,atol=1e-3),False)):
            return False
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
    if(check_timeout(lambda: np.allclose(getActualTCPPose(),target_q,atol=1e-3),False)):
        return False
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
    if(check_timeout(lambda: np.allclose(getActualTCPPose(),target,atol=1e-3),False)):
        return False      
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
    if(check_timeout(lambda: np.allclose(getActualTCPPose(),target,atol=1e-3),False)):
        return False      
    print(f"Target reached")
    return True         
     

def setTcp(z_offset):
    """
    Permite establecer la nueva posición del TCP al usar una pinza más larga introduciendo cuanto más larga es esta pinza.
    """
    rtde_c.setTCP(z_offset)
    new_tpcPose=rtde_c.getTCPOffset()
    if(check_timeout(lambda: z_offset==new_tpcPose,False)):
        return False
    
    print(f"Offset updated to {z_offset}")
    return True


def PickAndPlace(target_pick,speed):
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
    acceleration=0.2
    z=0.5 #Distancia en z descender/ascender desde el punto de aproximacion al punto de coger/dejar la lata
    target_home=[0.064,0.472,0.086,0.477,-3.25,-0.012] #Punto home
    target_waiting=[0.064,0.472,0.086,0.477,-3.25,-0.012] #Punto sobre las latas esperando a que se seleccione una
    target_place=[0.064,0.472,0.086,0.477,-3.25,-0.012] #Punto donde dejar las latas (con z más alto)
    can_height=0.5 # coordenada z de la herramienta en el punto de aproximacion a la lata
    TCP_rotation=[0.477,-3.25,-0.012] #rx,rx,yz of the tool

    bOk=connect_robot()
    if(bOk):
        bOk=setTcp(0.5)
    if(bOk):
        bOk=moveJ(target_waiting)
    if(bOk):
        target_pick.extend([can_height,TCP_rotation])
        if target_pick:
            bOk=True
        else:
            bOk=False
    if(bOk):
        bOk=moveJ_IK(target_pick,speed,acceleration)
    if(bOk):
        bOk=descendRobotZ(z)
    if(bOk):
        bOk=CloseGrip()        
    if(bOk):
        bOk=ascendRobotZ(z)
    if(bOk):
        bOk=moveJ(target_place,speed,acceleration)
    if(bOk):
        bOk=descendRobotZ(z)
    if(bOk):
        bOk=OpenGrip()
    if(bOk):
        bOk=ascendRobotZ(z)
    if(bOk):
        moveJ(target_home,speed,acceleration)
    if(bOk):
        print("Pick & Place done succesfully")

