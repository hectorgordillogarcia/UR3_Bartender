
import rtde_control
import rtde_receive
import rtde_io
import numpy as np
import time
from realsense_main import GetRobotCoord



#Comprobar que el robot esté conectado
def RobotConexion():        
        if(rtde_c.isConnected() and rtde_r.isConnected()):
                return True
        else:
                return False
        

#Esperar hasta que la acción se ejecute dentro de un tiempo determinado. Parametros: condicion a esperar. Affirmation: si True quiere decir que usas if, sino usas if not
def check_timeout(condition,affirmation):
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


#Cerrar pinza
def CloseGrip():
        print("Closing gripper")
        rtde_i_o.setToolDigitalOut(0,False)
        if(check_timeout(lambda: rtde_r.getDigitalInState(0),True)):
                return False
        rtde_i_o.setToolDigitalOut(1,True)
        if(check_timeout(lambda: rtde_r.getDigitalInState(1),False)):
                return False
        print("Gripper closed")
        return True

#Abrir pinza
def OpenGrip():
        print("Opening gripper")
        rtde_i_o.setToolDigitalOut(1,False)
        if(check_timeout(lambda: rtde_r.getDigitalInState(1),True)):
                return False
        rtde_i_o.setToolDigitalOut(0,True)
        if(check_timeout(lambda: rtde_r.getDigitalInState(1),False)):
                return False
        print("Gripper opened")
        return True

#Movimientos lineales a la posición cartesiana (x,y,z,rx,ry,rz) del robot usando cinematica inversa
def moveL(target,speed,acceleration):
        print(f"Moving in linear direction to target {target}")
        rtde_c.moveL(target,speed,acceleration)
        if(check_timeout(lambda: np.allclose(getActualTCPPose(),target,atol=1e-3),False)):
                return False
        print("Target achieved") 
        return True

#Movimientos lineales dando como parametros las posiciones articulares del robot usando cinematica inversa
def moveL_FK(target_q,speed,acceleration):
        print(f"Moving in linear direction to target {target_q}")
        rtde_c.moveL(target_q,speed,acceleration)
        if(check_timeout(lambda: np.allclose(getActualTCPPose(),target_q,atol=1e-3),False)):
                return False
        print("Target achieved")
        return True


# Muevo el robot a la posicion cartesiana (x,y,z,rx,ry,rz). La libreria calcula la cinemática inversa y manda moveJ al robot
def moveJ_IK(target,speed,acceleration):
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


# Muevo el robot a la posicion articular dando como entrada las posiciones articulares
def moveJ(target_q,speed,acceleration):
        print(f"Moving joints to target {target_q}")
        rtde_c.moveJ(target_q,speed,acceleration)
        if(check_timeout(lambda: np.allclose(getActualTCPPose(),target_q,atol=1e-3),False)):
                return False
        print("Target achieved")
        return True

#Obtengo las posicion actual de las articulaciones del robot (para usar moveJ)
def getActualJointPosition():
        jointPositions=rtde_r.getActualQ()
        print(f"Actual joint positions: {jointPositions}")
        return jointPositions

#Obtengo las coordenadas de la herramienta (x,y,z,rx,ry,rz)
def getActualTCPPose():
        TCPPose=rtde_r.getActualTCPPose()
        print(f"Actual Position of the tool: {TCPPose}")
        return TCPPose

#Desciendo el robot de forma lineal para coger/dejar la lata
def descendRobotZ(z,speed,acceleration):
        target=getActualTCPPose()
        target[2]-=z
        print(f"Descending robot {z} meters in z")
        moveL(target,speed,acceleration)
        if(check_timeout(lambda: np.allclose(getActualTCPPose(),target,atol=1e-3),False)):
                return False      
        print(f"Target reached")
        return True              
        
#Asciendo el robot de forma lineal despues de coger/dejar la lata
def ascendRobotZ(z,speed,acceleration):
        target=getActualTCPPose()
        target[2]+=z
        print(f"Ascending robot {z} meters in z")
        moveL(target,speed,acceleration)
        if(check_timeout(lambda: np.allclose(getActualTCPPose(),target,atol=1e-3),False)):
                return False      
        print(f"Target reached")
        return True              
        
#Permite establecer la nueva posición del TCP al usar una pinza más larga introduciendo cuanto mas larga es esta pinza
def setTcp(z_offset):
        rtde_c.setTCP(z_offset)
        new_tpcPose=rtde_c.getTCPOffset()
        if(check_timeout(lambda: z_offset==new_tpcPose,False)):
                return False
        
        print(f"Offset updated to {z_offset}")
        return True

def main():
        speed=0.2
        acceleration=0.2
        z=0.5
        target_home=[0.064,0.472,0.086,0.477,-3.25,-0.012] # en articulares
        target_waiting=[0.064,0.472,0.086,0.477,-3.25,-0.012] # en articulares
        target_place=[0.064,0.472,0.086,0.477,-3.25,-0.012] # en cartesianas



        #Conectamos el robot
        rtde_c = rtde_control.RTDEControlInterface("169.254.12.28")
        rtde_r = rtde_receive.RTDEReceiveInterface("169.254.12.28")
        rtde_i_o = rtde_io.RTDEIOInterface("169.254.12.28")

        bOk=RobotConexion()
        if(bOk):
                bOk=setTcp(0.5)
        if(bOk):
                bOk=moveJ(target_waiting)
        if(bOk):
                target_pick=GetRobotCoord # en cartesianas (x,y,z)
                target_pick.extend([0.477,-3.25,-0.012]) #añado rx,ry,rz siempre las mismas
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
        

        #Hago setTCP para poner el TCP correcto
        # Uso moveJ para ir a target target_waiting
        # Leo las coordenadas de la lata usando getRobotCoord()
        # Uso moveJ_IK para ir a las coordenadas de la lata (con z mayor)
        # hago un descendRobotZ
        # Hago CloseGrip
        # Hago ascendRobotZ
        # Uso moveJ para ir a la zona de la bandeja
        # Uso moveL para bajar en z
        # Hago OpenGrip
        # asciendo en z
        # vuelvo a home con moveJ




if __name__ == "__main__":
    main()


