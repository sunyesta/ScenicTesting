import math as _math

import airsim as airsim

from scenic.core.simulators import Action
from scenic.core.vectors import Orientation, Vector
from scenic.simulators.airsim.simulator import scenicToAirsimLocation


# class moveByAngleAndThrottle(Action):
#     def __init__(self, x, y, z, throttle, duration):
#         self.client.moveByRollPitchYawThrottleAsync(
#             self, x, y, z, throttle, duration, vehicle_name=self.realObjName
#         )
