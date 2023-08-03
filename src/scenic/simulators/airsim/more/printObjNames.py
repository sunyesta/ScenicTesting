import airsim

client = airsim.VehicleClient()
client.confirmConnection()
client.simPause(True)

print(client.simListSceneObjects())