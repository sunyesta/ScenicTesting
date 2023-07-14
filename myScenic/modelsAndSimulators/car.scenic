from scenic.simulators.gta.model import Car
workspace = Workspace(RectangularRegion((0,0,0), 0, 50, 50))
ground = workspace

ego = new Object on ground,
                with shape BoxShape(),
                with width Range(1,2),
                with length Range(1,2),
                with height Range(1,3),
                facing (Range(0,360) deg, Range(0,360) deg, Range(0,360) deg)
                 

bottleneck = new Object with shape ConeShape(), on ground
Pipe = new Object with shape SpheroidShape(), on ground


gap = 1.2 * ego.width
halfGap = gap / 2

leftEdge = new OrientedPoint left of bottleneck by halfGap,
    facing Range(60, 120) deg relative to bottleneck.heading
rightEdge = new OrientedPoint right of bottleneck by halfGap,
    facing Range(-120, -60) deg relative to bottleneck.heading

new Pipe ahead of leftEdge, with length Range(1, 2), on ground, facing leftEdge, with parentOrientation 0
#new Pipe ahead of rightEdge, with length Range(1, 2), on ground, facing rightEdge, with parentOrientation 0