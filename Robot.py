from BaseLibrary.Code.Server.Motor import*
from cv.faceDetect import Vision
from BaseLibrary.Code.Server.servo import Servo
import time

cv = Vision()
PWM = Motor()
servo = Servo()

try:
    servo.setServoPwm('0', 90)
    servo.setServoPwm('1', 110)
    idleCount = 0
    m1i = m2i = m3i = m4i = 0  # Forward/backwards values
    m1t = m2t = m3t = m4t = 0  # Turning Values
    # Main robot loop goes here
    while True:
        (x, y, w, h) = cv.get_bounding_box()
        # print(f"{x}, {y}, {w}, {h}")
        relativeX = cv.get_x_center() - x - w / 2
        if (x, y, w, h) == (0, 0, 0, 0):
            print("No face detected")

        if w != 0 and abs(relativeX) >= 20:
            if relativeX < 0:
                print("Turning right")
                m1t, m2t, m3t, m4t = 600, 600, 0, 0
            elif relativeX > 0:
                print("Turning left")
                m1t, m2t, m3t, m4t = 0, 0, 600, 600
        else:
            print("No turning")
            m1t = m2t = m3t = m4t = 0

        if w > 100 and h > 100:
            # Too close
            print("Going backwards")
            m1i, m2i, m3i, m4i = -600, -600, -600, -600
            idleCount = 0
        elif 0 < w < 80 and 0 < h < 80:
            # Too far
            print("Going forwards")
            m1i, m2i, m3i, m4i = 600, 600, 600, 600
            idleCount = 0
        elif idleCount < 2:
            print("Idling")
            idleCount += 1
        else:
            print("No f/b movement")
            m1i, m2i, m3i, m4i = 0, 0, 0, 0

        PWM.setMotorModel(m1t + m1i, m2t + m2i, m3t + m3i, m4t + m4i)

except KeyboardInterrupt:
    PWM.setMotorModel(0, 0, 0, 0)
    cv.destroy()
    servo.setServoPwm('0',90)
    servo.setServoPwm('1',90)


    
