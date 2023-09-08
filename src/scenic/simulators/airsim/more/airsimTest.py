import airsim
import random
import time
import threading


def scenicToAirsimRotation(orientation):
    pitch, yaw, roll = orientation.r.as_euler("XZY", degrees=True)
    return airsim.to_quaternion(pitch, roll, yaw)


def startWait(future):
    def joinAsync():
        future.join()

    threading.Thread(target=joinAsync).start()

    return future


client = airsim.MultirotorClient()
client.confirmConnection()
client.simAddVehicle(
    vehicle_name="drone2",
    vehicle_type="simpleflight",
    pose=airsim.Pose(
        position_val=airsim.Vector3r(0, 0, -5),
    ),
)

drone = client.listVehicles()[0]
drone2 = client.listVehicles()[1]


client.enableApiControl(True, drone)
client.armDisarm(True, drone)
print(drone)


client.simSetVehiclePose(
    airsim.Pose(
        position_val=airsim.Vector3r(0, 0, -5),
    ),
    True,
    drone,
)
client.simSetVehiclePose(
    airsim.Pose(
        position_val=airsim.Vector3r(5, 5, -5),
    ),
    True,
    drone2,
)

client.moveByVelocityAsync(0, 0, 0, 1, vehicle_name=drone)
client.moveByVelocityAsync(0, 0, 0, 1, vehicle_name=drone2)


client.moveToPositionAsync(
    0,
    0,
    0,
    5,
    vehicle_name=drone,
)
client.moveToPositionAsync(
    0,
    0,
    0,
    5,
    vehicle_name=drone2,
)


client.simPause(False)

time.sleep(0.1)
# client.simPause(True)
