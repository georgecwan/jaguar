from BaseLibrary.Code.Server.Motor import*
from cv.faceDetect import Vision
import time

cv = Vision()
PWM = Motor()


try:
    idleCount = 0
    m1i = m2i = m3i = m4i = 0
    # Main robot loop goes here
    while True:
        (x, y, w, h) = cv.get_bounding_box()
        # print(f"{x}, {y}, {w}, {h}")
        relativeX = cv.get_x_center() - x - w / 2
        m1 = m2 = m3 = m4 = 0
        if w != 0 and abs(relativeX) >= 75:
            if relativeX < 0:
                print("Turning right")
                m1, m2, m3, m4 = m1 + 500, m2 + 500, m3 - 500, m4 - 500
            elif relativeX > 0:
                print("Turning left")
                m1, m2, m3, m4 = m1 - 500, m2 - 500, m3 + 500, m4 + 500

        if w > 100 and h > 100:
            # Too close
            print("Going backwards")
            m1, m2, m3, m4 = m1 - 800, m2 - 800, m3 - 800, m4 - 800
        elif 0 < w < 60 and 0 < h < 60:
            # Too far
            print("Going forwards")
            m1, m2, m3, m4 = m1 + 800, m2 + 800, m3 + 800, m4 + 800
        if m1 == m2 == m3 == m4 == 0 and idleCount < 5:
            print("No movement")
            idleCount += 1
            PWM.setMotorModel(m1i, m2i, m3i, m4i)
        else:
            m1i, m2i, m3i, m4i = m1, m2, m3, m4
            idleCount = 0
            PWM.setMotorModel(m1, m2, m3, m4)

except KeyboardInterrupt:
    PWM.setMotorModel(0, 0, 0, 0)
    cv.destroy()


    