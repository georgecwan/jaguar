from BaseLibrary.Code.Server.Motor import *
import time

PWM = Motor()


try:
    while True:
        a = input()
        if a == 'w':
            PWM.setMotorModel(1000, 1000, 1000, 1000)
        elif a == 'a':
            PWM.setMotorModel(-1900, -1500, 2000, 2000)
        elif a == 's':
            PWM.setMotorModel(-1000, -1000, -1000, -1000)
        elif a == 'd':
            PWM.setMotorModel(2000, 2000, -2500, -1500)
        else:
            PWM.setMotorModel(0, 0, 0, 0)

except KeyboardInterrupt:
    PWM.setMotorModel(0, 0, 0, 0)

