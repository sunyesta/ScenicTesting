# standard libs
import math
import time
from cmath import atan, pi, tan
from math import sin, radians, degrees, copysign

# third party libs
import airsim
import scipy
import numpy as np

# scenic libs
from scenic.core.vectors import Orientation, Vector
from scenic.core.type_support import toVector
from scenic.core.simulators import (
    Simulator,
    Simulation,
    SimulationCreationError,
    SimulatorInterfaceWarning,
)
from .conversionUtils import (
    scenicToAirsimLocation,
    scenicToAirsimOrientation,
    airsimToScenicLocation,
    airsimToScenicOrientation,
    scenicToAirsimScale,
)


def flyToPosition(client, drone, newPos):
    """flys the drone to the specified position

    Args:
        client (airsim client): airsim client
        drone (string): drone name in airsim
        newPose (vector or tuple): position you want the drone to go to
    """
    newPos = scenicToAirsimLocation(toVector(newPos))
    curPos = client.simGetVehiclePose(drone)
    # client.moveByVelocityAsync
