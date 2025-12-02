from controller import Robot
import math

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
camera.enable(timestep*2)


# -----------------------------------------------------------------------------------------------------
# FUNCTION participents must complete
# -----------------------------------------------------------------------------------------------------
def arm_controller(sensor_values, image):
    """
    sensor_values = dict containing all sensor readings
    image = camera image or None
    Webots provides the camera frame as a raw BGRA byte buffer (no NumPy/OpenCV format).
    To process it with OpenCV, reshape it into (H, W, 4) and remove the alpha channel → BGR image.


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

    # TODO: participents implement logic here
    # example: return all zeros
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
