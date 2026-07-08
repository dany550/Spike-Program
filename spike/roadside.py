from setup import *                                                                                                                                                                                                                                                                                
from pybricks.tools import wait
from tester import *
from pybricks.pupdevices import UltrasonicSensor
from imgs import idown, iup
from umath import degrees

def side_decider():
    page = 0    
    while True:
        if drive.robot.hub.isButtonPressed(Button.LEFT):
            page = -1 #-1
            drive.robot.hub.color(Color.RED)
            drive.robot.hub.image(iup)
            drive.robot.hub.beep(400, 250)
        elif drive.robot.hub.isButtonPressed(Button.RIGHT):
            page = 1
            drive.robot.hub.color(Color.BLUE)
            drive.robot.hub.image(idown)
            drive.robot.hub.beep(800, 250)
        elif drive.robot.hub.isButtonPressed(Button.CENTER) and page != 0:
            drive.robot.hub.beep(600, 500)
            while drive.robot.hub.isButtonPressed(Button.CENTER):
                wait(10)
            if page == -1:
                drive.sideSwitch = -1
            return

def tpe(pos, speed = 1000, backwards = False, distance = 150, nerror = 0):
    drive.toPos(pos, speed, backwards = backwards, background=True,)
    error = 0
    ferror = False
    while drive.isTasksRunning():
        drive.runTasks()
        #print(ul.distance())
        if ferror and ul.distance() < 3 * distance:
            ferror = False
        if ul.distance() < distance or ferror:
            error += 1
            ferror = True
            drive.robot.stop()
            wait(1000)
            if nerror != 0 and error > nerror:
                drive.stopTasks()
                break

#sken class
def enemy_sken(ang = 180, val = 150, patience = 5, sample = 500): 
    drive.rotate(ang, 500)
    strike = 3
    for j in range(patience):
        for z in range(sample):
            if drive.robot.devices[2].distance() < val:
                drive.robot.hub.beep(1000, 200)
                wait(500) ### domyslet!
                strike += 1
                break
        strike -= 1
        wait(500)
        print("strike", strike)
        if strike == 0:
            return False
    drive.robot.hub.beep(1300, 500)
    return True
        
def car_sken(pos, distance = 20): ##otestovat!
    for i in range (4):
        enemy_sken(ang=180, val=70, sample=5)  # check for enemy robots
        drive.toPos(vec2((pos.x + distance * i), pos.y * drive.side), speed = cspeed, backwards=True)
        color = drive.robot.devices[3].color()
        c = 0
        while color == Color.NONE:
            c += 1
            drive.toPos(vec2((pos.x + distance * i + c), (pos.y - c)  * drive.side), speed = cspeed, backwards=True)
            drive.rotate(180, 500)
            color = drive.robot.devices[3].color()
        print("color", i, color)
        if color == drive.side_color:
            return i

def ultra_align(shift = 5):
    drive.rotate(180, 1000)  # rotate to align with the ultrasonic sensor
    x = drive.robot.devices[2].distance  # get the distance from the ultrasonic sensor
    drive.rotate(-90 * drive.side, 1000)  # rotate to align with the battery pickup position
    y = drive.robot.devices[2].distance  # get the distance from the ultrasonic sensor
    drive.robot.pos = vec2((x + shift), (y + shift) * drive.side)  # set the robot position

"""
#hook class
def hook_pickup(): ##otestovat!
    hook_setup(300)
    drive.hooks = [True, True]

def hook_drop(N: int):
    N = clamp(N, 0, 1)
    drive.turnMotor(N, 100 * drive.hook_speeds[N], simple=True)
    drive.hooks[N] = False

def battery_pickup(pickup_pos):
    hook_setup()
    drive.toPos(vec2(pickup_pos.x, (pickup_pos.y - 13)  * drive.side), speed = cspeed)
    drive.rotate(90 * drive.side)
    drive.toPos(vec2(pickup_pos.x, pickup_pos.y * drive.side), speed = cspeed)
    hook_pickup()

def battery_delivery(car_number, Starting_pos = vec2(80, 35), car_distance = 20, hook_shift = 2, both = False): #75 22
    if drive.hooks[0] == True:
        N = 0
        hook = hook_shift
    elif drive.hooks[1] == True:
        N = 1
        hook = -hook_shift
    else:
        return False
    drive.toPos(vec2((Starting_pos.x + car_number * car_distance + hook), Starting_pos.y * drive.side), speed = 500)
    drive.rotate(-90 * drive.side, 500)
    if both == False:
        hook_drop(N)
    else:
        hook_setup()
    drive.toPos(vec2((Starting_pos.x + car_number * car_distance + hook), (Starting_pos.y+10) * drive.side), speed = 500, backwards=True)
    hook_setup(300)
    return(True)
"""
    
class Line:
    def __init__(self, a: vec2, b: vec2, full: bool):
        self.a = a
        self.b = b
        self.full = full
        self.direction = (b - a).normalize()
        self.normal = vec2(-self.direction.y, self.direction.x)
        self.parC = - self.normal.x * self.a.x - self.normal.y * self.a.y
        self.orientation = self.direction.xAngle()

    def move(self, shift: vec2):
        self.a += shift
        self.b += shift

    def translated(self, shift: vec2):
        """new line parallel to the original and shifted by given vector"""
        return Line(self.a + shift, self.b + shift)

class Car:
    def __init__(self, pos: vec2):
        self.pos = pos
        self.color = Color.NONE

def alignWall(wall: Line, contact: vec2, speed, time = 2000, gyroCorrection = False):
    """contact is a vector from center of rotation to the side of contact, positive x is in default direction of motion"""
    timer = StopWatch()
    timer.reset()
    while timer.time() < time:
        drive.robot.setSpeed(speed, speed)
        #drive.robot.update()
    drive.robot.stop()
    #drive.robot.update()
    drive.robot.lM.deltaAngle = 0
    drive.robot.rM.deltaAngle = 0
    drive.robot.rM.setDefAngle()
    drive.robot.lM.setDefAngle()


    if round(wall.orientation) == 0:
        drive.robot.pos.y = (wall.a.y - contact.x)*drive.sideSwitch 
    elif abs(wall.orientation - pi/2) < 0.1:
        drive.robot.pos.x = wall.a.x - contact.x
    else:
        drive.robot.hub.m_hub.speaker.beep()
        print("incorrect wall orientation: ", wall.orientation)
    if gyroCorrection:
        drive.robot.hub.resetAngle()
        drive.robot.hub.addOffset(degrees(wall.orientation) + 90*sign(contact.x))


#/map def
carY = 17
carXShift = 20
carXO = 75
cars = [Car(vec2(carXO + i * carXShift, carY)) for i in range(8)]
carWall = Line(vec2(75 ,23), vec2(230, 23), False)
xWall = Line(vec2(0, 0), vec2(300, 0), True)
yWall = Line(vec2(0, 0), vec2(0, 200), True)
xxWall = Line(vec2(0, 200), vec2(300, 200), True)
yyWall = Line(vec2(300, 0), vec2(300, 200), True)
batteryWall = Line(vec2(130, 80), vec2(170, 80), False)
signWall = Line(vec2(120, 100), vec2(180, 100), False)
lorryWall = Line(vec2(70, 120), vec2(70, 200), False)
olorryvall = Line(vec2(230, 120), vec2(230, 200), False)
depoWall = Line(vec2(130, 175), vec2(170, 175), False)
rback = vec2(-3.5, 0)
rfront = vec2(8.1, 0)

class Multitool:
    def __init__(self, color: Color, motor: Port, motor2: Port, cs: Port, drive: driveManager, batteryExcentricity: vec2, csExcentricity: vec2):
        self.color = color
        self.motor = Motor(motor)
        self.motor2 = Motor(motor2)
        self.cs = ColorSensor(cs)
        self.drive = drive
        self.batteryExcentricity = batteryExcentricity
        self.csExcentricity = csExcentricity
    
    def up(self):
        self.motor.run_target(1000, 0, wait=False)
        self.motor2.run_target(1000, 0)


    def middleLow(self):
        self.motor.run_target(1000, 80, wait=False)
        self.motor2.run_target(1000, -80)

    def middle(self):
        self.motor.run_target(1000, 60, wait=False)
        self.motor2.run_target(1000, -60)

    def down(self):
        self.motor.run_target(1000, 90, wait=False)
        self.motor2.run_target(1000, -90)

    def sken(self, pos: vec2, shift = 20):
        done = False
        cars = []
        for i in range(4):
            if not done:
                tpe(pos + vec2(-self.csExcentricity.x*self.drive.sideSwitch + i * shift, 0), backwards = (self.color == Color.RED))
                self.drive.rotate(90 - 90 * self.drive.sideSwitch)
            hue = self.cs.hsv().h
            if hue < 300:
                color = Color.BLUE
            elif hue > 300:
                color = Color.RED
            if color == self.color and not done:
                self.drive.robot.hub.beep(400, 100)
                done = True
                cars.append((pos+vec2((i) * shift, 0)))
            else:
                cars.append((pos+vec2((7-i) * shift, 0)))
        return cars

    def batUp(self, pos):
        self.drive.toPos(pos - vec2(0, 25), backwards=True)
        self.drive.rotate(-90 * self.drive.sideSwitch)
        self.middleLow()
        self.drive.toPos(pos - vec2(0, 15), backwards=True)
        self.up()
        self.drive.toPos(pos - vec2(0, 20))

    def batDown(self, pos):
        tpe(pos + vec2(0, 10))
        self.drive.rotate(90 * self.drive.sideSwitch)
        self.drive.toPos(pos - vec2(0, 5), backwards=True)
        self.middle()
        self.drive.toPos(pos + vec2(0, 15), backwards=False)
        self.up()

    def load(self, cars, bats):
        ncars = len(cars)
        for i in range(ncars):
            self.batUp(bats[i])
            self.batDown(cars[ncars - i - 1])

            




#main class
cspeed = 750
def m1():
    #start
    #drive.circleToPos(vec2(50, 70), connect=[False, True], speed = cspeed, backwards=True)
    #drive.straight(5, backwards=False, speed = cspeed)
    drive.toPos(vec2(60, 40 * drive.side), speed = cspeed, backwards=True)
    drive.toPos(vec2(50, 160 * drive.side), backwards=False, speed = cspeed)

    #ninja moves
    drive.rotate(45 * drive.side)
    #hook_align()
    #drive.rotate(90)
    #drive.toPos(vec2(50, 165 * drive.side))

    #zarovnání zpět
    drive.toPos(vec2(50, 50 * drive.side), backwards = False)
    #nájezd na křižovatku m1 m2
    #drive.circleToPos(vec2(100  * drive.side, 40), connect=[False, True], speed = cspeed, backwards=True)
    #drive.toPos(vec2(50, 50 * drive.side), speed = cspeed, backwards=True)

"""
def m2():
    #nájezd na auta
    car_N = car_sken(vec2(81 ,34), 20)
    hook_align()
    hook_setup()
    print(car_N)
    battery_shift = 0
    cars = [car_N, 4, 5, 6, 7]
    cars.pop(len(cars) - 1 - car_N)  # remove car_N from the list
    print("cars", cars)
    
    for car in cars:
        if battery_delivery(car) == False:
            print("pickup")
            battery_pickup(vec2(142, (48 + battery_shift)))  # pickup position
            battery_shift += 6
            ### | dodělat! + check?
            battery_delivery(car)

def m22():
    #nájezd na auta
    car_N = car_sken(vec2(81 ,34), 20)
    hook_align()
    hook_setup()
    print(car_N)
    battery_shift = 0
    cars = [car_N, 4, 5, 6, 7]
    cars.pop(len(cars) - 1 - car_N)  # remove car_N from the list
    print("cars", cars)
    
    car = cars[0]
    if battery_delivery(car, both = True) == False:
        print("pickup")
        battery_pickup(vec2(142, (48 + battery_shift)))  # pickup position
        battery_shift += 6
        ### | dodělat! + check?
        battery_delivery(car)

def mF():
    drive.toPos(vec2(25, 40 * drive.side))
"""
    
#main 
def Roadmain():
    #start
    side_decider()

    #init
    s = drive.sideSwitch
    if s == 1:
        col = Color.BLUE
    else:
        col = Color.RED
    drive.robot.pos = vec2(5,33*s)
    drive.robot.hub.resetAngle()
    drive.robot.hub.addOffset(0)
    print(drive.robot.hub.angle(), " | ", drive.robot.pos)
    m = Multitool(col, Port.E, Port.C, Port.A, drive, vec2(-21, 0), vec2(6, -13))
    batts = [vec2(135, 70), vec2(141, 70), vec2(147, 70), vec2(153, 70)]

    tpe(vec2(55, 40))
    cars = m.sken(vec2(74, 37))
    m.load(cars, batts)

    #naklaďák
    drive.toPos(vec2(55, 40))
    #drive.toPos(vec2(50, 180), backwards=True)
    #tpe(vec2(55, 70))
    drive.toPos(vec2(55, 180), backwards=True)
    drive.toPos(vec2(55, 160))
    drive.toPos(vec2(80, 175))
    drive.toPos(vec2(40, 185), backwards=True)
    #drive.rotate(45 * s)
    drive.toPos(vec2(50, 100))
    tpe(vec2(50, 50), distance=400, nerror=1)
    drive.toPos(vec2(0, drive.robot.pos.y*s))

    """
    m.up()
    drive.rotate(90*s)
    alignWall(xWall, rback, -500)
    print(drive.robot.pos)
    drive.robot.update()
    print(drive.robot.pos)
    drive.toPos(vec2(drive.robot.pos.x, 20))
    drive.rotate(0)
    alignWall(yWall, rback, -500)
    print(drive.robot.pos)
    
    cars = m.sken(vec2(74, 37))
    m.load(cars, batts)
    """
    #
    

    #baterie
    
    #m.sken(vec2(80, 40))

def Roadmain1():
    #start
    side_decider()

    #init
    s = drive.sideSwitch
    if s == 1:
        col = Color.BLUE
    else:
        col = Color.RED
    drive.robot.pos = vec2(5,33*s)
    drive.robot.hub.resetAngle()
    drive.robot.hub.addOffset(0)
    print(drive.robot.hub.angle(), " | ", drive.robot.pos)
    m = Multitool(col, Port.E, Port.C, Port.A, drive, vec2(-21, 0), vec2(6, -13))
    batts = [vec2(135, 70), vec2(141, 70), vec2(147, 70), vec2(153, 70)]

    #naklaďák
    tpe(vec2(55, 40))
    #drive.toPos(vec2(50, 180), backwards=True)
    #tpe(vec2(55, 70))
    drive.toPos(vec2(55, 180), backwards=True)
    drive.toPos(vec2(55, 160))
    drive.toPos(vec2(80, 175))
    drive.toPos(vec2(40, 185), backwards=True)
    #drive.rotate(45 * s)
    drive.toPos(vec2(50, 100))
    tpe(vec2(50, 50), distance=400, nerror=1)
    tpe(vec2(150, drive.robot.pos.y*s), nerror=60)
    drive.toPos(vec2(0, drive.robot.pos.y*s), backwards=True)

    