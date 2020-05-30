import subprocess

class RemoteVehicle:
    
    def __init__(self, pathToBSMFile):
        self.bsmFile = pathToBSMFile
        self.loadBSMs()
        
    """
    Load the BSM message strings from a precompiled file into a list for rapid processing
    """
    def loadBSMs(self):
        with open(self.bsmFile) as bsmFile:
            self.bsmSequence = bsmFile.readlines()
    
    # Send stream of payloads to GNURadio (wifi_tx.py)
    def start(self):
        for BSM in self.bsmSequence:
                loader = subprocess.Popen(("echo","-n","-e",BSM), stdout=subprocess.PIPE)
                sender = subprocess.check_output(("nc","-w0","-u","localhost","52001"),stdin=loader.stdout) 
        