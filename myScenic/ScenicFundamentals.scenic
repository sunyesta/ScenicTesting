ego = new Object with shape ConeShape(),
        with width 2,
        with length 2,
        with height 1.5,
        facing (-90 deg, 45 deg, 0)

chair = new Object at (4,0,2),
            with shape MeshShape.fromFile(localPath("../tools/meshes/chair.obj.bz2"), type="bz2",
                initial_rotation=(0,90 deg,0), dimensions=(1,1,1))

plane_shape = MeshShape.fromFile(path=localPath("../tools/meshes/plane.obj.bz2"), type="obj")

plane = new Object left of chair by 1,
            with shape plane_shape,
            with width 2,
            with length 2,
            with height 1,
            facing directly toward ego