from pybricks.tools import wait
from pybricks.parameters import Color, Port
from pybricks.pupdevices import ColorSensor
from Device_manager.maths import vec2
from Device_manager.robot import Robot
from pybricks.pupdevices import Motor

class cube:
    def __init__(self, color: Color, position: vec2):
        self.color = color
        self.pos = position

def setCubes():
    rShift = 31 #in mm
    c_shift = 31
    cubes = []
    for set in [
        [Color.YELLOW, vec2(0, 0)],
        [Color.BLUE, vec2(0, 0)],
        [Color.GREEN, vec2(0, 0)],
        [Color.WHITE, vec2(0, 0)],
    ]:
        cCubes = []
        for col in range(3):
            for row in range(2):
                cCubes.append(cube(set[0], set[1] + vec2(col * c_shift, row * rShift)))
        cubes.extend(cCubes)
    return cubes

class mozaikovator:
    def __init__(self, robot: Robot, liftMotor: Port, grabMotor: Port, excentricity: vec2):
        """
        has 3 chambers for cubes and 2 motors for lifting and grabbing cubes
        excentricity: center in center of rotation; x in direction of motion; y perpendicular to x positive to the left, measured in read/write position"""
        self.robot = robot
        self.cubes = []
        self.liftMotor = Motor(liftMotor)
        self.grabMotor = Motor(grabMotor)

    def up(self):
        self.liftMotor.run_target(1000, -145)

    def down(self):
        self.liftMotor.run_target(1000, 123)
    
    def midle(self):
        self.liftMotor.run_target(1000, 0)

    def dropPos(self):
        self.liftMotor.run_target(1000, 120)

    def grab(self):
        self.grabMotor.run(-1000)

    def release(self):
        self.grabMotor.run_target(1000, 0)

    def pickUp(self):
        self.release()
        self.down()
        wait(200)
        self.grab()
        wait(200)
        self.up()

    def drop(self):
        self.midle()
        self.release()
        self.up()

    def load(self, cubes: list[cube]):
        """loads 3 of each color in cubes"""
        for cube in cubes:
            #add drive to cube
            self.pickUp()
            self.cubes.append(cube)

    def unload(self, n = 4):
        """unloads all cubes in mozaikovator"""
        for i in range(n):
            #add drive to cube
            self.drop()
            self.cubes.pop(0)

class betonovator:
    def __init__(self, robot: Robot, motor: Port):
        """excentricity: center in center of rotation; x in direction of motion; y perpendicular to x positive to the left, measured in read/write position"""
        self.robot = robot
        self.motor = Motor(motor)
    
    def aling(self): #not used
        self.motor.run_target(1000, 0)

    def up(self):
        self.motor.run_target(1000, 55)

    def down(self):
        self.motor.run_target(500, -30)

#inicialization
robot = Robot()
mozaik = mozaikovator(robot, Port.F, Port.C, vec2(0, 0))
beton = betonovator(robot, Port.B)