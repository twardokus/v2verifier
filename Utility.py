# a file for utility functions
import math
from v2verifier.wave import WAVEPacketBuilder

class Utility:
    
    def __init__(self):
        self.waveBuilder = WAVEPacketBuilder()
        
    def buildBSMQueue(self, traceFilePath, key):
        
        bsmQueue = []
        
        with open(traceFilePath, "r") as infile:
            coordinateList = infile.readlines()
            
        for i in range(0, len(coordinateList) - 2):
            heading = self.calculateHeading(coordinateList[i], coordinateList[i+1])
            speed = self.calcSpeed(coordinateList[i], coordinateList[i+1])
            bsmText = coordinateList[i].replace("\n","") + "," + heading + "," + str(round(speed,2)) + "\n"
            bsmQueue.append(self.waveBuilder.getWSMPayload(bsmText, key))
            
        return bsmQueue
        #getWSMPayload
        
    # For the local vehicle, full WSMs are unnecessary as there is no communication over the SDR
    def buildLocalQueue(self, traceFilePath):
        with open(traceFilePath) as infile:
            coordinates = infile.readlines()
        messages = []
        for i in range(0, len(coordinates)):
            messages.append(coordinates + "," + self.calculateHeading(coordinates[i], coordinates[i+1]) + "," + self.calcSpeed(coordinates[i], coordinates[i+1]))
        return messages
        
    # takes in two strings "x,y" from a trace file
    # returns one- or two-character string indicating heading
    def calculateHeading(self, currentCoords, nextCoords):
        xNow, yNow = currentCoords.split(",")
        xNow = float(xNow)
        yNow = float(yNow)
    
        xNext, yNext = nextCoords.split(",")
        xNext = float(xNext)
        yNext = float(yNext)
    
        if xNext == xNow and yNext == yNow:
            return "-"
        else:
            if xNext > xNow:
                if yNext > yNow:
                    return "SE"
                elif yNext == yNow:
                    return "E"
                else:
                    return "NE"
            elif xNext == xNow:
                return "S" if yNext > yNow else "N"
            elif xNext < xNow:
                if yNext > yNow:
                    return "SW"
                elif yNext == yNow:
                    return "W"
                else:
                    return "NW"
        
    # takes in two strings "x,y" from a trace file
    # returns speed in km/hr
    def calcSpeed(self, currentCoords, nextCoords):
        xNow, yNow = currentCoords.split(",")
        xNow = float(xNow)
        yNow = float(yNow)
    
        xNext, yNext = nextCoords.split(",")
        xNext = float(xNext)
        yNext = float(yNext)
        
        return math.sqrt(math.pow(xNext-xNow, 2)+math.pow(yNext-yNow, 2)) * 36
