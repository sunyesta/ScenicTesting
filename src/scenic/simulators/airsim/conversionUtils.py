import airsim
from scenic.core.type_support import toVector
from scenic.core.vectors import Orientation, Vector
import scipy


def tupleToVector3r(tuple):
    return airsim.Vector3r(tuple[0], tuple[1], tuple[2])


def scenicToAirsimOrientation(orientation):
    pitch, yaw, roll = orientation.r.as_euler("XZY", degrees=False)
    return airsim.to_quaternion(pitch, roll, yaw)


def airsimToScenicOrientation(orientation):
    r = scipy.spatial.transform.Rotation.from_euler(
        seq="XZY", angles=airsimToScenicOrientationTuple(orientation), degrees=False
    )
    return Orientation(r)


def airsimToScenicOrientationTuple(orientation):
    # intrinsic angles
    pitch, roll, yaw = airsim.to_eularian_angles(orientation)
    angles = (pitch, yaw, roll)

    return angles


def scenicToAirsimLocation(position):
    position = toVector(position)
    return airsim.Vector3r(position.x, position.y, -position.z)


def scenicToAirsimLocationVector(position):
    position = toVector(position)
    return Vector(position.x, position.y, -position.z)


def airsimToScenicLocation(position):
    return Vector(
        position.x_val,
        position.y_val,
        -position.z_val,
    )


def airsimToScenicLocationTuple(position):
    return (
        position.x_val,
        position.y_val,
        -position.z_val,
    )


def scenicToAirsimScale(obj):
    # movment function in meters
    # drone size in blender is 98.1694 m
    # coords scaled by 100? https://microsoft.github.io/AirSim/apis/#:~:text=All%20AirSim%20API%20uses%20NED,in%20centimeters%20instead%20of%20meters.
    return airsim.Vector3r(obj.width, obj.length, obj.height)