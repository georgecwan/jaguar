# This program is to be spawned by the main robot class.
# It runs the wake word detection and the speech recognition.
import subprocess
import time
from multiprocessing.shared_memory import SharedMemory

class Voice:
    def __init__(self, shared_memory_name):
        self.shared_mode = SharedMemory(name=shared_memory_name, create=False)
        self.state = False
        self.script_helper = None
        self.wake_wait = None

    def start(self):
        # Start the wake word detection and the speech recognition.
        self.state = True
        self.run()

    def run(self):
        # Uses the voice2json software to listen for the wake word
        while self.state:
            # These two commands are blocking
            # The first command waits for a wake word then exits
            # The second command listens for the actual command, parses it, and exits
            self.wait_wait = subprocess.Popen(["/usr/bin/voice2json", "-p", "/home/pi/.local/share/voice2json/en-us_kaldi-zamia", "wait-wake", "--exit-count", "1"]).wait()
            
            # Tell the car to stop while the system is running
            self.shared_mode.buf[0] = 0
            self.script_helper = subprocess.Popen(["./voice_helper.sh"], stdout=subprocess.PIPE, universal_newlines=True)

            # Read the output of the speech recognition
            for stdout_line in iter(self.script_helper.stdout.readline, ""):
                if "Command: " in stdout_line:
                    func_name = stdout_line.split()[1]
                    if func_name == "SitDown":
                        self.shared_mode.buf[0] = 0
                    elif func_name == "Follow":
                        self.shared_mode.buf[0] = 1
                    elif func_name == "Spin":
                        self.shared_mode.buf[0] = 2
                    elif func_name == "Speak":
                        self.shared_mode.buf[0] = 3
            self.script_helper.stdout.close()

    def stop(self):
        self.state = False
        if self.script_helper is not None:
            self.script_helper.terminate()
        if self.wake_wait is not None:
            self.wake_wait.terminate()
        time.sleep(3)
        self.shared_mode.close()


if __name__ == "__main__":
    script_helper = subprocess.Popen(["./voice_helper.sh"], stdout=subprocess.PIPE, universal_newlines=True)
    for stdout_line in iter(script_helper.stdout.readline, ""):
        if "Command: " in stdout_line:
            print(stdout_line.split()[1])
