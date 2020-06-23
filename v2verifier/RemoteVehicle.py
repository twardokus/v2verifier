import subprocess
import time
from Utility import Utility

class RemoteVehicle:
    
    def __init__(self, bsmQueue):
        self.bsmQueue = bsmQueue
        self.util = Utility()
    
    # Send stream of payloads to GNURadio (wifi_tx.py)
    def start(self):
        for BSM in self.bsmQueue:
            BSM = self.util.injectTime(BSM)
            #print("real:\t" + BSM)
            loader = subprocess.Popen(("echo","-n","-e",BSM), stdout=subprocess.PIPE)
            sender = subprocess.check_output(("nc","-w0","-u","localhost","52001"),stdin=loader.stdout) 
            time.sleep(0.1)