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
from scenic.core.type_support import toVector

import numpy as np

from scenic.core.simulators import (
    Simulator,
    Simulation,
    SimulationCreationError,
    SimulatorInterfaceWarning,
)

import airsim


class AirSimSimulator(Simulator):
    def __init__(self, map_path, timestep=0.1, idleStoragePos=(0, 0, 0)):
        # print(airsim.Vector3r(100, 100, 100))

        # initializing airsim

        try:
            client = airsim.MultirotorClient()
            client.confirmConnection()
            client.simPause(True)
            pass
        except Exception:
            raise RuntimeError("Airsim must be running on before executing scenic")

        self.client = client
        self.idleStoragePos = idleStoragePos
        super().__init__()

    def createSimulation(self, scene, **kwargs):
        return AirSimSimulation(self, scene, self.client, **kwargs)

    def destroy(self):
        super().destroy()


class AirSimSimulation(Simulation):
    # ------------------- Required Methods -------------------

    def __init__(self, simulator, scene, client, **kwargs):
        self.simulator = simulator
        self.client = client
        self.joinables = []
        self.objs = {}

        super().__init__(scene, **kwargs)

    def setup(self):
        self.client.simPause(True)

        self.joinables = []
        self.objTrove = []

        self.startDrones = self.client.listVehicles()
        self.client.simPause(False)
        for i, drone in enumerate(self.startDrones):
            newPose = airsim.Pose(
                position_val=scenicToAirsimLocation(self.simulator.idleStoragePos)
                + airsim.Vector3r(i, 0, 0)
            )
            self.client.enableApiControl(True, drone)
            self.client.simSetVehiclePose(
                vehicle_name=drone, pose=newPose, ignore_collision=False
            )
            self.client.moveByVelocityAsync(0, 0, 0, 1, vehicle_name=drone)

        self.client.simPause(True)
        self.nextAvalibleDroneIndex = 0

        # create objs
        super().setup()

    def createObjectInSimulator(self, obj):
        # ------ set default values ------
        if not obj.name:
            obj.name = str(hash(obj))

        # ensure obj isn't already in world
        if obj.name in self.objs:
            raise RuntimeError(
                "there is already an object of the name "
                + obj.name
                + " in the simulator"
            )

        realObjName = obj.name + str(hash(obj))
        obj.realObjName = realObjName
        # ------------

        pose = airsim.Pose(
            position_val=scenicToAirsimLocation(obj.position),
            orientation_val=scenicToAirsimRotation(obj.orientation),
        )

        if obj.blueprint == "Drone":
            obj._startPos = obj.position

            # if there is an avalible drone, take it
            if self.nextAvalibleDroneIndex < len(self.startDrones):
                realObjName = self.startDrones[self.nextAvalibleDroneIndex]
                self.nextAvalibleDroneIndex += 1
                obj.realObjName = realObjName
            else:
                self.client.simAddVehicle(
                    vehicle_name=realObjName, vehicle_type="simpleflight", pose=pose
                )
            self.objs[obj.name] = realObjName
            self.client.enableApiControl(True, realObjName)
            self.client.armDisarm(True, realObjName)

            self.client.simSetVehiclePose(
                vehicle_name=realObjName, pose=pose, ignore_collision=True
            )

            if obj.startHovering:
                self.client.moveByVelocityAsync(0, 0, 0, 1, vehicle_name=realObjName)
            else:
                # shut off drone propellers
                self.client.moveByVelocityAsync(0, 0, 0, -1, vehicle_name=realObjName)

        else:
            if not (obj.assetName in self.client.simListAssets()):
                raise RuntimeError("no asset of name found: " + obj.assetName)

            # print("creating:" + obj.name + " " + realObjName)

            realObjName = self.client.simSpawnObject(
                object_name=realObjName,
                asset_name=obj.assetName,
                pose=pose,
                scale=scenicToAirsimScale(obj),
                physics_enabled=obj.physEnabled,
                is_blueprint=False,
            )

            self.objs[obj.name] = realObjName
            self.objTrove.append(realObjName)
        # print(f"Created object {realObjName} from asset {obj.assetName} ")

    def initializeDronePosition(self, droneName, pose):
        self.client.simPause(False)

        time.sleep(4)

        # print("new pose = "+str(pose.position))

        # joinable = self.client.moveToPositionAsync(
        #     pose.position.x_val,
        #     pose.position.y_val,
        #     pose.position.z_val,
        #     10,
        #     vehicle_name=droneName,
        # )

        joinable = self.client.takeoffAsync(
            vehicle_name=droneName,
        )
        self.joinables.append(joinable)
        self.client.simPause(True)

        # save our newly created drone
        self.vehicles = self.client.listVehicles()

    def step(self):
        # step 1 frame
        self.client.simContinueForTime(self.timestep)
        pass

    def waitForJoinables(self):
        self.client.simPause(False)
        for joinable in self.joinables:
            joinable.join()
        self.client.simPause(True)
        print("joined " + str(len(self.joinables)))
        self.joinables = []

    # ------------------- Other Simulator methods -------------------

    def destroy(self):
        print("\n\n\ndestroying!!!")
        client = airsim.MultirotorClient()
        client.confirmConnection()
        client.simPause(True)

        print(self.objTrove)
        # ? nothing wants to run after a client method is called?
        # client.simPause(False)
        for obj_name in self.objTrove:
            print("destroying:" + obj_name)
            client.simDestroyObject(obj_name)

        # for drone in client.listVehicles():
        client.reset()
        super().destroy()

    def getProperties(self, obj, properties):
        # # get object properties (not sure if neccessary since objects don't move)
        objName = self.objs[obj.name]

        pose = None

        velocity, speed, angularSpeed, angularVelocity = None, None, None, None
        if obj.blueprint == "Drone":
            pose = self.client.simGetVehiclePose(objName)
            kinematics = self.client.simGetGroundTruthKinematics(objName)
            velocity = airsimToScenicLocation(kinematics.linear_velocity)

            angularVelocity = airsimToScenicLocation(kinematics.angular_velocity)

        elif obj.blueprint == "StaticObj":
            pose = self.client.simGetObjectPose(objName)

            # static objs don't have velocity
            velocity = Vector(0, 0, 0)
            angularVelocity = Vector(0, 0, 0)

        globalOrientation = airsimToScenicRotation(pose.orientation)
        yaw, pitch, roll = obj.parentOrientation.localAnglesFor(globalOrientation)

        location = airsimToScenicLocation(pose.position)

        speed = math.hypot(velocity.x, velocity.y, velocity.z)
        angularSpeed = math.hypot(
            angularVelocity.x, angularVelocity.y, angularVelocity.z
        )

        values = dict(
            position=location,
            velocity=velocity,
            speed=speed,
            angularSpeed=angularSpeed,
            angularVelocity=angularVelocity,
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
    pitch, yaw, roll = orientation.r.as_euler("XZY", degrees=False)
    return airsim.to_quaternion(pitch, roll, yaw)


def airsimToScenicRotation(orientation):
    # intrinsic angles
    pitch, roll, yaw = airsim.to_eularian_angles(orientation)
    angles = (pitch, yaw, roll)

    r = scipy.spatial.transform.Rotation.from_euler(
        seq="XZY", angles=angles, degrees=False
    )
    return Orientation(r)


def scenicToAirsimLocation(position):
    position = toVector(position)
    return airsim.Vector3r(position.x, position.y, -position.z)


def airsimToScenicLocation(position):
    return Vector(
        position.x_val,
        position.y_val,
        -position.z_val,
    )


def scenicToAirsimScale(obj):
    # movment function in meters
    # drone size in blender is 98.1694 m
    # coords scaled by 100? https://microsoft.github.io/AirSim/apis/#:~:text=All%20AirSim%20API%20uses%20NED,in%20centimeters%20instead%20of%20meters.
    return airsim.Vector3r(obj.width, obj.length, obj.height)
