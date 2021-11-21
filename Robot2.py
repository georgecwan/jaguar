import math
from BaseLibrary.Code.Server.Motor import*
from cv.faceDetect import Vision
# from rpi_ws281x import *
from BaseLibrary.Code.Server.servo import Servo
import time

cv = Vision()
PWM = Motor()
servo = Servo()

try:
    delay = 0
    h_angle = 90
    v_angle = 120
    servo.setServoPwm('0', h_angle)  # Horizontal, 0 is left, 180 is right
    servo.setServoPwm('1', v_angle)  # Vertical, 0 is down, 180 is up
    absoluteX = 90
    idleCount = 0
    idleTurn = 5
    m1i = m2i = m3i = m4i = 0  # Forward/backwards values
    m1t = m2t = m3t = m4t = 0  # Turning Values

    # Main robot loop goes here
    while True:
        # Servo Adjustment code
        (x, y, w, h) = cv.get_bounding_box()
        if (x, y, w, h) == (0, 0, 0, 0):
            relativeX = 0
            relativeY = 0
            absoluteX = 90
            print("No face detected")
        else:
            relativeX = cv.get_x_center() - x - w / 2  # Left (+), Right (-)
            relativeY = cv.get_y_center() - y - h / 2  # Up (+), Down (-)
        if w != 0 and h != 0 and delay == 0:
            temp = h_angle
            h_angle -= cv.get_horizontal_angle(relativeX) / 2.5
            v_angle += cv.get_vertical_angle(relativeY) / 2.5
            delay += 1
            absoluteX = temp - cv.get_horizontal_angle(relativeX)
        elif w != 0 and h != 0:
            delay = 0
        elif delay > 10:
            if h_angle != 90:
                if h_angle >= 135:
                    idleTurn = -5
                if h_angle <= 45:
                    idleTurn = 5
                h_angle += idleTurn
            if v_angle != 120:
                v_angle += 1 if v_angle < 120 else -1
        else:
            delay += 1

        if h_angle < 20:
            h_angle = 20
        elif h_angle > 160:
            h_angle = 160
        if v_angle < 90:
            v_angle = 90
        elif v_angle > 150:
            v_angle = 150

        servo.setServoPwm('0', h_angle)
        servo.setServoPwm('1', v_angle)

        # Motor code
        if (w > 80 and h > 80) or v_angle > 155:
            # Too close
            print("Going backwards")
            m1i, m2i, m3i, m4i = -600, -600, -600, -600
            idleCount = 0
        elif 0 < w < 70 and 0 < h < 70:
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

        if w != 0 and h != 0 and abs(absoluteX - 90) > 0 and not (m1i == m2i == m3i == m4i == 0):
            if absoluteX > 110:
                print("Turning eright")
                m1t, m2t, m3t, m4t = 1650, 1650, 0, 0
            elif absoluteX < 70:
                print("Turning eleft")
                m1t, m2t, m3t, m4t = 0, 0, 1200, 1200
            elif absoluteX > 100:
                print("Turning vright")
                m1t, m2t, m3t, m4t = 1400, 1400, 0, 0
            elif absoluteX < 80:
                print("Turning vleft")
                m1t, m2t, m3t, m4t = 0, 0, 1000, 1000
            elif absoluteX > 90:
                print("Turning sright")
                m1t, m2t, m3t, m4t = 910, 910, 0, 0
            elif absoluteX < 90:
                print("Turning sleft")
                m1t, m2t, m3t, m4t = 0, 0, 700, 700
        elif m1i == m2i == m3i == m4i == 0:
            if absoluteX > 80:
                print("Turning right in place")
                m1t, m2t, m3t, m4t = 2000, 2000, -2500, -1500
            elif absoluteX < 100:
                print("Turning left in place")
                m1t, m2t, m3t, m4t = -1900, -1500, 2000, 2000
        else:
            print("No turning")
            m1t = m2t = m3t = m4t = 0

        PWM.setMotorModel(m1t + m1i, m2t + m2i, m3t + m3i, m4t + m4i)


except KeyboardInterrupt:
    PWM.setMotorModel(0, 0, 0, 0)
    cv.destroy()
    servo.setServoPwm('0', 90)
    servo.setServoPwm('1', 90)
