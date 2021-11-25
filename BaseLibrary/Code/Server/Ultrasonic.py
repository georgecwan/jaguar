import time
from Motor import *
import RPi.GPIO as GPIO
from servo import *
from PCA9685 import PCA9685


class Ultrasonic:
    def __init__(self, trigger_pin, echo_pin,):
        GPIO.setwarnings(False)
        self.trigger_pin = trigger_pin
        self.echo_pin = echo_pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.trigger_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)

    def send_trigger_pulse(self):
        GPIO.output(self.trigger_pin, True)
        time.sleep(0.00015)
        GPIO.output(self.trigger_pin, False)

    def wait_for_echo(self, value, timeout):
        count = timeout
        while GPIO.input(self.echo_pin) != value and count > 0:
            count = count-1

    def get_distance(self):
        distance_cm = [0, 0, 0, 0, 0]
        for i in range(3):
            self.send_trigger_pulse()
            self.wait_for_echo(True, 10000)
            start = time.time()
            self.wait_for_echo(False, 10000)
            finish = time.time()
            pulse_len = finish-start
            distance_cm[i] = pulse_len/0.000058
        distance_cm = sorted(distance_cm)
        return int(distance_cm[2])

def run_motor(PWM, L, M, R):
    if (L < 30 and M < 30 and R < 30) or M < 30:
        self.PWM.setMotorModel(-1450, -1450, -1450, -1450)
        time.sleep(0.1)
        if L < R:
            self.PWM.setMotorModel(1450, 1450, -1450, -1450)
        else:
            self.PWM.setMotorModel(-1450, -1450, 1450, 1450)
    elif L < 30 and M < 30:
        PWM.setMotorModel(1500, 1500, -1500, -1500)
    elif R < 30 and M < 30:
        PWM.setMotorModel(-1500, -1500, 1500, 1500)
    elif L < 20:
        PWM.setMotorModel(2000, 2000, -500, -500)
        if L < 10:
            PWM.setMotorModel(1500, 1500, -1000, -1000)
    elif R < 20:
        PWM.setMotorModel(-500, -500, 2000, 2000)
        if R < 10:
            PWM.setMotorModel(-1500, -1500, 1500, 1500)
    else:
        self.PWM.setMotorModel(600, 600, 600, 600)

# trigger pin, echo pin
ultrasonicL = Ultrasonic(9, 25)
ultrasonicR = Ultrasonic(11, 8)
ultrasonicM = Ultrasonic(27, 22)

# Main program logic follows:
if __name__ == '__main__':
    print('Program is starting ... ')
    PWM = Motor()
    try:
        while True:
            L = ultrasonicL.get_distance()
            R = ultrasonicR.get_distance()
            M = ultrasonicM.get_distance()
            run_motor(PWM, L, M, R)
            time.sleep(0.2)

    # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
    except KeyboardInterrupt:
        PWM.setMotorModel(0, 0, 0, 0)
