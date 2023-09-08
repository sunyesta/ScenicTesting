import cv2
import airsim
import numpy as np
import os
import pprint
import tempfile
import trimesh
import json
import re
import time
from conversionUtils import (
    airsimToScenicOrientationTuple,
    airsimToScenicLocationTuple,
)

outputDirectory = (
    "/home/mary/Documents/AirSim/ScenicTesting/src/scenic/simulators/airsim/objs/cubes/"
)
os.makedirs(outputDirectory + "assets", exist_ok=True)
os.makedirs(outputDirectory + "objectMeshes", exist_ok=True)


def getAssetName(meshName):
    return re.sub(r"_\d+$", "", meshName)


# init airsim client
client = airsim.MultirotorClient()
client.confirmConnection()
client.simPause(True)

assets = client.simListAssets()
#! version 1
# TODO try to get data using unreal command line
# create objects of the assets
objNameDict = {}

for asset in assets:
    objName = client.simSpawnObject(
        object_name=asset,
        asset_name=asset,
        pose=airsim.Pose(position_val=airsim.Vector3r(0, 0, 0)),
        scale=airsim.Vector3r(1, 1, 1),
    )
    objNameDict[asset] = objName.lower()

meshes = client.simGetMeshPositionVertexBuffers()

print("got meshes")
meshDict = {}
for asset in assets:
    objName = objNameDict[asset]
    for mesh in meshes:
        if mesh.name == objName:
            # print(mesh.name)
            meshDict[asset] = mesh
            break


def makeTrimsh(mesh):
    vertex_list = np.array(mesh.vertices, dtype=np.float32)
    indices = np.array(mesh.indices, dtype=np.uint32)

    num_vertices = int(len(vertex_list) / 3)
    num_indices = len(indices)

    vertices_reshaped = vertex_list.reshape((num_vertices, 3))
    indices_reshaped = indices.reshape((int(num_indices / 3), 3))
    vertices_reshaped = vertices_reshaped.astype(np.float64)
    indices_reshaped = indices_reshaped.astype(np.int64)

    tmesh = trimesh.Trimesh(
        vertices=vertices_reshaped, faces=indices_reshaped, process=True
    )

    if tmesh.body_count > 1:
        tmesh.fix_normals(multibody=True)
    else:
        tmesh.fix_normals()

    return tmesh


# save an obj file for each asset
for assetName in assets:
    if not (assetName in meshDict):
        continue
    mesh = meshDict[assetName]
    tmesh = makeTrimsh(mesh)

    with open(
        outputDirectory + "assets/" + assetName + ".obj",
        "w",
    ) as outfile:
        outfile.write(trimesh.exchange.obj.export_obj(tmesh))


# ----------------- extract world info


cleanedMeshes = []
for mesh in meshes:
    found = False

    # check if mesh is in the created meshes
    for mesh2 in meshDict.values():
        if mesh.name == mesh2.name:
            found = True
            break

    # check if mesh is a vehicle
    for vehicle in client.listVehicles():
        if mesh.name == vehicle:
            found = True
            break

    # if mesh was not found in checks, add it to cleanedMeshes
    if not found:
        cleanedMeshes.append(mesh)

worldInfo = []
for mesh in cleanedMeshes:
    tmesh = makeTrimsh(mesh)

    objectName = mesh.name

    pose = client.simGetObjectPose(objectName)
    position = airsimToScenicLocationTuple(pose.position)
    orientation = airsimToScenicOrientationTuple(pose.orientation)

    worldInfo.append(
        dict(
            name=objectName,
            position=position,
            orientation=orientation,
        ),
    )
    with open(
        outputDirectory + "objectMeshes/" + objectName + ".obj",
        "w",
    ) as outfile:
        outfile.write(trimesh.exchange.obj.export_obj(tmesh))


with open(outputDirectory + "worldInfo.json", "w") as outfile:
    json.dump(worldInfo, outfile, indent=4)
