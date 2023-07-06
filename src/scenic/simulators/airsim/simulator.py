
from cmath import atan, pi, tan
import math
from math import sin, radians, degrees, copysign
import os
import pathlib
import time

import airsim
import numpy as np

from scenic.core.simulators import Simulator, Simulation


class AirSimSimulator(Simulator):
    def __init__(self, timestep=1):
        pass

    def createSimulation(self, scene):
        return AirSimSimulation()


class AirSimSimulation(Simulation):
    def __init__(self, scene, network, timestep, verbosity=0, *, headless=False):
        super().__init__(scene, timestep=timestep, verbosity=verbosity)

        # init airsim
        client = airsim.MultirotorClient()
        client.confirmConnection()
        client.enableApiControl(True)
        client.simPause(True)

        # ------- init enviornment

        for obj in self.objects:
            self.createObjectInSimulator(obj)

        # ------- start airsim simulation
        client.armDisarm(True)  # start drone
        client.takeoffAsync().join()  # make drone take off

        pass

    # ------------------- Required Methods -------------------

    def createObjectInSimulator(self, obj):
        # no coordinate recalculating is needed: All AirSim API uses NED coordinate system, i.e., +X is North, +Y is East and +Z is Down


        # spawn objects
        self.client.simSpawnObject(object_name, asset_name, pose, scale, physics_enabled=False, is_blueprint=False)

        pass

    def step(self):
        # step 1 frame
        self.client.simContinueForFrames(1)
        pass

    def getProperties(self, obj, properties):
        # get object properties (not sure if neccessary since objects don't move)
        pose = self.client.simGetObjectPose()
        
        
        # get drone properties
        pose = self.client.simGetVehiclePose()
        pitch, roll, yaw = airsim.to_eularian_angles(pose.orientation)
        position = pose.position
        pass

    # ------------------- Utils -------------------

    def setProperties(self, obj, properties):
        # set drone position and rotation
        self.client.simSetVehiclePose(airsim.Pose(airsim.Vector3r(
            0, 0, 0), airsim.to_quaternion(0, 0, 0)), False)  # ignore collision set to false

        # pose can also be directly manipulated
        pose = self.client.simGetVehiclePose()
        pose.position = pose.position + airsim.Vector3r(0.03, 0, 0)
