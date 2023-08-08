# param map_path = localPath('C:/Users/Mary/Documents/Code/Scenic/AirSimBinaries/Blocks/WindowsNoEditor/Blocks.exe')
model scenic.simulators.airsim.model


behavior MoveToPosition(x,y,z):
    take MoveToPositionAction(x,y,z)

new Drone at (0,0,0),  facing (20 deg, 10.6 deg,9.68 deg),
    with behavior MoveToPosition(4,4,2)

    
new Drone at (0,0,5)
# new Drone at (0,0,10)

new Object at (0,10,0),
    with width 2,
    with assetName "Cone",
    with name "fun"

new Object at (0,20,0),
    with width 2,
    with assetName "Cone",
    with name "cool"
# ego = new Drone at (0,0,0)