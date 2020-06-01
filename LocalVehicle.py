from Utility import Utility
import json
import time

class LocalVehicle():
    
    def __init__(self, localTraceFile):
        self.util = Utility()
        self.trace = localTraceFile
        
    def start(self, s, lock):
        messages = self.util.buildLocalQueue(self.trace)
        self.sendToGUI(messages, s, lock)
        
    def sendToGUI(self, messages, s, lock):
        
        for msg in messages: 
            
            bsm = msg.split(",")
            
            decodedData = {}    
            
            decodedData['id'] = bsm[0]
            decodedData['x'] = bsm[1]
            decodedData['y'] = bsm[2]
            decodedData['heading'] = bsm[3]
            decodedData['speed'] = bsm[4]
            
            decodedData['sig'] = True
            decodedData['elapsed'] = 0
            decodedData['recent'] = True
            decodedData['receiver'] = True
        
            vehicleDataJSON = json.dumps(decodedData)
        
            with lock:
                s.send(vehicleDataJSON.encode())
            time.sleep(0.1)
            
