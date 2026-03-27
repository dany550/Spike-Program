from pybricks.parameters import *
from pybricks.pupdevices import *
from pybricks.hubs import PrimeHub
from pybricks.tools import *
from Device_manager.maths import *
from Device_manager.hub import Hub

class Robot:
    def __init__(self):
        self.hub = Hub()
        self.devices = []
        #multitasking
        self.tasks = []
    
    def isTasksRunning(self, numOfTasks = 0):
        if len(self.tasks) > numOfTasks:
            return True
        return False
    
    def waitForTasks(self, numOfTasks = 0):
        while self.isTasksRunning(numOfTasks = numOfTasks):
            self.runTasks()
    
    def stopTasks(self):
        self.tasks = []
    
    def addTask(self, gen):
        self.tasks.append(gen)
    
    def runTasks(self):
        for task in self.tasks[:]:
            try:
                next(task)
            except StopIteration:
                self.tasks.remove(task)
    
    def addDevice(self, device):
        self.devices.append(device)


class Rdevice:
    def __init__(self, port: Port, robot: Robot):
        self.port = port
        self.robot = robot
        self.robot.addDevice(self)

    def stop(self):
        pass
