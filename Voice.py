# This program is to be spawned by the main robot class.
# It runs the wake word detection and the speech recognition.
import subprocess
import json
# from rpi_ws281x import *  # TODO: LED strip
from multiprocessing.shared_memory import SharedMemory


class Voice:
    def __init__(self, shared_memory_name):
        self.shared_mode = SharedMemory(name=shared_memory_name, create=False)
        self.state = False

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
            subprocess.Popen(["voice2json", "wait-wake", "--exit-count", "1"], shell=True)
            voice_command = subprocess.Popen(['voice2json', 'transcribe-stream', '--exit-count', '1', '|', 'voice2json', 'recognize-intent'],
                                             shell=True, stdout=subprocess.PIPE, universal_newlines=True)

            # Read the output of the speech recognition
            for stdout_line in iter(voice_command.stdout.readline, ""):
                data = json.loads(stdout_line)
                if not data['timeout'] and data['intent']['name']:
                    func_name = data['intent']['name']
                    if func_name == "SitDown":
                        self.shared_mode.buf[0] = 0
                    elif func_name == "Follow":
                        self.shared_mode.buf[0] = 1
                    elif func_name == "Spin":
                        self.shared_mode.buf[0] = 2
                    elif func_name == "Speak":
                        self.shared_mode.buf[0] = 3

    def stop(self):
        self.state = False
        self.shared_mode.close()


if __name__ == "__main__":
    subprocess.Popen(["voice2json", "-p", "en-us_kaldi-zamia", "wait-wake", "--exit-count", "1"], shell=True)
    print("Wake received")
    voice_command = subprocess.Popen(['voice2json', "-p", "en-us_kaldi-zamia", 'transcribe-stream', '--exit-count', '1', '|', 'voice2json', "-p", "en-us_kaldi-zamia", 'recognize-intent'],
                                             shell=True, stdout=subprocess.PIPE, universal_newlines=True)
    for stdout_line in iter(voice_command.stdout.readline, ""):
        print(stdout_line)
