from pybricks.hubs import PrimeHub
from imgs import *
from spike_lib.screen import *
from test import *
from spike_lib.robot import hub

print("Starting program")
menu = Screen(hub())
menu.addPage(Page(hallo, icon=wroimg, image=arrow, delta=110))


menu.start()
while True:
    menu.update()


