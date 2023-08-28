import airsim
import random
import time


def scenicToAirsimRotation(orientation):
    pitch, yaw, roll = orientation.r.as_euler("XZY", degrees=True)
    return airsim.to_quaternion(pitch, roll, yaw)


client = airsim.MultirotorClient()
client.confirmConnection()

upAngle = 3.14159 / 2

drone = client.listVehicles()[0]
client.enableApiControl(True, drone)
client.armDisarm(True, drone)
print(drone)

newPose = airsim.Pose(
    position_val=airsim.Vector3r(0, 0, -1),
    orientation_val=airsim.to_quaternion(0, 0, upAngle),
)


client.simPause(False)
client.simSetVehiclePose(newPose, True, drone)
time.sleep(0.1)
# client.simPause(True)
