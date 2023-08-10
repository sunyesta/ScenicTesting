import airsim

client = airsim.MultirotorClient()
client.confirmConnection()
client.simPause(False)


drone = client.listVehicles()[0]
client.enableApiControl(True, drone)
print(drone)

client.armDisarm(True, drone)
client.takeoffAsync(vehicle_name=drone).join()
print("took off")

pose = airsim.Pose(airsim.Vector3r(0, 0, -10), airsim.to_quaternion(0, 0, 0))

print(client.simGetVehiclePose(drone))


# client.moveToPositionAsync(
#     pose.position.x_val,
#     pose.position.y_val,
#     pose.position.z_val,
#     velocity=5,
#     vehicle_name=drone,
# )

# self.client.armDisarm(True, drone)
client.simSetVehiclePose(vehicle_name=drone, pose=pose, ignore_collision=True)


client.moveToPositionAsync(
    10,
    10,
    -10,
    5,
    vehicle_name=drone,
).join()
print("finished")
