# This program is to be spawned by the main robot class.
# It runs the wake word detection and the speech recognition.
import subprocess
import time
from multiprocessing.shared_memory import SharedMemory

class Voice:
    def __init__(self, shared_memory_name):
        self.shared_mode = SharedMemory(name=shared_memory_name, create=False)
        self.script_helper = None

    def start(self):
        # Start the wake word detection and the speech recognition.
        self.run()

    def run(self):
            self.script_helper = subprocess.Popen(["./voice_helper.sh"], stdout=subprocess.PIPE, universal_newlines=True)

            # Read the output of the speech recognition
            for stdout_line in iter(self.script_helper.stdout.readline, ""):
                if "Command: " in stdout_line:
                    try:
                        func_name = stdout_line.split()[1]
                    except IndexError:
                        continue
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
        if self.script_helper is not None:
            self.script_helper.terminate()
        time.sleep(3)
        self.shared_mode.close()


if __name__ == "__main__":
    script_helper = subprocess.Popen(["./voice_helper.sh"], stdout=subprocess.PIPE, universal_newlines=True)
    for stdout_line in iter(script_helper.stdout.readline, ""):
        if "Command: " in stdout_line:
            try:
                print(stdout_line.split()[1])
            except IndexError:
                continue
