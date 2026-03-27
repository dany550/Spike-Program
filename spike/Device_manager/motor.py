from Device_manager.maths import *
from Device_manager.robot import Rdevice, Robot
from pybricks.parameters import Port
from pybricks.pupdevices import Motor
#add settings

class motor(Rdevice):
    def __init__(self, port: Port, robot: Robot):
        super().__init__(port, robot)
        self.reverse = False
        self.offset = 0
        self.switchDir = False
        self.m_motor = Motor(port)
        self.deltaAngle = 0
        self.lastAngle = self.angleRad()
        self.tolDiff = pi/90
    
    def setDefAngle(self, angle = 0):
        self.offset = angle/180*pi + self.angleRad()
    
    def setSpeed(self, speed: float):
        if self.reverse:
            self.m_motor.run(-speed)
        else:
            self.m_motor.run(speed)
        pass

    def stop(self):
        self.m_motor.stop()
        pass
    
    def Update(self):
        if self.reverse:
            self.deltaAngle = -self.angleRad() + self.lastAngle
        else:
            self.deltaAngle = self.angleRad() - self.lastAngle
        self.lastAngle = self.angleRad()
        pass
    
    def brake(self):
        self.m_motor.brake()
        pass
    
    def hold(self):
        self.m_motor.hold()
        pass
    
    def angle(self):
        return float(self.m_motor.angle()) - self.offset/pi * 180
    
    def angleRad(self):
        return float(self.m_motor.angle())/180 * pi - self.offset
    
    def turnMotorRad(self, angle:float, speed = 1000, background = False, simple = False, time = 0):
        if background:
            self.robot.addTask(self.turnMotorRadGen(angle, speed = speed, simple=simple, time = time))
        else:
            for _ in self.turnMotorRadGen(angle, speed = speed, simple=simple, time = time):
                self.robot.runTasks()
                pass
    
    def turnMotorRadGen(self, angle:float, speed = 1000, simple = False, time = 0):
        dif = angleDiff(self.angleRad(), angle, simple=simple)
        doTime = True
        if time == 0:
            doTime = False

        while fabs(dif) > self.tolDiff*2 and (time > 0 or not doTime):
            dif = angleDiff(self.angleRad(), angle, simple=simple)
            self.setSpeed(sign(dif) * clamp(speed*abs(dif)*0.5,110,200))
            time -= 1
            yield
        self.hold()
        if time == 0:
            print("motor failed to reach target angle in time")

    def turnMotor(self, angle:float, speed = 1000, background = False, simple = False, time = 0):
        self.turnMotorRad(angle/180 * pi, speed=speed, background=background, simple=simple, time=time)