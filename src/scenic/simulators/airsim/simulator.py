
from cmath import atan, pi, tan
import math
from math import sin, radians, degrees, copysign
import os
import pathlib
import time
import random
import subprocess

import airsim
import numpy as np

from scenic.core.simulators import Simulator, Simulation


class AirSimSimulator(Simulator):
    def __init__(self, map_path, timestep=0.1):

        # run airsim
        exepath = r"C:\Users\Mary\Documents\Code\Scenic\AirSimBinaries\Blocks\WindowsNoEditor\Blocks.exe"
        arguments = '-settings="C:\Users\Mary\Documents\Code\Scenic\ScenicTesting\src\scenic\simulators\airsim\airsimSettings.json"'
        command = f'start {exepath} {arguments}'
        subprocess.run(command, shell=True)

        # initializing airsim
        client = airsim.VehicleClient()
        client.confirmConnection()
        client.simPause(True)
        self.client = client

    def createSimulation(self, scene, **kwargs):
        return AirSimSimulation(self, scene, self.client, **kwargs)

    def destroy(self):
        super().destroy()

        # close simulator
        self.client.armDisarm(False)
        self.client.enableApiControl(False)


class AirSimSimulation(Simulation):

    # ------------------- Required Methods -------------------

    def __init__(self, scene, client, **kwargs):
        self.client = client

        super().__init__(scene, **kwargs)

    def setup(self):
        # Create objects.
        super().setup()

    def createObjectInSimulator(self, obj):
        # * if we want custom meshes, you need to precompile a binary that includes those meshes: https://www.youtube.com/watch?v=Bp86WiLUC80&ab_channel=AhmedElsaharti

        # TODO ensure object name is unique
        if not obj.displayName:
            obj.displayName = str(obj)

        # no coordinate recalculating is needed: All AirSim API uses NED coordinate system, i.e., +X is North, +Y is East and +Z is Down
        pose = airsim.Pose(position_val=tupleToVector3r(scenicToAirsimSpace(
            obj.position)), orientation_val=obj.rotation)  # todo transfer to quaternion

        if obj.type == "Drone":

            self.client.simAddVehicle(
                object_name=obj.displayName, vehicle_type="simpleflight", pose=pose)
        else:
            obj_name = self.client.simSpawnObject(object_name=obj.displayName, asset_name=obj.asset_name,
                                                  pose=pose, scale=obj.scale, physics_enabled=obj.physEnabled, is_blueprint=False)

        print(f"Created object {obj_name} from asset {obj.asset_name} "
              f"at pose {pose}, scale {obj.scale}")

    def step(self):
        # step 1 frame
        self.client.simContinueForTime(self.timestep)
        pass

    # ------------------- Other Simulator methods -------------------

    def destroy(self):
        # * made more general
        # destroy all sim objects
        for obj_name in self.client.simListSceneObjects():
            self.client.simDestroyObject(obj_name)

        self.client.reset()

        super().destroy()

    def getProperties(self, obj, properties):
        # get object properties (not sure if neccessary since objects don't move)
        pose = self.client.simGetObjectPose(obj.displayName)

        # todo use built in obj.parentOrientation.localAnglesFor(globalOrientation)
        pitch, roll, yaw = airsim.to_eularian_angles(pose.orientation)
        position = airsimToScenicSpace(pose.position)

        # TODO fix properties in dict
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


# -------------- Static helper functions --------------

def tupleToVector3r(tuple):
    return airsim.Vector3r(tuple[0], tuple[1], tuple[2])


def scenicToAirsimSpace(tuple):
    return (tuple[0], tuple[2], tuple[1])


def airsimToScenicSpace(tuple):
    return (tuple[0], tuple[2], tuple[1])
