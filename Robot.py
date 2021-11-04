from multiprocessing.shared_memory import SharedMemory
from BaseLibrary.Code.Server.Motor import *

"""
This shared variable will control what the robot is currently doing.
It will be shared between the voice recognition process and polled during every robot loop.

0: Following mode - Facial tracking active and robot follows
1: Stopped mode - Facial tracking active but robot stationary
2: Spin mode - Facial tracking inactive and robot spins
3: Shutdown - End program
"""
# To access the shared memory from an external process, do
#     shared_ptr = SharedMemory(name="mode", create=False)
# and get the address of the buffer.
# See: https://docs.python.org/3/library/multiprocessing.shared_memory.html
shared_ptr = SharedMemory(name="mode", create=True, size=1)
mode = shared_ptr.buf  # Access the mode by writing/reading to mode[0]

# Initialize the mode to 0
mode[0] = 0


# Main robot loop goes here
while mode[0] != 3:
    pass  # TODO



# Deinitialize shared memory on exit
time.sleep(5)  # Delay to ensure all processes close the shared ptr first
shared_ptr.close()
shared_ptr.unlink()