# a file for utility functions
import math
from WavePacketBuilder import WAVEPacketBuilder
from datetime import datetime
import time

class Utility:
    
    def __init__(self):
        self.waveBuilder = WAVEPacketBuilder()
        
    def buildBSMQueue(self, vehicleNo, traceFilePath, key):
        
        bsmQueue = []
        with open(traceFilePath, "r") as infile:
            coordinateList = infile.readlines()
        if len(coordinateList) < 3:
            raise Exception("Your file must have at least 3 pairs of coordinates")
            
        for i in range(0, len(coordinateList) - 2):
            heading = self.calculateHeading(coordinateList[i], coordinateList[i+1])
            speed = self.calcSpeed(coordinateList[i], coordinateList[i+1])
            bsmText = str(vehicleNo) + "," + coordinateList[i].replace("\n","") + "," + heading + "," + str(round(speed,2)) + "\n"
            bsmQueue.append(self.waveBuilder.getWSMPayload(bsmText, key))
            
        return bsmQueue
        #getWSMPayload
        
    # For the local vehicle, full WSMs are unnecessary as there is no communication over the SDR
    def buildLocalQueue(self, traceFilePath):
        with open(traceFilePath) as infile:
            coordinates = infile.readlines()
        messages = []
        for i in range(0, len(coordinates)-2):
            messages.append("99," + coordinates[i].replace("\n","") + "," + self.calculateHeading(coordinates[i], coordinates[i+1]) + "," + str(self.calcSpeed(coordinates[i], coordinates[i+1])))
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
    
    def injectTime(self,bsm):
        
        # IEEE 1609.2 defines timestamps as an estimate of the microseconds elapsed since
        # 12:00 AM on January 1, 2004
        origin = datetime(2004, 1, 1, 0, 0, 0, 0)
        
        # get the offset since the origin time in microseconds
        offset = (datetime.now() - origin).total_seconds() * 1000
        timestr = hex(int(math.floor(offset)))
        timestr  = timestr[2:]
        if len(timestr) < 16:
            for i in range(0, 16 - len(timestr)):
                timestr = "0" + timestr
        timestr = "\\x" + "\\x".join(timestr[i:i+2] for i in range(0, len(timestr), 2))
        bsm = bsm.replace("\\xF0\\xE0\\xF0\\xE0\\xF0\\xE0\\xF0\\xE0",timestr)

        return bsm.replace("\\xF0\\xE0\\xF0\\xE0\\xF0\\xE0\\xF0\\xE0",timestr)
