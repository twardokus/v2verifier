from Utility import Utility

class LocalVehicle():
    
    def __init__(self, localTraceFile):
        self.util = Utility()
        self.trace = localTraceFile
        
    def start(self):
        messages = self.util.buildLocalQueue(self.trace)