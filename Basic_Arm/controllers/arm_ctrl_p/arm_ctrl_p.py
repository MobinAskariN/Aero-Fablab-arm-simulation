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

#homing
homing_done = False

# -----------------------------------------------------------------------------------------------------
# FUNCTION participants must complete
# -----------------------------------------------------------------------------------------------------
def arm_controller(sensor_values, image):
    """
    TODO: process image and implement arm control logic here.
    You are free to import classes, define new functions, and 
    modify the drm_controller function as you wish but the desired 
    format of the other parts of the program must stay exactly
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
    
    """
    
    print(sensor_values)
    
    if image is not None:

        # Show the image using OpenCV
        cv2.imshow("Camera Image", image)
        cv2.waitKey(1)  
        
    #Return MANUAL_speed of each joint  
    return {
        "waist": 0.0,
        "shoulder": 0.0,
        "elbow": 0.0,
        "wrist": 0.0,
        "pitch": 0.0,
        "claw": 0.0
    }

# -----------------------------------------------------------------------------------------------------
# Manual control for testing (DO NOT MODIFY!)
# -----------------------------------------------------------------------------------------------------
def keyboard_arm_controller(sensor_values, image):
    MANUAL_SPEED = 0.5  

    velocities = {
        "waist": 0.0,
        "shoulder": 0.0,
        "elbow": 0.0,
        "wrist": 0.0,
        "pitch": 0.0,
        "claw": 0.0
    }

    key = keyboard.getKey()
    
    print(sensor_values)
    
    if image is not None:

        cv2.imshow("Camera Image", image)
        cv2.waitKey(1)  
    
    if key == ord('Q'):
        velocities["waist"] = +MANUAL_SPEED
    elif key == ord('A'):
        velocities["waist"] = -MANUAL_SPEED

    elif key == ord('W'):
        velocities["shoulder"] = +MANUAL_SPEED
    elif key == ord('S'):
        velocities["shoulder"] = -MANUAL_SPEED

    elif key == ord('E'):
        velocities["elbow"] = +MANUAL_SPEED
    elif key == ord('D'):
        velocities["elbow"] = -MANUAL_SPEED

    elif key == ord('R'):
        velocities["wrist"] = +MANUAL_SPEED
    elif key == ord('F'):
        velocities["wrist"] = -MANUAL_SPEED

    elif key == ord('T'):
        velocities["pitch"] = +MANUAL_SPEED
    elif key == ord('G'):
        velocities["pitch"] = -MANUAL_SPEED

    elif key == ord('Y'):
        velocities["claw"] = +MANUAL_SPEED
    elif key == ord('H'):
        velocities["claw"] = -MANUAL_SPEED

    return velocities

# -----------------------------------------------------------------------------------------------------
# Move arm to initial pose
# -----------------------------------------------------------------------------------------------------
def move_arm_to_initial(sensor_values,
                         targets=None,
                         kp=1.5,
                         tolerance=0.01,
                         max_speed=0.6):


    if targets is None:
        targets = {
            "waist": 0.0,
            "shoulder": 0.0,
            "elbow": 0.0,
            "wrist": 0.0,
            "pitch": 0.0,
            "claw": 0.0
        }

    velocities = {}

    for joint, target in targets.items():

        sensor_key = "fingers" if joint == "claw" else joint
        current = sensor_values[sensor_key]
        error = target - current

        if abs(error) < tolerance:
            velocities[joint] = 0.0
        else:
            vel = kp * error

            vel = max(min(vel, max_speed), -max_speed)
            velocities[joint] = vel

    return velocities

# -----------------------------------------------------------------------------------------------------
# MAIN LOOP (DO NOT MODIFY!)
# -----------------------------------------------------------------------------------------------------
while robot.step(timestep) != -1:
    
    sensor_values = {name: s.getValue() for name, s in sensors.items()}

    for name, s in sensor_values.items():
        if abs(s) < 0.0001:
            sensor_values[name] = 0.0
        else:
            sensor_values[name] = round(s, 3)
    image = camera.getImage()
    
    if image is not None:
        width = camera.getWidth()
        height = camera.getHeight()
        
        img_data = np.frombuffer(image, dtype=np.uint8)
        img_data = img_data.reshape((height, width, 4))
        
        bgr_image = img_data[:, :, :3]

    # homing
    if not homing_done:
        velocities = move_arm_to_initial(sensor_values)

        if all(abs(v) < 1e-3 for v in velocities.values()):
            homing_done = True
            print("Homing completed.")
    else:
   
        # call the controller
        # velocities = arm_controller(sensor_values, bgr_image)

        # manuall controller
        velocities = keyboard_arm_controller(sensor_values, bgr_image)

    for joint, vel in velocities.items():
        motors[joint].setVelocity(vel)

cv2.destroyAllWindows()
