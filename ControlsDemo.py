from BaseLibrary.Code.Server.Motor import *
import time

PWM = Motor()


try:
    PWM.setMotorModel(1000, 1000, 1000, 1000)
    print("The car is going forwards")
    input()
    PWM.setMotorModel(0, 0, 0, 0)
    input()
    PWM.setMotorModel(-1000, -1000, -1000, -1000)
    print("The car is going backwards")
    input()
    PWM.setMotorModel(0, 0, 0, 0)
    input()
    PWM.setMotorModel(-1900, -1500, 2000, 2000)  # Left
    print("The car is turning left")
    input()
    PWM.setMotorModel(0, 0, 0, 0)
    input()
    PWM.setMotorModel(2000, 2000, -2500, -1500)  # Right
    print("The car is turning right")
    input()
    PWM.setMotorModel(0, 0, 0, 0)

except KeyboardInterrupt:
    PWM.setMotorModel(0, 0, 0, 0)

