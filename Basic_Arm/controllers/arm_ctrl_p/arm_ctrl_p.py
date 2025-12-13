from controller import Robot
import math
import numpy as np
import cv2  
import random
from controller import Keyboard



# -----------------------------------------------------------------------------------------------------
# INITIALIZATION (DO NOT MODIFY!)
# -----------------------------------------------------------------------------------------------------
robot = Robot()
timestep = int(robot.getBasicTimeStep())

keyboard = Keyboard()
keyboard.enable(timestep)


# Initialize Motors
motors = {
    "waist": robot.getDevice('waist_motor'),
    "shoulder": robot.getDevice('shoulder_motor'),
    "elbow": robot.getDevice('elbow_motor'),
    "wrist": robot.getDevice('wrist_motor'),
    "pitch": robot.getDevice('pitch_motor'),
    "claw": robot.getDevice('phalanx_motor::right')
}

# # ---------------- INITIAL POSITION OF JOINTS ----------------
# initial_positions = {
#     "waist": 1.08,
#     "shoulder": 0.16,
#     "elbow": 0.06,
#     "wrist": 0.0,
#     "pitch": -0.46,
#     "claw": 0.0
# }

# # Set initial positions
# for joint, pos in initial_positions.items():
#     motors[joint].setPosition(pos)
#     motors[joint].setVelocity(1.0)

# # Let the robot reach initial pose
# for _ in range(60):     # ~2 seconds
#     robot.step(timestep)

for m in motors.values():
    m.setPosition(float('inf'))
    m.setVelocity(0)

# Initialize Sensors
sensors = {
    "waist": robot.getDevice('waist_sensor'),
    "shoulder": robot.getDevice('shoulder_sensor'),
    "elbow": robot.getDevice('elbow_sensor'),
    "wrist": robot.getDevice('wrist_sensor'),
    "pitch": robot.getDevice('pitch_sensor'),
    "fingers": robot.getDevice('phalanx_sensor'),
    "finger_switch": robot.getDevice('finger_sensor')
}

for s in sensors.values():
    s.enable(timestep)

# Camera
camera = robot.getDevice('camera')
camera.enable(timestep * 2)

# Order of placement
order = random.randint(1,6)

# -----------------------------------------------------------------------------------------------------
# FUNCTION participants must complete
# -----------------------------------------------------------------------------------------------------
def arm_controller(sensor_values, image, order):
    """
    TODO: process image and implement arm control logic here.
    You are free to import classes, define new functions, and 
    modify the code as you wish but the desired format must stay
    the same; meaning after any process, you should return this dict
    at the end of current function:
    {
        "waist": vel,
        "shoulder": vel,
        "elbow": vel,
        "wrist": vel,
        "pitch": vel,
        "claw": vel
    }
    
    You should place the boxes on the matching surface in respect to value of 'order':
    1 : blue, green, black
    2 : blue, black, green
    3 : green, blue, black
    4 : green, black, blue
    5 : black, blue, green
    6 : black, green, blue
    """
    
    if image is not None:
        # Show the image using OpenCV
        cv2.imshow("Camera Image", image)
        cv2.waitKey(1)  
        
    #Return speed of each joint  
    return {
        "waist": 0.0,
        "shoulder": 0.0,
        "elbow": 0.0,
        "wrist": 0.0,
        "pitch": 0.0,
        "claw": 0.0
    }

def keyboard_arm_controller():
    SPEED = 0.5  # rad/s

    velocities = {
        "waist": 0.0,
        "shoulder": 0.0,
        "elbow": 0.0,
        "wrist": 0.0,
        "pitch": 0.0,
        "claw": 0.0
    }

    key = keyboard.getKey()
    print(key)

    if key == ord('Q'):
        velocities["waist"] = +SPEED
    elif key == ord('A'):
        velocities["waist"] = -SPEED

    elif key == ord('W'):
        velocities["shoulder"] = +SPEED
    elif key == ord('S'):
        velocities["shoulder"] = -SPEED

    elif key == ord('E'):
        velocities["elbow"] = +SPEED
    elif key == ord('D'):
        velocities["elbow"] = -SPEED

    elif key == ord('R'):
        velocities["wrist"] = +SPEED
    elif key == ord('F'):
        velocities["wrist"] = -SPEED

    elif key == ord('T'):
        velocities["pitch"] = +SPEED
    elif key == ord('G'):
        velocities["pitch"] = -SPEED

    elif key == ord('Y'):
        velocities["claw"] = +SPEED
    elif key == ord('H'):
        velocities["claw"] = -SPEED

    return velocities

# -----------------------------------------------------------------------------------------------------
# MAIN LOOP (DO NOT MODIFY!)
# -----------------------------------------------------------------------------------------------------
while robot.step(timestep) != -1:
    
    # read all sensors
    sensor_values = {name: s.getValue() for name, s in sensors.items()}

    # get camera frame (if needed)
    image = camera.getImage()
    
    print(sensor_values)
    print('order: ', order)
    if image is not None:
        width = camera.getWidth()
        height = camera.getHeight()
        
        # Convert image to a numpy array (BGRA format)
        img_data = np.frombuffer(image, dtype=np.uint8)
        img_data = img_data.reshape((height, width, 4))  # Reshape to (height, width, 4)
        
        # Convert BGRA to BGR by removing the alpha channel (last channel)
        bgr_image = img_data[:, :, :3]

    
    # # call the controller
    # velocities = arm_controller(sensor_values, bgr_image, order)
    # manuall controller
    velocities = keyboard_arm_controller()



    # set returned velocities to motors
    for joint, vel in velocities.items():
        motors[joint].setVelocity(vel)

cv2.destroyAllWindows()
