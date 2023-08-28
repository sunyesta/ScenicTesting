from scenic.core.simulators import Action
from scenic.simulators.airsim.simulator import scenicToAirsimLocation


class MoveToPositionAction(Action):
    def __init__(self, position):
        airsimPosition = scenicToAirsimLocation(position)
        self.x = airsimPosition.x_val
        self.y = airsimPosition.y_val
        self.z = airsimPosition.z_val

    def applyTo(self, agent, simulation):
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


behavior FlyToPosition(position, tolerance = 1):

    if distance from self to position < tolerance:
        return
    take MoveToPositionAction(position)
    while distance from self to position > tolerance:
        wait

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

    


behavior Follow(obj,tolerance=1):
    if distance from self to obj.position > tolerance:
        take FollowAction(obj)
