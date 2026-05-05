from pybricks.parameters import *
from maths import *
from driveFunc import driveManager
from robot import *

r = robot(Port.E, Port.A, 5.6, 19.1, pos=vec2(18, 15.5))
r.lM.reverse = True
r.rM.switchDir = True
r.lM.switchDir = True
r.hub.addOffset(-90)
drive = driveManager(r)
