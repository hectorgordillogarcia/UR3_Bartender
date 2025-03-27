
import rtde_control
import rtde_receive
import pyRobotiqGripper
import time

rtde_c = rtde_control.RTDEControlInterface("169.254.12.28")
rtde_r = rtde_receive.RTDEReceiveInterface("169.254.12.28")

gripper = pyRobotiqGripper.RobotiqGripper('/dev/ttyUSB0')

# # target=[-0.0177,0.495,0.270,3.16,-1.77,-0.031]
# # rtde_c.moveJ_IK(target, 0.2, 0.2)

# # rtde_c.sendScript("rq_close()")  # Cerrar gripper

# # Esperar 1 segundo y luego abrir
# # time.sleep(2)

# # rtde_c.sendScript("rq_open()")  # Abrir gripper

# gripper.activate()  # returns to previous position after activation
# gripper.set_force(50)  # from 0 to 100 %
# gripper.set_speed(100)  # from 0 to 100 %

# # Perform some gripper actions
gripper.open()
time.sleep(2)
gripper.close()
print(dir(pyRobotiqGripper))
