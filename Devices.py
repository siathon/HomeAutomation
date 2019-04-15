from spidev import SpiDev
from time import sleep

class Lamp():
    def __init__(self, nm):
        self.__name = nm
        self.spi = SpiDev()
        self.spi.open(0, 0)
        self.spi.max_speed_hz = 1000000
        sleep(1)
        self.__status = self.getState()

    def turnON(self):
        print('Turning lamp ON...', end='')
        self.spi.xfer([0x55])
        sleep(1)
        st = self.getState()

        if st:
            print('Done.')
        else:
            print('Failed!')
        return st

    def turnOFF(self):
        print('Turning lamp OFF...', end='')
        self.spi.xfer([0xAA])
        sleep(1)
        st = self.getState()

        if not st:
            print('Done.')
        else:
            print('Failed!')
        return not st

    def getState(self):
        self.spi.xfer([0x3F])
        sleep(1)
        st = self.spi.readbytes(1)[0]
        sleep(1)

        if st == 0x55:
            self.__status = True
            return self.__status
        elif st == 0xAA:
            self.__status = False
            return self.__status

    def __str__(self):
        if self.__status:
            st = 'ON'
        else:
            st = 'OFF'
        return "{}'s Lamp is {}".format(self.__name, st)
