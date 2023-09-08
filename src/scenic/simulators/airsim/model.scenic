import trimesh
import json

from scenic.simulators.airsim.simulator import AirSimSimulator 
from scenic.simulators.airsim.actions import *
from scenic.simulators.airsim.behaviors import *
from scenic.core.utils import repairMesh


# ---------- global parameters ----------

# setting Default global parameters for any missing parameters
param timestep = 1
param airsimWorldInfoPth = None
param idleStoragePos = (1000,1000,1000)
param worldInfoPath = "/home/mary/Documents/AirSim/ScenicTesting/src/scenic/simulators/airsim/objs/cubes/"

# ---------- helper functions ----------
# REAL
def createMeshShape(assetFolder, assetName, name = ""):

    mesh = trimesh.load( globalParameters.worldInfoPath+assetFolder+"/"+assetName+".obj")
   
    if not mesh.is_watertight:
        print("repairing: ",assetName,name)
        mesh = repairMesh(mesh, verbose=True)
        
        if not mesh.is_volume:
            print(assetName,"has no volume")
            mesh = trimesh.load( globalParameters.worldInfoPath+"assets/Cube.obj")
    return MeshShape(mesh,scale=.01)

# QUICK
# def createMeshShape(assetFolder, assetName, name = ""):
#     mesh = trimesh.load( globalParameters.worldInfoPath+"assets/Cube.obj")
            
#     return MeshShape(mesh,scale=.01)


# ---------- simulator creation ----------
print("TS = ",globalParameters.timestep)
simulator AirSimSimulator(timestep=globalParameters.timestep,idleStoragePos=globalParameters.idleStoragePos) 


# ---------- base classes ----------
class AirSimPrexisting:
    name: None
    shape: createMeshShape("objectMeshes",self.name,self.name)
    allowCollisions: True
    blueprint: "AirSimPrexisting"

class AirSimActor:
        
    name: None
    assetName: None
    blueprint: None
    realObjName: None 

    # override
    shape: createMeshShape("assets",self.assetName)

    def __str__(self):
        return self.assetName


# ---------- inherited classes ----------
class Drone(AirSimActor):
    blueprint: "Drone"
    startHovering: True
    assetName: "Quadrotor1"
    _startPos: None

class StaticObj(AirSimActor):
    blueprint: "StaticObj"
    physEnabled: False



# ---------- body ----------

# # Create prexisiting airsim objs
with open(
    globalParameters.worldInfoPath+"worldInfo.json",
    "r",
) as inFile:
    # todo raise warning if there isn't a volume
    meshDatas = json.load(inFile)
    for meshData in meshDatas:
        new AirSimPrexisting with name meshData["name"],
            at meshData["position"],
            facing meshData["orientation"]