# UR3 Bartender Project

## Description
This project implements an automated bartender system using a UR3 robot. The robot can recognize and select soda cans based on customer choices, placing them on a tray using a pick & place operation. Additionally, the system includes functionality to detect and reposition fallen cans.

## Key Features
- **Can Selection**: Customers can choose between different types of sodas (Coca-Cola, Fanta Orange, Fanta Lemon).
- **Can Recognition with YOLO**: YOLO vision technology is used for real-time can detection and classification.
- **Pick & Place Operation**: The robot picks up the selected cans and places them on a serving tray.
- **Fallen Can Correction**: If a can is not in the correct position, the robot detects and repositions it properly.

## Technologies Used
- **UR3 Robot** for can manipulation and movement.
- **YOLO (You Only Look Once)** for real-time detection and classification of soda cans.
- **Python and OpenCV** for image processing and system control.
- **URx Library** for direct communication with the UR3 robot via Ethernet.

## Usage
1. Select the desired soda from the interface.
2. The robot detects and picks up the corresponding can.
3. The can is placed on the tray.
4. If any cans are fallen, the system will automatically correct their position.
