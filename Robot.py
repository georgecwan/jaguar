from BaseLibrary.Code.Server.Motor import*
from cv.faceDetect import Vision
import time

cv = Vision()
PWM = Motor()


try:
    # Main robot loop goes here
    while True:
        (x, y, w, h) = cv.get_bounding_box()
        # print(f"{x}, {y}, {w}, {h}")
        if w > 0 and h > 0:
            if w > 120 and h > 120:
                # Moves backward
                print("Going backwards")
                PWM.setMotorModel(-1000, -1000, -1000, -1000)
            elif w < 80 and h < 80:
                # Moves forward
                print("Going forwards")
                PWM.setMotorModel(1000, 1000, 1000, 1000)
            else:
                # Stop
                print("Staying still")
                PWM.setMotorModel(0, 0, 0, 0)
except KeyboardInterrupt:
    PWM.destroy()
    cv.destroy()


    