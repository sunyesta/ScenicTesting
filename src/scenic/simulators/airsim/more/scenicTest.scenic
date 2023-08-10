# param map_path = localPath('C:/Users/Mary/Documents/Code/Scenic/AirSimBinaries/Blocks/WindowsNoEditor/Blocks.exe')
model scenic.simulators.airsim.model


# ego = new Drone at (0,0,10),
#     with behavior MoveToPosition(4,4,2)



    
# new Drone at (3,3,3), with behavior FlyToPosition((10,10,10))
new Drone at (0,0,0), with behavior Patrol([(10,10,10),(10,0,10),(0,10,10),(0,0,10)])
# new Drone at (0,0,5)
# new Drone at (0,0,10)
    
# new Drone at (10,10,10), facing (30 deg,10 deg, 0),
#      with behavior FlyToPosition(1,1,1)
# new Drone at (-4,-4,5)

new StaticObj at (0,10,0),
    with width 2,
    with assetName "Cone",
    with name "fun"

new StaticObj at (0,20,0),
    with width 2,
    with assetName "Cone",
    with name "cool"
# ego = new Drone at (0,0,0)

# record ego.position as "ego position"