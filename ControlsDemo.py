from BaseLibrary.Code.Server.Motor import *
import time

PWM = Motor()


try:
    while True:
        a = input()
        if a == 'w':
            PWM.setMotorModel(1100, 1100, 1000, 1000)
        elif a == 'a':
            PWM.setMotorModel(-1900, -1500, 2000, 2000)
        elif a == 's':
            PWM.setMotorModel(-1450, -1450, -1450, -1450)
        elif a == 'd':
            PWM.setMotorModel(2000, 2000, -2500, -1500)
        elif a == 'q':
            PWM.setMotorModel(600, 600, 1300, 1300)  # slight left
        elif a == 'e':
            PWM.setMotorModel(1510, 1510, 600, 600)  # slight right
        elif a == 'j':
            PWM.setMotorModel(600, 600, 1600, 1600)  # more left
        elif a == 'l':
            PWM.setMotorModel(2000, 2000, 600, 600)  # more right
        elif a == 'z':
            PWM.setMotorModel(2000, 2000, -2500, -1500)
            time.sleep(0.1)
            PWM.setMotorModel(1450, 1450, 1450, 1450)
            time.sleep(0.3)
            PWM.setMotorModel(-1900, -1500, 2000, 2000)
            time.sleep(0.1)
            PWM.setMotorModel(1450, 1450, 1450, 1450)
            time.sleep(0.3)
            PWM.setMotorModel(2000, 2000, -2500, -1500)
        else:
            PWM.setMotorModel(0, 0, 0, 0)

except KeyboardInterrupt:
    PWM.setMotorModel(0, 0, 0, 0)
