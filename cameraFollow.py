import math
from BaseLibrary.Code.Server.Motor import*
from cv.faceDetect import Vision
# from rpi_ws281x import *
from BaseLibrary.Code.Server.servo import Servo
import time

cv = Vision()
servo = Servo()

try:
    h_angle = 90
    v_angle = 90
    servo.setServoPwm('0', h_angle)  # Horizontal, 0 is left, 180 is right
    servo.setServoPwm('1', v_angle)  # Vertical, 0 is down, 180 is up
    # Main camera adjustment loop
    while True:
        (x, y, w, h) = cv.get_bounding_box()
        if w != 0 and h != 0:
            relativeX = cv.get_x_center() - x - w / 2  # Left (+), Right (-)
            relativeY = cv.get_y_center() - y - h / 2  # Up (+), Down (-)
            h_angle += cv.get_horizontal_angle(relativeX)
            v_angle += cv.get_vertical_angle(relativeY)
        else:
            if h_angle != 90:
                h_angle += 1 if h_angle < 90 else -1
            if v_angle != 120:
                v_angle += 1 if v_angle < 120 else -1
        if h_angle < 20:
            h_angle = 20
        elif h_angle > 160:
            h_angle = 160
        if v_angle < 90:
            v_angle = 90
        elif v_angle > 150:
            v_angle = 150

        # servo.setServoPwm('0', h_angle)
        # servo.setServoPwm('1', v_angle)
        print(f"{h_angle}, {v_angle}")


except KeyboardInterrupt:
    cv.destroy()
    servo.setServoPwm('0', 90)
    servo.setServoPwm('1', 90)
