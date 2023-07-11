
from cmath import atan, pi, tan
import math
from math import sin, radians, degrees, copysign
import os
import pathlib
import time
import random

import airsim
import numpy as np

from scenic.core.simulators import Simulator, Simulation


class AirSimSimulator(Simulator):
    def __init__(self):

        # initializing airsim
        client = airsim.MultirotorClient()
        client.confirmConnection()

        client.simPause(True)
        self.client = client

    def createSimulation(self, scene, *, timestep=1, **kwargs):

        return AirSimSimulation(self, scene, self.client, timestep, **kwargs)

    def destroy(self):
        super().destroy()

        # close simulator
        self.client.armDisarm(False)
        self.client.enableApiControl(False)


class AirSimSimulation(Simulation):

    # ------------------- Required Methods -------------------

    def __init__(self, scene, client, timestep, **kwargs):
        self.client = client
        self.timestep = timestep

        super().__init__(scene, **kwargs)

    def setup(self):
        # start airsim simulation
        self.client.enableApiControl(True)
        self.client.armDisarm(True)  # start drone
        self.client.takeoffAsync().join()  # make drone take off

        # Create objects.
        super().setup()

    def createObjectInSimulator(self, obj):

        self.createObject(obj.asset_name, pos=obj.pos, rot=obj.rot,
                          scale=obj.scale, display_name=obj.name)

    def step(self):
        # step 1 frame
        self.client.simContinueForTime(self.timestep)
        pass

    # ------------------- Other Simulator methods -------------------

    def executeActions(self, allActions):
        super().executeActions(allActions)
        # TODO: implement
        #! need explanation

    def destroy(self):

        # destroy all sim objects
        for obj_name in self.client.simListSceneObjects():
            self.client.simDestroyObject(obj_name)

        self.client.reset()

        super().destroy()

    def getProperties(self, obj, properties):

        if obj.rolename == "drone":
            # get drone properties
            pose = self.client.simGetVehiclePose()
        else:

            # get object properties (not sure if neccessary since objects don't move)
            pose = self.client.simGetObjectPose()

        pitch, roll, yaw = airsim.to_eularian_angles(pose.orientation)
        position = pose.position

        values = dict(position=position, eulerXYZ=(pitch, roll, yaw))
        return values

    # ------------------- Utils -------------------

    def setProperties(self, obj, properties):
        # set drone position and rotation
        self.client.simSetVehiclePose(airsim.Pose(airsim.Vector3r(
            0, 0, 0), airsim.to_quaternion(0, 0, 0)), False)  # ignore collision set to false

        # pose can also be directly manipulated
        pose = self.client.simGetVehiclePose()
        pose.position = pose.position + airsim.Vector3r(0.03, 0, 0)

    def createObject(self, asset_name, *, pos, rot, scale=(1.0, 1.0, 1.0), display_name):
        """Spawns an airsim asset into the simulator

        Args:
            asset_name (string): airsim asset name for identifying the asset you want to spawn in
            pos (tuple): position of the object
            rot (tuple): eulerXYZ rotation of the object
            displayName (string): desired object name
            scale (tuple, optional): _description_. Defaults to (1.0, 1.0, 1.0).
        """
        if not displayName:
            displayName = f"{asset_name}_spawn_{random.randint(0, 100)}"

        # no coordinate recalculating is needed: All AirSim API uses NED coordinate system, i.e., +X is North, +Y is East and +Z is Down
        pose = airsim.Pose(position_val=tupleToVector3r(
            pos), orientation_val=airsim.to_eularian_angles(pose.orientation))

        obj_name = self.client.simSpawnObject(object_name=displayName, asset_name=asset_name,
                                              pose=pose, scale=scale, physics_enabled=False, is_blueprint=False)

        print(f"Created object {obj_name} from asset {asset_name} "
              f"at pose {pose}, scale {scale}")


# -------------- Static helper functions --------------

def tupleToVector3r(tuple):
    return airsim.Vector3r(tuple[0], tuple[1], tuple[2])
