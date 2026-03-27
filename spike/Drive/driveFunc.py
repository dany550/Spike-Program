from Device_manager.maths import *
from Device_manager.robot import Robot
from Device_manager.motor import motor
from Device_manager.hub import Hub
from pybricks.parameters import Port
from pybricks.tools import wait

#todo circle to pos background

class Drivesettings:
    def __init__(self):
        pass

class driveManager:
    def __init__(self, robot:Robot, leftPort: Port, rightPort: Port, wDiameter: float, axle: float):
        self.robot = robot
        self.lM = motor(leftPort, robot)
        self.rM = motor(rightPort, robot)
        self.wDiameter = wDiameter
        self.axle = axle
        self.pos = vec2(0,0)
        self.setDefaultMode()
        #curves
        self.cTolerance = 0.5
        self.cAcc = 100
        self.cDeacc = 50
        self.cStart = vec2(0,0)
        self.cFinish = vec2(0,0)

    def setDefaultMode(self):
        #both
        self.defspeed = 250
        #drive
        self.acc = 80
        self.deacc = 30
        self.turnCoeff = 3
        self.brake = True
        #rotate
        self.tolDiff = pi/90
        self.accuracy = 0.01
        self.racc = 500
        self.rdeacc = 500
        self.braker = True
    
    def setFastMode(self):
        #both
        self.defspeed = 100
        #drive
        self.acc = 300
        self.deacc = 300
        self.turnCoeff = 5
        self.brake = True
        #rotate
        self.tolDiff = pi/180
        self.accuracy = 0.01
        self.racc = 800
        self.rdeacc = 800
        self.braker = True
        
    def setPreciseMode(self):
        #both
        self.defspeed = 50
        #drive
        self.acc = 20
        self.deacc = 20
        self.turnCoeff = 10
        self.brake = True
        #rotate
        self.tolDiff = pi/180
        self.accuracy = 0.001
        self.racc = 100
        self.rdeacc = 100
        self.braker = True
        
    def setStartMode(self):
        #both
        self.defspeed = 110
        #drive
        self.acc = 100
        self.deacc = 10000000
        self.turnCoeff = 2
        self.brake = False
        #rotate
        self.tolDiff = pi/180
        self.accuracy = 0.0015
        self.racc = 555
        self.rdeacc = 555
        self.braker = True
        
    def setConnectMode(self):
        #both
        self.defspeed = 1000
        #drive
        self.acc = 0
        self.deacc = 0
        self.turnCoeff = 2
        self.brake = False
        #rotate
        self.tolDiff = pi/180
        self.accuracy = 0.0015
        self.racc = 555
        self.rdeacc = 555
        self.braker = True
        
    def setFinishMode(self):
        #both
        self.defspeed = 110
        #drive
        self.acc = 10000000
        self.deacc = 50
        self.turnCoeff = 2
        self.brake = True
        #rotate
        self.tolDiff = pi/180
        self.accuracy = 0.0015
        self.racc = 555
        self.rdeacc = 555
        self.braker = True   
    

    def setSpeed(self, lSpeed: float, rSpeed: float):
        self.lM.setSpeed(lSpeed)
        self.rM.setSpeed(rSpeed)
        pass
    
    def stop(self, brake = True):
        if brake:
            self.lM.hold()
            self.rM.hold()
            wait(200)
            self.lM.brake()
            self.rM.brake()
        else:
            self.lM.brake()
            self.rM.brake()
        pass

    def update(self):
        self.pos += self.navigate(self.lM, self.rM, self.robot.hub, self.wDiameter)

    def navigate(self, lM:motor, rM:motor, hub:Hub, diameter): ########wtf
        scalar = (lM.deltaAngle*diameter + rM.deltaAngle*diameter) * 0.25
        vec = scalar * mat2.rotation(hub.angleRad()) * vec2(1, 0)
        lM.Update()
        rM.Update()
        return vec

    def setMotorsToDef(self):
        self.lM.setDefAngle()
        self.rM.setDefAngle()
    
    def straight(self, length: float, speed = 1000, backwards = False, background = False):
        self.toPos(self.pos + mat2.rotation(self.robot.hub.angleRad()) * vec2(length,0), speed, backwards, background=background)
    
    def circle(self, center: vec2, circlePercentage, speed = 1000):
        angle = asin((center - self.pos).normalize().y) - sign(circlePercentage)*pi*0.5
        self.rotateRad(angle)
        finalPos = mat2.rotation(2*pi*circlePercentage)*(self.pos - center) + center
        r = (self.pos - center).length()
        ratio = (r-self.axle*0.5)/(r+self.axle*0.5)
        side = -sign(circlePercentage)
        startPos = self.pos
        
        length = abs(r*angleDiff((startPos - center).xAngle(), (finalPos - center).xAngle()))
        apos = length
        while(apos > 0.5):
            apos = abs(r*angleDiff((self.pos - center).xAngle(), (finalPos - center).xAngle()))
            aspeed = self.calcSpeed(vec2(length-apos,0), length, speed) + 100
            self.update()
            if side > 0:
                self.setSpeed(aspeed, aspeed*ratio)
            else:
                self.setSpeed(aspeed*ratio, aspeed)
        self.stop(self.brake)

    def toPosGen(self, pos: vec2, speed = 1000, backwards = False, stop = True, turn = True, tolerance = 0.0, extraDist = 0.0, background = False, connect = [False, False]):
        offset:vec2 = self.pos
        angle:float = atan2((pos-offset).y,(pos-offset).x)
        rotMat:mat2 = mat2.rotation(-angle)
        if backwards:
            angle += (pi)
        if turn and not connect[0]:
            if background:
                self.rotateRad(angle, background=True)
                while angleDiff(self.robot.hub.angleRad(), angle) > self.tolDiff:
                    yield
            else:
                self.rotateRad(angle)
        length = rotMat*(pos - offset)
        swap = sign(length.x - (rotMat*self.pos).x)
        swap = 1
        movedPos:vec2 = rotMat*(self.pos-offset)
        while(movedPos.x*swap < length.x*swap - tolerance):
            self.update()
            self.calcDir(rotMat*(self.pos-offset), length.x, self.calcSpeed(movedPos, length.x, speed, connect = connect),angle, backwards, extraDist)
            movedPos = rotMat*(self.pos-offset)
            yield
        if not stop and not connect[1]:
            self.stop(False)
        elif not connect[1]:
            self.stop(self.brake)

    def toPos(self, pos, speed = 1000, backwards = False, stop = True, turn = True, tolerance = 0.0, extraDist = 10.0, background=False, connect = [False, False]):
        if background:
            self.robot.addTask(self.toPosGen(pos, speed = speed, backwards = backwards, stop = stop, turn = turn, tolerance = tolerance, extraDist = extraDist, background=background, connect=connect))
        else:
            for _ in self.toPosGen(pos, speed = speed, backwards = backwards, stop = stop, turn = turn, tolerance = tolerance, extraDist = extraDist, background=background, connect=connect):
                self.robot.runTasks()
                pass
    
    def calcDir(self, pos:vec2, length, speed, offsetAngle, backwards = False, extraDist = 0.0):
        a2 = (self.robot.hub.angleRad()-offsetAngle) % (2*pi)
        pos = vec2(length + extraDist - pos.x, -pos.y)
        a1 = atan2(pos.y, pos.x) % (2*pi)
        angle = (a2 - a1 + pi) % (2*pi) - pi
        speedM = speed * minV(1-(fabs(angle)*self.turnCoeff),-1.0)**1
        if(backwards):
            speed, speedM = -speedM, -speed
        mult = 1/(fabs(angle)*0+1)
        if sign(angle) > 0:
            self.setSpeed(speed*mult, speedM*mult)
        else:
            self.setSpeed(speedM*mult, speed*mult)


    def calcSpeed(self, pos, length, speed, connect = [False, False]):
        if self.cStart == self.cFinish:
            accSpeed = speed
            deaccSpeed = speed
            
            if not connect[0]:
                accSpeed = fabs(pos.x) * self.acc + self.defspeed
            if not connect[1]:
                deaccSpeed = fabs(length - pos.x) * self.deacc + self.defspeed
        else:
            accSpeed =  (self.pos - self.cStart).length() * self.cAcc + self.defspeed
            deaccSpeed = (self.pos - self.cFinish).length() * self.cDeacc + self.defspeed
        return clamp(fabs(maxV(deaccSpeed,accSpeed)), self.defspeed ,speed)


    def rotate(self, angle, speed = 1000, background = False):
        self.rotateRad(angle/180 * pi, speed = speed, background=background)
    
    def rotateRad(self, angle, speed = 1000, background = False):
        if background:
            self.robot.addTask(self.rotateRadGen(angle, speed))
        else:
            for _ in self.rotateRadGen(angle, speed):
                self.robot.runTasks()
                pass
       
    def rotateRadGen(self, angle, speed = 1000):
        angleInit = self.robot.hub.angleRad()
        angleInitD = 0
        angleD = angleDiff(self.robot.hub.angleRad(), angle)
        if fabs(angleD) <= self.tolDiff:
            return
        while fabs(angleD) > self.accuracy:
            rspeed = self.calcSpeedR(angleD, speed, angleInitD)
            self.setSpeed(-rspeed*sign(angleD), rspeed*sign(angleD))
            self.update()
            angleInitD = angleDiff(self.robot.hub.angleRad(), angleInit)
            angleD = angleDiff(self.robot.hub.angleRad(), angle)
            
            yield
        self.stop(self.braker)

    def calcSpeedR(self, angle:float, speed:float, angleInit:float):
        rspeed = fabs(angle) * self.rdeacc + self.defspeed
        aspeed = fabs(angleInit) * self.racc + self.defspeed
        return maxV(maxV(rspeed,aspeed),speed)
    
    def circleToPos(self,pos, speed = 1000, connect = [False, False], accuracy = 0.2, backwards = False, background = False):
        if background:
            self.robot.addTask(self.circleToPosGen(pos, speed = speed, connect = connect, accuracy = accuracy, backwards = backwards))
        else:
            for _ in self.circleToPosGen(pos, speed = speed, connect = connect, accuracy = accuracy, backwards = backwards):
                self.robot.runTasks()
                pass
    
    def circleToPosGen(self, pos: vec2, speed = 1000, connect = [False, False], accuracy = 0.2, backwards = False):
        startPos = self.pos
        if accuracy == 0.2 and connect[1]:
            accuracy = 13
        while (self.pos - pos).length() > accuracy:
            angle = self.robot.hub.angleRad()
            if backwards:
                angle = angleDiff(0, angle + pi)
            
            dir = vec2(cos(angle), sin(angle))
            dx = pos.x - self.pos.x
            dy = pos.y - self.pos.y
            t=(dx*dir.x + dy*dir.y) / (2*(dy*dir.x - dx*dir.y))
            center = vec2(0.5*(self.pos.x + pos.x) - t*dy, 0.5*(pos.y + self.pos.y) + t*dx)
            radius = (pos - center).length()
            ratio = (radius-self.axle*0.5)/(radius+self.axle*0.5)
            side = sign((mat2.rotation(-angle+ 0.5*pi) * (pos-self.pos)).x)
            
            cSpeed = self.calcSpeedDis(startPos, pos, speed, connect = connect)
            if backwards:
                cSpeed = -cSpeed
                side = -side
            
            if side == 1:
                self.setSpeed(cSpeed, cSpeed*ratio)
            else:
                self.setSpeed(cSpeed*ratio, cSpeed)
            
            self.update()
            yield
        if not connect[1]:
            self.stop(self.brake)

    
    def calcSpeedDis(self, startPos: vec2, EndPos: vec2, speed: float, connect = [False, False]):
       
        disToStart = (startPos - self.pos).length()
        disToEnd = (EndPos - self.pos).length()
        rspeed = speed
        if not connect[0]:
            rspeed = disToStart * self.acc + self.defspeed
        if not connect[1]:
            rspeed = maxV(rspeed, disToEnd * self.deacc + self.defspeed)
        else:
            rspeed = maxV(rspeed, disToEnd * self.deacc*3 + self.defspeed)
        rspeed = maxV(rspeed, speed)
        return rspeed
    
    
    def bezier(self, p0:vec2, p1:vec2, p2:vec2, p3:vec2, numOfPoints = 10, speed = 500):
        points = generateBezierCurve(p0, p1, p2, p3, numOfPoints)
        self.cStart = points[0]
        self.cFinish = points[len(points)-1]
        for i in range(numOfPoints+1):
            if i == 0:
                self.toPos(points[i], tolerance=self.cTolerance)
            elif i == 1:
                self.toPos(points[i], tolerance=self.cTolerance,stop=False, speed=speed)
            elif i == numOfPoints:
                self.toPos(points[i], turn=False, speed=speed)
            else:
                self.toPos(points[i], turn = False, stop=False, tolerance=self.cTolerance, extraDist=0.0,speed=speed)
        self.cStart = self.cFinish = vec2(0,0)
    