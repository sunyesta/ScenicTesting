from scenic.core.simulators import Action
from .conversionUtils import scenicToAirsimLocationVector


import airsim
import threading
from promise import Promise

def startWait(future):
    def joinAsync():
        future.join()
    
    if not future._loop:
        threading.Thread(target=joinAsync).start()

    return future

def getActualDronePos(drone,client):
    # print("getting",drone.realObjName)
    return client.simGetVehiclePose(drone.realObjName).position

class MoveToPositionAction(Action):
    def __init__(self, position):
        airsimPosition = scenicToAirsimLocation(position)
        self.x = airsimPosition.x_val
        self.y = airsimPosition.y_val
        self.z = airsimPosition.z_val

    def applyTo(self, agent, simulation):

        client = airsim.MultirotorClient()
        client.confirmConnection()
        client.moveToPositionAsync(
            self.x,
            self.y,
            self.z,
            5,
            vehicle_name=agent.realObjName,
        )
        simulation.client.moveToPositionAsync(
            self.x,
            self.y,
            self.z,
            5,
            vehicle_name=agent.realObjName,
        )
        


class MoveByVelocityAction(Action):
    def __init__(self, position, duration):
        airsimVelocity = scenicToAirsimLocation(position)
        self.x = airsimVelocity.x_val
        self.y = airsimVelocity.y_val
        self.z = airsimVelocity.z_val
        self.duration = duration

    def applyTo(self, agent, simulation):
        simulation.client.moveByVelocityAsync(
            self.x,
            self.y,
            self.z,
            self.duration,
            vehicle_name=agent.realObjName,
        )

class FollowAction(Action):
    def __init__(self, obj):
        airsimPosition = scenicToAirsimLocation(obj.position)
        self.x = airsimPosition.x_val
        self.y = airsimPosition.y_val
        self.z = airsimPosition.z_val

    def applyTo(self, agent, simulation):
        simulation.client.moveToPositionAsync(
            self.x,
            self.y,
            self.z,
            1,
            vehicle_name=agent.realObjName,
        )



behavior TestBehavior():
    print("testing behavior")
    wait

behavior FlyToPosition(position, speed = 5):

    airsimPosition = scenicToAirsimLocationVector(position)

    client = simulation().client

    reached = False

    
    prom = Promise.cast(client.moveToPositionAsync(
        airsimPosition.x,airsimPosition.y,airsimPosition.z,
        speed,
        vehicle_name=self.realObjName,
    ))

    print(prom)
    print("starting")
    print(prom.is_fulfilled)
    print(prom.is_pending)
    while not prom.is_fulfilled:
        # print(prom.is_fulfilled)
        wait
    

    print("reached:",self.position,getActualDronePos(self,client))
    return

behavior Patrol(positions, loop=True):
    
    while True:
        for pos in positions:
            do FlyToPosition(pos)
        if not loop:
            return




behavior MoveByVelocity(position,seconds):
    endTime = simulation().currentRealTime + seconds 
    take MoveByVelocityAction(position,seconds)
    

    while simulation().currentRealTime < endTime:
        wait

# ? how to run
behavior FlyToStart():
    print(self._startPos)
    do FlyToPosition(self._startPos)

    


behavior Follow(obj,speed = 5, interval = 5):
    client = simulation().client
    while True:
        position = scenicToAirsimLocationVector(obj.position)
        print(obj.position)
        # client.moveToPositionAsync(
        #     position.x,position.y,position.z,
        #     speed,
        #     vehicle_name=self.realObjName,
        # )
        do FlyToPosition(obj.position)
        # for i in range(interval):
        #     wait
