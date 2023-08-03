from cmath import atan, pi, tan
import math
from math import sin, radians, degrees, copysign
import os
import pathlib
import time
import random
import subprocess
import scipy
from scenic.core.vectors import Orientation, Vector
import time

import airsim
import numpy as np

from scenic.core.simulators import (
    Simulator,
    Simulation,
    SimulationCreationError,
    SimulatorInterfaceWarning,
)

# todo by next meeting


class AirSimSimulator(Simulator):
    def __init__(self, map_path, timestep=0.1):
        print("dsafds")
        # initializing airsim

        try:
            client = airsim.MultirotorClient()
            client.confirmConnection()
            client.simPause(True)
        except:
            raise SimulatorInterfaceWarning(
                "Airsim must be running on before executing scenic"
            )

        self.client = client

        # # # delete all objects in simulation
        # for objName in client.simListSceneObjects():
        # print("flight name",objName)
        # client.simDestroyObject("SimpleFlight")
        # if "Ground" in objName:
        #     client.simDestroyObject(objName)

        super().__init__()

    def createSimulation(self, scene, **kwargs):
        return AirSimSimulation(self, scene, self.client, **kwargs)

    def destroy(self):
        super().destroy()

        # close simulator
        # todo


class AirSimSimulation(Simulation):
    # ------------------- Required Methods -------------------

    def __init__(self, simulator, scene, client, **kwargs):
        self.simulator = simulator
        self.client = client

        self.objs = {}

        # since we can't delete any drones, we need to keep track of which ones we are using and which ones we arent

        # todo put in setup method
        client.simPause(False)
        self.startDrones = client.listVehicles()
        print("vehicles: " + str(client.listVehicles()))
        for drone in self.startDrones:
            self.client.enableApiControl(True, drone)
            self.client.armDisarm(True, drone)  # todo make optional
            client.takeoffAsync(vehicle_name=drone)
        client.simPause(True)
        self.nextAvalibleDroneIndex = 0
        super().__init__(scene, **kwargs)

    def setup(self):
        # Create objects.
        super().setup()

    def createObjectInSimulator(self, obj):
        # ------ set default values ------
        if not obj.name:
            obj.name = str(hash(obj))

        # ensure obj isn't already in world
        if obj.name in self.objs:
            raise SimulationCreationError(
                "there is already an object of the name "
                + obj.name
                + "in the simulator"
            )

        realObjName = obj.name + str(hash(obj))

        # ------------

        pose = airsim.Pose(
            position_val=scenicToAirsimLocation(obj.position),
            orientation_val=scenicToAirsimRotation(obj.orientation),
        )

        if obj.blueprint == "Drone":
            # if there is an avalible drone, take it
            if self.nextAvalibleDroneIndex < len(self.startDrones):
                realObjName = self.startDrones[self.nextAvalibleDroneIndex]
                print("created type1: " + realObjName)
                self.nextAvalibleDroneIndex += 1

                self.objs[obj.name] = realObjName

                # set its pose
                self.client.simSetVehiclePose(
                    vehicle_name=realObjName, pose=pose, ignore_collision=True
                )

            else:
                print("created type2: " + realObjName)
                self.objs[obj.name] = realObjName
                self.client.simAddVehicle(
                    vehicle_name=realObjName, vehicle_type="simpleflight", pose=pose
                )
                self.client.hoverAsync(vehicle_name=realObjName)
                self.client.enableApiControl(True, realObjName)
                self.client.armDisarm(True, realObjName)
                self.client.takeoffAsync(vehicle_name=realObjName)
                self.client.simSetVehiclePose(
                    vehicle_name=realObjName, pose=pose, ignore_collision=True
                )

                # save our newly created drone

        else:
            print("created type3: " + realObjName)
            self.objs[obj.name] = realObjName
            self.client.simSpawnObject(
                object_name=realObjName,
                asset_name=obj.assetName,
                pose=pose,
                scale=scenicToAirsimScale(obj),
                physics_enabled=obj.physEnabled,
                is_blueprint=False,
            )

        # print(f"Created object {realObjName} from asset {obj.assetName} ")

    def step(self):
        # step 1 frame
        print(self.objs)
        self.client.simContinueForTime(self.timestep)
        pass

    # ------------------- Other Simulator methods -------------------

    def destroy(self):
        for obj_name in self.objs:
            self.client.simDestroyObject(obj_name)

        self.newObjs = {}

        super().destroy()

    def getProperties(self, obj, properties):
        # # get object properties (not sure if neccessary since objects don't move)
        objName = self.objs[obj.name]

        pose = None
        if obj.blueprint == "Drone":
            pose = self.client.simGetVehiclePose(objName)
        else:
            pose = self.client.simGetObjectPose(objName)

        globalOrientation = airsimToScenicRotation(pose.orientation)
        yaw, pitch, roll = obj.parentOrientation.localAnglesFor(globalOrientation)

        location = airsimToScenicLocation(pose.position)
        values = dict(
            position=location,
            velocity=Vector(0, 0, 0),  #! placeholder
            speed=0,  #! placeholder
            angularSpeed=0,  #! placeholder
            angularVelocity=Vector(0, 0, 0),  #! placeholder
            yaw=yaw,
            pitch=pitch,
            roll=roll,
        )

        return values

    # ------------------- Utils -------------------

    # def setProperties(self, obj, properties):
    #     # set drone position and rotation
    #     self.client.simSetVehiclePose(
    #         airsim.Pose(airsim.Vector3r(0, 0, 0), airsim.to_quaternion(0, 0, 0)), False
    #     )  # ignore collision set to false

    #     # pose can also be directly manipulated
    #     pose = self.client.simGetVehiclePose()
    #     pose.position = pose.position + airsim.Vector3r(0.03, 0, 0)

    def objInScene(self, objName):
        return objName in self.client.simListSceneObjects()


# -------------- Static helper functions --------------


def tupleToVector3r(tuple):
    return airsim.Vector3r(tuple[0], tuple[1], tuple[2])


def scenicToAirsimRotation(orientation):
    pitch, yaw, roll = orientation.r.as_euler("XZY", degrees=True)
    return airsim.to_quaternion(pitch, roll, yaw)


def airsimToScenicRotation(orientation):
    # TODO does this return intrinsic or extrinsic euler angles
    pitch, roll, yaw = airsim.to_eularian_angles(
        orientation
    )  # TODO check order of pitch roll and yaw being applied
    angles = (pitch, yaw, roll)

    r = scipy.spatial.transform.Rotation.from_euler(
        seq="XZY", angles=angles, degrees=False  # TODO check if degrees
    )
    return Orientation(r)


def scenicToAirsimLocation(position):
    return airsim.Vector3r(position.x, position.y, -position.z)


def airsimToScenicLocation(position):
    return Vector(position.x_val, position.y_val, -position.z_val)


def scenicToAirsimScale(obj):
    # TODO fix scale ratio
    return airsim.Vector3r(obj.width, obj.length, obj.height)
