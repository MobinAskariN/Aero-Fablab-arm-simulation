from controller import Robot
import math
import time
import numpy as np
import cv2  # For displaying the image

robot = Robot()
timestep = int(robot.getBasicTimeStep())

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

# -----------------------------------------------------------------------------------------------------
# FUNCTION participants must complete
# -----------------------------------------------------------------------------------------------------
def arm_controller(sensor_values, image):
    """
    sensor_values = dict containing all sensor readings

    Should return a dict:
    {
        "waist": vel,
        "shoulder": vel,
        "elbow": vel,
        "wrist": vel,
        "pitch": vel,
        "claw": vel
    }
    """

    # TODO: process image and implement arm control logic here
    print(sensor_values)
    
    if image is not None:
        width = camera.getWidth()
        height = camera.getHeight()
        
        # Convert image to a numpy array (BGRA format)
        img_data = np.frombuffer(image, dtype=np.uint8)
        img_data = img_data.reshape((height, width, 4))  # Reshape to (height, width, 4)
        
        # Convert BGRA to BGR by removing the alpha channel (last channel)
        bgr_image = img_data[:, :, :3]

        # Show the image using OpenCV
        cv2.imshow("Camera Image", bgr_image)
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

# -----------------------------------------------------------------------------------------------------
# MAIN LOOP
# -----------------------------------------------------------------------------------------------------
while robot.step(timestep) != -1:

    # read all sensors
    sensor_values = {name: s.getValue() for name, s in sensors.items()}

    # get camera frame (if needed)
    image = camera.getImage()

    # call the controller
    velocities = arm_controller(sensor_values, image)

    # set returned velocities to motors
    for joint, vel in velocities.items():
        motors[joint].setVelocity(vel)

# Close all OpenCV windows when the simulation ends
cv2.destroyAllWindows()
