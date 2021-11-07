# from BaseLibrary.Code.Server.Motor import *
from cv.faceDetect import Vision
import time

cv = Vision()

# Main robot loop goes here
while True:
    (x, y, w, h) = cv.get_bounding_box();
    print(f"{x}, {y}, {w}, {h}")
    