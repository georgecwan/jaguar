from BaseLibrary.Code.Server.Motor import*
import time

PWM = Motor()


try:
    PWM.setMotorModel(1000, 1000, 1000, 1000)  # Forward
    print("The car is going forwards")
    a = input()
    PWM.setMotorModel(0, 0, 0, 0)
    b = input()
    PWM.setMotorModel(-1000, -1000, -1000, -1000)  # Back
    print("The car is going backwards")
    c = input()
    PWM.setMotorModel(0, 0, 0, 0)
    b = input()
    PWM.setMotorModel(-1900, -1500, 2000, 2000)  # Left
    print("The car is turning left")
    d = input()
    PWM.setMotorModel(0, 0, 0, 0)
    b = input()
    PWM.setMotorModel(2000, 2000, -2500, -1500)  # Right
    print("The car is turning right")
    e = input()
    PWM.setMotorModel(0, 0, 0, 0)

except KeyboardInterrupt:
    PWM.setMotorModel(0, 0, 0, 0)
    cv.destroy()
