import airsim
import random
import time
import threading

client = airsim.MultirotorClient()
client.confirmConnection()


drone = client.listVehicles()[0]

client.enableApiControl(True, drone)
client.armDisarm(True, drone)

drone.setVelocityControllerGains()
