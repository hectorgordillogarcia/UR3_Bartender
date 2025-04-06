
import rtde_control
import rtde_receive
import rtde_io
import time

rtde_c = rtde_control.RTDEControlInterface("169.254.12.28")
rtde_r = rtde_receive.RTDEReceiveInterface("169.254.12.28")
rtde_i_o = rtde_io.RTDEIOInterface("169.254.12.28")
bOk=False; 

target_situate=[0.064,0.472,0.086,0.477,-3.25,-0.012]
target_Aproximate=[0.107,0.387,0.105,0.025,3.13,-0.068]

print("target_Aproximate:", target_Aproximate)  # Z aumentado en 0.15


# if rtde_c.getInverseKinematicsHasSolution(target_begin):
#     rtde_c.moveJ_IK(target_begin, 0.2, 0.2)
#     time.sleep(1)

if rtde_c.getInverseKinematicsHasSolution(target_Aproximate):
        rtde_c.moveJ_IK(target_Aproximate, 0.2, 0.2)
        time.sleep(0.5)

target_Pick=rtde_r.getActualTCPPose()
target_Pick[2]-=0.5

rtde_c.moveL(target_Pick,0.2,0.2)
time.sleep(0.5)

# target_Pick=rtde_r.getActualTCPPose()
# target_Pick[2] += 0.10

#rtde_c.moveJ_IK(target_Aproximate, 0.2, 0.2)
#time.sleep(0.5)

#rtde_c.moveJ_IK(target_Pick, 0.2, 0.2)

#rtde_c.moveL(target_Pick,0.2,0.2)
#time.sleep(0.5)

#Ensure that digital output is set to 0
#rtde_i_o.setToolDigitalOut(0,False)
#time.sleep(0.1)

#Close
rtde_i_o.setToolDigitalOut(0,False)
rtde_i_o.setToolDigitalOut(1,True)

time.sleep(1)

target_end=[-0.0177,0.495,0.5,3.16,-1.77,-0.031]
# rtde_c.moveJ_IK(target_end, 0.2, 0.2)

#Open
rtde_i_o.setToolDigitalOut(1,False)
rtde_i_o.setToolDigitalOut(0,True)

time.sleep(1)

#Wait 1 second to ensure that the gripper is opened
