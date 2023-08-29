import trimesh
import json

from scenic.simulators.airsim.simulator import AirSimSimulator    # for use in scenarios
from scenic.simulators.airsim.actions import *
from scenic.simulators.airsim.behaviors import *
from scenic.core.utils import repairMesh


# ---------- global parameters ----------
# Parameters of a scene like weather or time of day which are not associated with any object. 
# These are defined using the param statement, and can be overridden from the command line with the --param option.

# setting Default global parameters for any missing parameters
# TODO
param timestep = 4
param airsimWorldInfoPth = None
param idleStoragePos = (1000,1000,1000)

# applying global parameters
simulator AirSimSimulator(None, timestep=globalParameters.timestep,idleStoragePos=globalParameters.idleStoragePos) 

def createMeshShape(assetName):

    mesh = trimesh.load( "/home/mary/Documents/AirSim/ScenicTesting/src/scenic/simulators/airsim/objs/cubes/"+assetName+".obj")
    
    if not mesh.is_watertight:
        mesh = repairMesh(mesh, verbose=True)
        if not mesh.is_watertight:
            mesh =  trimesh.load( "/home/mary/Documents/AirSim/ScenicTesting/src/scenic/simulators/airsim/objs/cubes/"+"Cube"+".obj")

    return MeshShape(mesh,scale=.01)


# TODO fix intersection problem!

class AirSimPrexisting:
    name: None
    assetName: None
    shape: createMeshShape(self.assetName)


# TODO fix when world positioning is fixed!
# with open(
#     "/home/mary/Documents/AirSim/ScenicTesting/src/scenic/simulators/airsim/objs/cubes/worldInfo.json",
#     "r",
# ) as inFile:
#     meshes = json.load(inFile)
#     for mesh in meshes:
#         new AirSimPrexisting at mesh["position"],
#             with name mesh["name"],
#             with assetName mesh["assetName"],


class AirSimActor:
    def __init__(self, *args, **kwargs):
        #? should I do it like this?
        # showing as cubes?
        
        


        super().__init__(*args, **kwargs)
        
    
    name: None

    assetName: None

    
    blueprint: None
    realObjName: None 

    # override
    shape: createMeshShape(self.assetName)
    
    
    scale: None
    # print(f"{oi} at {oi.position} intersects" f" {oj} at {oj.position}")
    def __str__(self):
        return self.assetName

class Drone(AirSimActor):
    blueprint: "Drone"
    startHovering: True
    assetName: "Quadrotor1"
    _startPos: None

class StaticObj(AirSimActor):
    blueprint: "StaticObj"
    physEnabled: False
    