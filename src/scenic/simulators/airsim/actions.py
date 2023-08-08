import math as _math

import airsim as airsim

from scenic.core.simulators import Action
from scenic.core.vectors import Orientation, Vector
from scenic.simulators.airsim.simulator import scenicToAirsimLocation

# import scenic.simulators.airsim.model as airsimModel


class MoveToPositionAction(Action):
    def __init__(self, x, y, z):
        airsimPosition = scenicToAirsimLocation(Vector(x, y, z))
        self.x = airsimPosition.x_val
        self.y = airsimPosition.x_val
        self.z = airsimPosition.x_val

    def applyTo(self, agent, simulation):
        simulation.client.moveToPositionAsync(
            self.x,
            self.y,
            self.z,
            5,
            vehicle_name=agent.realObjName,
        )


# class MoveByVelocity(Action):
#     def __init__(self, vx, vy, vz, duration):
#         airsimVelocity = scenicToAirsimLocation(Vector(vx, vy, vz))
#         self.client.moveToPositionAsync(
#             airsimVelocity.x_val,
#             airsimVelocity.y_val,
#             airsimVelocity.z_val,
#             duration,
#             vehicle_name=self.realObjName,
#         )


# class moveByAngleAndThrottle(Action):
#     def __init__(self, x, y, z, throttle, duration):
#         self.client.moveByRollPitchYawThrottleAsync(
#             self, x, y, z, throttle, duration, vehicle_name=self.realObjName
#         )
