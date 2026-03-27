def play(notes,  mult = 1):
    drive.robot.hub.setVolume(1000)
    for freq, duration in notes:
        drive.robot.hub.beep(freq, duration * mult)
        #wait(duration)
        
def rotate():
    drive.robot.lM.setSpeed(100)
    drive.robot.rM.setSpeed(-100)
    play(funkytown, 1)