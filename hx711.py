import RPi.GPIO as GPIO
import time


class HX711:

    """711取值"""

    def __init__(self, SCK, DT):
        GPIO.setup(DT, GPIO.IN)
        GPIO.setup(SCK, GPIO.OUT, initial=0)
        self.DT = DT
        self.SCK = SCK

    def getdv(self):
        d = 0
        while GPIO.input(self.DT) == 1:
            pass
        for i in range(24):
            GPIO.output(self.SCK, 1)
            d = d << 1
            GPIO.output(self.SCK, 0)
            if GPIO.input(self.DT) == 0:
                d = d+1
        GPIO.output(self.SCK, 1)
        time.sleep(0.001)
        GPIO.output(self.SCK, 0)
        d = d ^ 0x800000
        return d
