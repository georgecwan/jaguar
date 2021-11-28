from PCA9685 import PCA9685
import RPi.GPIO as GPIO
import time


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


# trigger pin, echo pin
ultrasonicL = Ultrasonic(9, 25)
ultrasonicR = Ultrasonic(11, 8)
ultrasonicM = Ultrasonic(27, 22)

# Main program logic follows:
if __name__ == '__main__':
    print('Program is starting ... ')
    try:
        while True:
            L = ultrasonicL.get_distance()
            R = ultrasonicR.get_distance()
            M = ultrasonicM.get_distance()
            print(f"Left: {L}, Right: {R}, Middle: {M}")
            time.sleep(0.2)

    # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
    except KeyboardInterrupt:
        pass
