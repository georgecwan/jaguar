from BaseLibrary.Code.Server.Motor import*
from cv.faceDetect import Vision
from BaseLibrary.Code.Server.servo import Servo
from multiprocessing.shared_memory import SharedMemory
import threading
import RPi.GPIO as GPIO
import Voice

# This variable determines what the robot will do
# 0 = stop
# 1 = follow human
# 2 = spin
# 3 = buzzer
# mode is a shared memory buffer and index 0 contains the mode
# Access and modify with mode[0]
shared_mode = SharedMemory('mode', True, 1)
mode = shared_mode.buf
mode[0] = 1

# Voice class
voice = Voice.Voice('mode')

# Spawn a new thread to run the voice recognition
# This thread will run until the program is closed
threading.Thread(target=voice.start).start()

# Variables for motors, servos, and CV
cv = Vision()
PWM = Motor()
servo = Servo()
motorValues = (
    ((550, 550, 2800, 2800), (600, 600, 1600, 1600), (600, 600, 1300, 1300), (660, 660, 600, 600), (1510, 1510, 600, 600), (2000, 2000, 600, 600), (2800, 2800, 550, 550)),  # 0 = Forward
    ((-1900, -1500, 2000, 2000), (-1900, -1500, 2000, 2000), (-1900, -1500, 2000, 2000), (0, 0, 0, 0), (2000, 2000, -2500, -1500), (2000, 2000, -2500, -1500), (2000, 2000, -2500, -1500)),  # 1 = Stationary
    ((-2800, -2800, -550, -550), (-2000, -2000, -600, -600), (-1510, -1510, -600, -600), (-660, -660, -600, -600), (-600, -600, -1300, -1300), (-600, -600, -1600, -1600), (-550, -550, -2800, -2800))  # 2 = Backward (Directions are mirrored)
)  # 0 = extreme left, 1 = very left, 2 = slight left, 3 = straight, 4 = slight right, 5 = very right, 6 = extreme right


# Variables for Buzzer
GPIO.setwarnings(False)
Buzzer_Pin = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(Buzzer_Pin,GPIO.OUT)

try:
    delay = 0
    h_angle = 90
    v_angle = 120
    servo.setServoPwm('0', h_angle)  # Horizontal, 0 is left, 180 is right
    servo.setServoPwm('1', v_angle)  # Vertical, 0 is down, 180 is up
    absoluteX = 90
    idleCount = 0
    idleTurn = 5
    dz = 0  # Forward/backwards values
    dx = 0  # Turning Values

    # Main robot loop goes here
    while True:
        if mode[0] == 1:
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
            elif delay > 5:
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
            if (w > 90 and h > 90) or v_angle > 155:
                # Too close
                print("Going backwards")
                dz = 2
                idleCount = 0
            elif 0 < w < 70 and 0 < h < 70:
                # Too far
                print("Going forwards")
                dz = 0
                idleCount = 0
            elif idleCount < 2:
                print("Idling")
                idleCount += 1
            else:
                print("No f/b movement")
                dz = 1

            if w != 0 and h != 0 and abs(absoluteX - 90) > 0:
                if absoluteX > 110:
                    print("Turning eright")
                    dx = 6
                elif absoluteX < 70:
                    print("Turning eleft")
                    dx = 0
                elif absoluteX > 100:
                    print("Turning vright")
                    dx = 5
                elif absoluteX < 80:
                    print("Turning vleft")
                    dx = 1
                elif absoluteX > 90:
                    print("Turning sright")
                    dx = 4
                elif absoluteX < 90:
                    print("Turning sleft")
                    dx = 2
            else:
                print("No turning")
                dx = 3

            m1, m2, m3, m4 = motorValues[dz][dx]
            PWM.setMotorModel(m1, m2, m3, m4)

        elif mode[0] == 0:
            # Stop and do nothing
            PWM.setMotorModel(0, 0, 0, 0)
            time.sleep(5)

        elif mode[0] == 2:
            # Turn for one second, then return to idle
            PWM.setMotorModel(2000, 2000, -1500, -1500)
            time.sleep(1)
            PWM.setMotorModel(0, 0, 0, 0)
            mode[0] = 0

        elif mode[0] == 3:
            # Stop and buzz for 3 seconds
            PWM.setMotorModel(0, 0, 0, 0)
            GPIO.output(Buzzer_Pin, True)
            time.sleep(3)
            GPIO.output(Buzzer_Pin, False)
            mode[0] = 0



except KeyboardInterrupt:
    # Reset motors and servos on completion
    PWM.setMotorModel(0, 0, 0, 0)
    cv.destroy()
    servo.setServoPwm('0', 90)
    servo.setServoPwm('1', 90)
    threading.Thread(target=voice.stop()).start()
    time.sleep(3)
    shared_mode.unlink()
