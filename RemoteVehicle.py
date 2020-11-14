import subprocess
import time
from Utility import Utility


class RemoteVehicle:

    def __init__(self, bsm_queue):
        self.bsmQueue = bsm_queue
        self.util = Utility()

    # Send stream of payloads to GNURadio (wifi_tx.py)
    def start(self):
        for bsm in self.bsmQueue:
            bsm = self.util.inject_time(bsm)
            print("Sending BSM")
            loader = subprocess.Popen(("echo", "-n", "-e", bsm), stdout=subprocess.PIPE)
            sender = subprocess.check_output(("nc", "-w0", "-u", "localhost", "52001"), stdin=loader.stdout)
            time.sleep(0.1)
