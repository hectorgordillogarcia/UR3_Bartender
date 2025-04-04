
import rtde_control
import rtde_receive
import rtde_io
import time

rtde_c = rtde_control.RTDEControlInterface("169.254.12.28")
rtde_r = rtde_receive.RTDEReceiveInterface("169.254.12.28")
rtde_i_o = rtde_io.RTDEIOInterface("169.254.12.28")



target_begin=[-0.0177,0.495,0.270,3.16,-1.77,-0.031]
rtde_c.moveJ_IK(target_begin, 0.2, 0.2)

#Ensure that digital output is set to 0
rtde_i_o.setToolDigitalOut(1,False)
time.sleep(0.1)

#Close
rtde_i_o.setToolDigitalOut(1,True)
time.sleep(0.5)

target_end=[-0.0177,0.495,0.5,3.16,-1.77,-0.031]
rtde_c.moveJ_IK(target_end, 0.2, 0.2)

#Open
rtde_i_o.setToolDigitalOut(1,False)
time.sleep(0.5)

#Wait 1 second to ensure that the gripper is opened
