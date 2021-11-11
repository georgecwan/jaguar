from BaseLibrary.Code.Server.Motor import*
from cv.faceDetect import Vision
from rpi_ws281x import *
from BaseLibrary.Code.Server.Led import Led
import time

cv = Vision()
PWM = Motor()
led = Led()


try:
    idleCount = 0
    m1i = m2i = m3i = m4i = 0  # Forward/backwards values
    # Main robot loop goes here
    while True:
        (x, y, w, h) = cv.get_bounding_box()
        # print(f"{x}, {y}, {w}, {h}")
        relativeX = 160 - x - w / 2
        m1t = m2t = m3t = m4t = 0  # Turning Values
        if (x, y, w, h) == (0, 0, 0, 0):
            print("No face detected")
            
        if w != 0 and abs(relativeX) >= 10:
            if relativeX < 0:
                print("Turning right")
                m1t, m2t, m3t, m4t = 600, 600, 0, 0
            elif relativeX > 0:
                print("Turning left")
                m1t, m2t, m3t, m4t = 0, 0, 600, 600

        if w > 50 and h > 50:
            # Too close
            print("Going backwards")
            m1i, m2i, m3i, m4i = -600, -600, -600, -600
            led.colorWipe(led.strip, Color(255, 0, 0))
            idleCount = 0
        elif 0 < w < 30 and 0 < h < 30:
            # Too far
            print("Going forwards")
            m1i, m2i, m3i, m4i = 600, 600, 600, 600
            led.colorWipe(led.strip, Color(0, 255, 0))
            idleCount = 0
        # elif idleCount < 2:
        #     print("Idling")
        #     idleCount += 1
        #     led.colorWipe(led.strip, Color(255, 255, 255))
        else:
            print("No f/b movement")
            m1i, m2i, m3i, m4i = 0, 0, 0, 0
            led.colorWipe(led.strip, Color(0, 0, 255))

        PWM.setMotorModel(m1t + m1i, m2t + m2i, m3t + m3i, m4t + m4i)

except KeyboardInterrupt:
    PWM.setMotorModel(0, 0, 0, 0)
    cv.destroy()
    led.colorWipe(led.strip, Color(0, 0, 0), 10)
