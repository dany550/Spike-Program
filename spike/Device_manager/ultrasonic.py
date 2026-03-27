from Device_manager.maths import *
from Device_manager.robot import Rdevice, Robot
from pybricks.parameters import Port
from pybricks.pupdevices import UltrasonicSensor

class Ultrasonic(Rdevice):
    def __init__(self, port: Port, robot: Robot):
        super().__init__(port, robot)
        self.m_sensor = UltrasonicSensor(port)
        
    def __repr__(self):
        return f"Ultrasonic(port={self.port}, distance={self.distance()})"

    def distance(self):
        return self.m_sensor.distance()/10