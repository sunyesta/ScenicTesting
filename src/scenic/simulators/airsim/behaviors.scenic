from scenic.core.simulators import Action
from scenic.simulators.airsim.simulator import scenicToAirsimLocation


class MoveToPositionAction(Action):
    def __init__(self, position):
        airsimPosition = scenicToAirsimLocation(position)
        self.x = airsimPosition.x_val
        self.y = airsimPosition.y_val
        self.z = airsimPosition.z_val

    def applyTo(self, agent, simulation):
        print("calling "+agent.realObjName)
        simulation.client.moveToPositionAsync(
            self.x,
            self.y,
            self.z,
            5,
            vehicle_name=agent.realObjName,
        )
        print("finished calling")


class MoveByVelocityAction(Action):
    def __init__(self, position, duration):
        airsimVelocity = scenicToAirsimLocation(position)
        self.x = airsimVelocity.x_val
        self.y = airsimVelocity.y_val
        self.z = airsimVelocity.z_val
        self.duration = duration

    def applyTo(self, agent, simulation):
        print("calling " + agent.realObjName)
        simulation.client.moveByVelocityAsync(
            self.x,
            self.y,
            self.z,
            self.duration,
            vehicle_name=agent.realObjName,
        )


behavior FlyToPosition(position, tolerance = 1):

    if distance from self to position < tolerance:
        return
    print(self.position,distance from self to position )
    take MoveToPositionAction(position)
    while distance from self to position > tolerance:
        print(self.position,distance from self to position )
        wait
    print("got to position: ",position)

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
    
    


