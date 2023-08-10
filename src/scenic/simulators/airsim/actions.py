import math as _math

import airsim as airsim

from scenic.core.simulators import Action
from scenic.core.vectors import Orientation, Vector
from scenic.simulators.airsim.simulator import scenicToAirsimLocation

# import scenic.simulators.airsim.model as airsimModel


# class MoveToPositionBehavior(x, y, z):
#     # TODO verify position and if position isn't at goal, recall
#     def __init__(self, x, y, z):
#         airsimPosition = scenicToAirsimLocation(Vector(x, y, z))
#         self.x = airsimPosition.x_val
#         self.y = airsimPosition.y_val
#         self.z = airsimPosition.z_val

#     def applyTo(self, agent, simulation):
#         print(
#             "moving to position: drone = "
#             + agent.realObjName
#             + " at "
#             + str((self.x, self.y, self.z))
#         )
#         print("client = " + str(simulation.client))
#         simulation.client.moveToPositionAsync(
#             self.x,
#             self.y,
#             self.z,
#             5,
#             vehicle_name=agent.realObjName,
#         ).join()
#         simulation.client.hoverAsync().join()
#         print("did it")
#         simulation.client.simPause(True)


# class MoveByVelocity(Action):
#     def __init__(self, vx, vy, vz, duration):
#         airsimVelocity = scenicToAirsimLocation(Vector(vx, vy, vz))
#         self.client.moveByVelocityBodyFrameAsync(
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
