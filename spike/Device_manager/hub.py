from pybricks.hubs import PrimeHub
from pybricks.parameters import Button, Axis, Color
from Device_manager.maths import pi

class Hub:
    def __init__(self):
        self.m_hub = PrimeHub()
        self.angleOffset = 0
        self.resetAngle()
        self.setOffButton(Button.BLUETOOTH)
        self.switch = False
    def addOffset(self, offset):
        self.angleOffset += offset    
    
    def angle(self):
        if self.switch:
            return - (self.m_hub.imu.rotation(Axis.Z) - self.angleOffset)
        return self.m_hub.imu.rotation(Axis.Z) - self.angleOffset
    
    def angleRad(self):
        if self.switch:
            return -(self.m_hub.imu.rotation(Axis.Z) - self.angleOffset) / 180 * pi
        return (self.m_hub.imu.rotation(Axis.Z) - self.angleOffset) / 180 * pi
    
    def resetAngle(self):
        self.angleOffset = self.m_hub.imu.rotation(Axis.Z)
        
    def pixel(self, x, y, brightness=100):
        self.m_hub.display.pixel(y, x, brightness) #??? why swapped?
    
    def beep(self, freq, duration):
        self.m_hub.speaker.beep(freq, duration)
    
    def setVolume(self, volume):
        self.m_hub.speaker.volume(volume)
    
    def notes(self, notes, tempo=120):
        self.m_hub.speaker.play_notes(notes, tempo)
    
    def isButtonPressed(self, button: Button):
        return True if button in self.m_hub.buttons.pressed() else False
    
    def setOffButton(self, button: Button):
        self.m_hub.system.set_stop_button(button)
    
    def color(self, color: Color):
        self.m_hub.light.on(color)
    
    def colorAnimate(self, colors, duration=100):
        self.m_hub.light.animate(colors, duration)
    
    def animate(self, animation, delta):
        self.m_hub.display.animate(animation, delta)

    def image(self, image):
        self.m_hub.display.icon(image)

    def clear(self):
        self.m_hub.display.off()