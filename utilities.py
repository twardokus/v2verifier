# a file for utility functions
import math

# takes a CSV file with two columns for x and y value, generates a BSM file
def compileBSMFile(traceFile, bsmOutputPath):
    coords = []
    with open(traceFile, "r") as infile:
        coords = infile.readlines()
    
    with open(bsmOutputPath, "w") as outfile:
        for i in range(0, len(coords)-2):
            heading = calculateHeading(coords[i], coords[i+1])
            speed = calcSpeed(coords[i], coords[i+1])
            bsm = coords[i] + "," + heading + "," + str(speed) + "\n"
            outfile.write(bsm)
            
# takes in two strings "x,y" from a trace file
# returns one- or two-character string indicating heading
def calculateHeading(currentCoords, nextCoords):
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
def calcSpeed(currentCoords, nextCoords):
    xNow, yNow = currentCoords.split(",")
    xNow = float(xNow)
    yNow = float(yNow)

    xNext, yNext = nextCoords.split(",")
    xNext = float(xNext)
    yNext = float(yNext)
    
    return math.sqrt(math.pow(xNext-xNow, 2)+math.pow(yNext-yNow, 2)) * 36