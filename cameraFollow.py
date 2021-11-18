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
    v_angle = 120
    servo.setServoPwm('0', h_angle)  # Horizontal, 0 is left, 180 is right
    servo.setServoPwm('1', v_angle)  # Vertical, 0 is down, 80 is up
    # Main camera adjustment loop
    while True:
        (x, y, w, h) = cv.get_bounding_box()
        relativeX = cv.get_x_center() - x - w / 2
        relativeY = cv.get_y_center() - y - h / 2
        h_angle += cv.get_horizontal_angle(relativeX)
        v_angle += cv.get_vertical_angle(relativeY)
        # servo.setServoPwm('0', h_angle)
        # servo.setServoPwm('1', v_angle)
        print(f"{h_angle}, {v_angle}")


except KeyboardInterrupt:
    cv.destroy()
    servo.setServoPwm('0', 90)
    servo.setServoPwm('1', 90)
