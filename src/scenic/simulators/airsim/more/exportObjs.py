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

outputDirectory = (
    "/home/mary/Documents/AirSim/ScenicTesting/src/scenic/simulators/airsim/objs/cubes/"
)


def getAssetName(meshName):
    return re.sub(r"_\d+$", "", meshName)


# init airsim client
client = airsim.MultirotorClient()
client.confirmConnection()
client.simPause(True)

assets = client.simListAssets()
#! version 1

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

#! version 2

# meshesRaw = None
# with open(
#     "/home/mary/Documents/AirSim/ScenicTesting/src/scenic/simulators/airsim/more/meshData.json",
#     "r",
# ) as inFile:
#     meshesRaw = json.load(inFile)


# class MeshGood:
#     def __init__(self, mesh):
#         self.name = mesh["name"]
#         self.vertices = mesh["vertices"]
#         self.indices = mesh["indices"]
#         self.assetName = mesh["assetName"]


# meshes = []
# for mesh in meshesRaw:
#     meshes.append(MeshGood(mesh))

# meshDict = {}
# for mesh in meshes:
#     if mesh.assetName:
#         meshDict[mesh.assetName] = mesh

# !!!!

# save an obj file for each asset
indicesDict = {}
for assetName in assets:
    if not (assetName in meshDict):
        continue
    mesh = meshDict[assetName]
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

    # assert tmesh.is_volume

    indicesDict[assetName] = indices

    with open(
        outputDirectory + assetName + ".obj",
        "w",
    ) as outfile:
        outfile.write(trimesh.exchange.obj.export_obj(tmesh))


# ----------------- extract world info

# todo makes meshes dict without added objs

cleanedMeshes = []
for mesh in meshes:
    found = False
    for mesh2 in meshDict.values():
        if mesh.name == mesh2.name:
            found = True
            break
    if not found:
        cleanedMeshes.append(mesh)
# print(indicesDict["Cone"])

worldInfo = {}
for mesh in cleanedMeshes:
    indices = np.array(mesh.indices, dtype=np.uint32)
    assetName = None
    for assetName2, indices2 in indicesDict.items():
        # print(indices2)
        if np.array_equal(indices, indices2):
            assetName = assetName2
            break

    if not assetName:
        print("no asset found for mesh ", mesh.name)
        continue

    pose = client.simGetObjectPose(objName)

    print(pose)
    position = (pose.position.x_val, pose.position.y_val, pose.position.z_val)
    orientation = airsim.to_eularian_angles(pose.orientation)

    worldInfo[mesh.name] = dict(
        assetName=assetName, position=position, orientation=orientation
    )


with open(outputDirectory + "worldInfo.json", "w") as outfile:
    json.dump(worldInfo, outfile, indent=4)
