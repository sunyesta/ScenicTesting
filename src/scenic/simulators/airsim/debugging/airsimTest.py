import airsim

client = airsim.VehicleClient()
client.confirmConnection()
client.simPause(True)


vehicle_name = "Drone2"
pose = airsim.Pose(airsim.Vector3r(0, 0, -5),
                   airsim.to_quaternion(0, 0, 0))
client.simAddVehicle(vehicle_name, "simpleflight", pose)
