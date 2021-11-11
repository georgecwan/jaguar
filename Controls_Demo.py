from BaseLibrary.Code.Server.Motor import*
import time

PWM = Motor()


try:
    PWM.setMotorModel(1000, 1000, 1000, 1000)
    a = input()
    PWM.setMotorModel(0, 0, 0, 0)
    b = input()
    PWM.setMotorModel(-1000, -1000, -1000, -1000)
    c = input()


except KeyboardInterrupt:
    PWM.setMotorModel(0, 0, 0, 0)
    cv.destroy()
