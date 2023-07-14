# Running
# scenic examples/driving/badlyParkedCarPullingIn2.scenic \
#     --2d       \
#     --simulate \
#     --model scenic.simulators.lgsvl.model \
#     --time 200 \
#     --param map assets/maps/LGSVL/borregasave.xodr \
#     --param lgsvl_map BorregasAve



param map = localPath('../../tests/formats/opendrive/maps/CARLA/Town05.xodr')
param carla_map = 'Town05'
param time_step = 1.0/10

model scenic.domains.driving.model

behavior PullIntoRoad():
    while (distance from self to ego) > 15:
        wait
    do FollowLaneBehavior(laneToFollow=ego.lane)

# behavior WaitUntilClose(threshold=15):
#     while distance from self to ego > threshold:
#         require self.distanceToClosest(Pedestrian) > threshold
#         wait
#     do FollowLaneBehavior()

# behavior DriveWithRandomStops():
#     delay = Range(15, 30) seconds #issue!
#     last_stop = 0
#     try:
#         do Drive()
#     interrupt when simulation().currentTime - last_stop > delay:
#         do StopBehavior() for 5 seconds
#         delay = Range(15, 30) seconds
#         last_stop = simulation().currentTime  



ego = new Car with behavior DriveAvoidingCollisions(avoidance_threshold=5)

rightCurb = ego.laneGroup.curb
spot = new OrientedPoint on visible rightCurb
badAngle = Uniform(1.0, -1.0) * Range(10, 20) deg
parkedCar = new Car left of spot by 0.5,
                facing badAngle relative to roadDirection,
                with behavior PullIntoRoad

require (distance to parkedCar) > 20

monitor StopAfterInteraction():
    for i in range(50):
        wait
    while ego.speed > 2:
        wait
    for i in range(50):
        wait
    terminate
require monitor StopAfterInteraction()
terminate after 15 seconds   # in case ego never breaks
