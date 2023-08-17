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


def getAssetName(meshName):
    return re.sub(r"_\d+$", "", meshName)


client = airsim.MultirotorClient()
client.confirmConnection()


client.simPause(True)

objNameDict = {}
assets = client.simListAssets()
for asset in assets:
    objName = client.simSpawnObject(
        object_name=asset,
        asset_name=asset,
        pose=airsim.Pose(position_val=airsim.Vector3r(0, 0, 0)),
        scale=airsim.Vector3r(1, 1, 1),
    )
    objNameDict[asset] = objName.lower()


meshes = client.simGetMeshPositionVertexBuffers()
# print(objNameDict)
# get all the meshes
meshDict = {}
for asset in assets:
    objName = objNameDict[asset]
    for mesh in meshes:
        if mesh.name == objName:
            # print(mesh.name)
            meshDict[asset] = mesh
            break

data = []

for assetName in assets:
    if not (assetName in meshDict):
        continue
    m = meshDict[assetName]
    vertex_list = np.array(m.vertices, dtype=np.float32)
    indices = np.array(m.indices, dtype=np.uint32)

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

    meshData = dict(name=m.name, isVolume=tmesh.is_volume, bodyCount=tmesh.body_count)
    data.append(dict(meshData))

    with open(
        "/home/mary/Documents/AirSim/ScenicTesting/src/scenic/simulators/airsim/objs/cubes/"
        + assetName
        + ".obj",
        "w",
    ) as outfile:
        outfile.write(trimesh.exchange.obj.export_obj(tmesh))

# with open("sample.json", "w") as outfile:
#     json.dump(data, outfile)
