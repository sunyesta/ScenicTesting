import trimesh

from scenic.simulators.airsim.simulator import AirSimSimulator    # for use in scenarios
from scenic.simulators.airsim.actions import *
from scenic.simulators.airsim.behaviors import *

# ---------- global parameters ----------
# Parameters of a scene like weather or time of day which are not associated with any object. 
# These are defined using the param statement, and can be overridden from the command line with the --param option.

# setting Default global parameters for any missing parameters
# TODO
param timestep = 4
param airsimWorldInfoPth = None

# applying global parameters
simulator AirSimSimulator(None, timestep=globalParameters.timestep) 

def createMeshShape(assetName):

    mesh = trimesh.load( "/home/mary/Documents/AirSim/ScenicTesting/src/scenic/simulators/airsim/objs/cubes/"+assetName+".obj")
    if not mesh.is_watertight:
        breakpoint()
        isWatertightNow = mesh.fill_holes()
        if not isWatertightNow:
            mesh = trimesh.load( "/home/mary/Documents/AirSim/ScenicTesting/src/scenic/simulators/airsim/objs/cubes/"+"Cube"+".obj")

    return MeshShape(mesh,scale=.01)




class AirSimPrexisting:
    name: None
    assetName: None
    shape: createMeshShape(self.assetName)


with open(
    "/home/mary/Documents/AirSim/ScenicTesting/src/scenic/simulators/airsim/objs/cubes/worldInfo.json",
    "r",
) as inFile:
    meshes = json.load(inFile)

    for mesh in meshes:
        new AirSimPrexisting at mesh.position,
            with name mesh.name,
            with assetName mesh.assetName,


class AirSimActor:
    def __init__(self, *args, **kwargs):
        #? should I do it like this?
        # showing as cubes?
        
        


        super().__init__(*args, **kwargs)
        
    
    name: None

    assetName: None

    # TODO make water tight if issue inside the exporter script
    # make the script create warnings for non watertight meshes
    # ask Eric about water tight mesh util func
    # shape: MeshShape(trimesh.load( "/home/mary/Documents/AirSim/ScenicTesting/src/scenic/simulators/airsim/objs/cubes/"+self.assetName+".obj"),scale=.01)
    shape: createMeshShape(self.assetName)
    blueprint: None
    realObjName: None 

    # override
    # TODO check this

    
    
    scale: None
    # print(f"{oi} at {oi.position} intersects" f" {oj} at {oj.position}")
    def __str__(self):
        return "cat"

class Drone(AirSimActor):
    blueprint: "Drone"
    startHovering: True
    assetName: "Quadrotor1"
    _startPos: None

class StaticObj(AirSimActor):
    blueprint: "Object"
    physEnabled: False
    