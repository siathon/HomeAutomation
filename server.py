from time import sleep

from Devices import Lamp

l = Lamp('myRoom')
print(l)
if l.getState():
    l.turnOFF()
    print(l)
else:
    l.turnON()
    print(l)
