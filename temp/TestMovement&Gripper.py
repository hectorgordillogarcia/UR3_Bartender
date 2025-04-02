
import rtde_control
import rtde_receive
import time

rtde_c = rtde_control.RTDEControlInterface("169.254.12.28")
rtde_r = rtde_receive.RTDEReceiveInterface("169.254.12.28")


target_begin=[-0.0177,0.495,0.270,3.16,-1.77,-0.031]
rtde_c.moveJ_IK(target_begin, 0.2, 0.2)

# Pins used in ros2 configuration
pin_close = 17  
pin_open = 16 

#Close
rtde_c.setStandardDigitalOut(pin_open, 0)
rtde_c.setStandardDigitalOut(pin_close, 1)

#Wait 1 second to ensure that the gripper is closed
time.sleep(1)

target_end=[-0.0177,0.495,0.5,3.16,-1.77,-0.031]
rtde_c.moveJ_IK(target_end, 0.2, 0.2)

#Open
rtde_c.setStandardDigitalOut(pin_open, 1)
rtde_c.setStandardDigitalOut(pin_close, 0)


#Wait 1 second to ensure that the gripper is opened
time.sleep(1)