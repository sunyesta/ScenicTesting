workspace = Workspace(RectangularRegion((0,0,0), 0, 4, 4))
floor = workspace

ego = new Object with shape Uniform(BoxShape(), SpheroidShape(), ConeShape()),
                 with width Range(1,2),
                 with length Range(1,2),
                 with height Range(1,3),
                 facing (Range(0,360) deg, Range(0,360) deg, Range(0,360) deg)
                

chair = new Object on floor,
            with shape MeshShape.fromFile(localPath("../globalMeshes/chair.obj"),
                initial_rotation=(0,90 deg,0), dimensions=(1,1,1))

plane_shape = MeshShape.fromFile(path=localPath("../globalMeshes/plane.obj"))

plane = new Object left of chair by 1,
        with shape plane_shape,
   #     with width 2,
    #    with length 2,
     #   with height 1,
        facing directly toward ego

