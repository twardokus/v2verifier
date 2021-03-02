import subprocess
import time
import Utility


class RemoteVehicle:

    def __init__(self, bsm_queue):
        self.bsmQueue = bsm_queue

    # Send stream of payloads to GNURadio (wifi_tx.py)
    def start(self):
        for bsm in self.bsmQueue:
            bsm = Utility.inject_time(bsm)
            print("Sending BSM")
            loader = subprocess.Popen(("echo", "-n", "-e", bsm), stdout=subprocess.PIPE)
            sender = subprocess.check_output(("nc", "-w0", "-u", "localhost", "52001"), stdin=loader.stdout)
            time.sleep(0.1)
