import subprocess
import time

class RemoteVehicle:
    
    def __init__(self, bsmQueue):
        self.bsmQueue = bsmQueue
    
    # Send stream of payloads to GNURadio (wifi_tx.py)
    def start(self):
        print("start")
        for BSM in self.bsmQueue:
                print("sending BSM")
                loader = subprocess.Popen(("echo","-n","-e",BSM), stdout=subprocess.PIPE)
                sender = subprocess.check_output(("nc","-w0","-u","localhost","52001"),stdin=loader.stdout) 
                time.sleep(0.1)