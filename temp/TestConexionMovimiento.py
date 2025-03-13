import rtde_control
rtde_c = rtde_control.RTDEControlInterface("127.0.0.1")
rtde_c.moveL([-0.143, -0.435, 0.20, -0.001, 3.12, 0.04], 0.5, 0.3)