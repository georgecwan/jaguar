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
        relativeX = cv.get_x_center() - x - w / 2
        m1 = m2 = m3 = m4 = 0
        if abs(relativeX) >= 100:
            if relativeX < 0:
                print("Turning right")
                m1, m2, m3, m4 = m1 + 200, m2 + 200, m3 - 200, m4 - 200
            elif relativeX > 0:
                print("Turning left")
                m1, m2, m3, m4 = m1 - 200, m2 - 200, m3 + 200, m4 + 200

        if w > 120 and h > 120:
            # Too close
            print("Going backwards")
            m1, m2, m3, m4 = m1 - 800, m2 - 800, m3 - 800, m4 - 800
        elif 0 < w < 80 and 0 < h < 80:
            # Too far
            print("Going forwards")
            m1, m2, m3, m4 = m1 + 800, m2 + 800, m3 + 800, m4 + 800
        else:
            # Stop
            print("No forwards/backwards movement")
        PWM.setMotorModel(m1, m2, m3, m4)

except KeyboardInterrupt:
    PWM.setMotorModel(0, 0, 0, 0)
    cv.destroy()


    