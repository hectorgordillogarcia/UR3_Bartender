
import rtde_control
import rtde_receive
import rtde_io
import time

rtde_c = rtde_control.RTDEControlInterface("169.254.12.28")
rtde_r = rtde_receive.RTDEReceiveInterface("169.254.12.28")
rtde_i_o = rtde_io.RTDEIOInterface("169.254.12.28")
bOk=False; 


#Posicion generica encima de las latas
target_situate=[0.064,0.472,0.086,0.477,-3.25,-0.012]
if rtde_c.getInverseKinematicsHasSolution(target_situate):
        rtde_c.moveJ_IK(target_situate, 0.2, 0.2)
        time.sleep(0.5)

# David me pasará las coordenadas del robot
# 
Coord_Camera=[0.107,0.387,0.105]


target_Aprox= [Coord_Camera[0],Coord_Camera[1],Coord_Camera[2],0.025,3.13,-0.068]
target_Aprox[2]+=0.5



if rtde_c.getInverseKinematicsHasSolution(target_Aprox):
        rtde_c.moveJ_IK(target_Aprox, 0.2, 0.2)
        time.sleep(0.5)

target_Pick=rtde_r.getActualTCPPose()
target_Pick[2]-=0.5

rtde_c.moveL(target_Pick,0.2,0.2)
time.sleep(0.5)

#Close
rtde_i_o.setToolDigitalOut(0,False)
rtde_i_o.setToolDigitalOut(1,True)

time.sleep(1)

target_Lift=rtde_r.getActualTCPPose()
target_Lift[2]+=0.5

rtde_c.moveL(target_Lift,0.2,0.2)
time.sleep(0.5)

target_waypoint=[-0.0177,0.495,0.5,3.16,-1.77,-0.031]
if rtde_c.getInverseKinematicsHasSolution(target_waypoint):
        rtde_c.moveJ_IK(target_waypoint, 0.2, 0.2)
        time.sleep(0.5)



target_situate2=[0.064,0.472,0.086,0.477,-3.25,-0.012]
if rtde_c.getInverseKinematicsHasSolution(target_situate2):
        rtde_c.moveJ_IK(target_situate2, 0.2, 0.2)
        time.sleep(0.5)

target_end=[-0.0177,0.495,0.5,3.16,-1.77,-0.031]

target_approx = target_end.copy()
target_approx[2] += 0.5

if rtde_c.getInverseKinematicsHasSolution(target_approx):
        rtde_c.moveJ_IK(target_approx, 0.2, 0.2)
        time.sleep(0.5)
        
target_end=rtde_r.getActualTCPPose()
target_end[2]-=0.5

rtde_c.moveL(target_end,0.2,0.2)
time.sleep(0.5)

#Open
rtde_i_o.setToolDigitalOut(1,False)
rtde_i_o.setToolDigitalOut(0,True)
time.sleep(1)



