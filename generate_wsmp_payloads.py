# Geoff Twardokus

# Imports
import os
import csv
import time
from collections import OrderedDict
import subprocess

# Constants
pathToDataFile = os.getcwd() + "/traces.txt"

# Functions
def loadTraces():

    v0Trace = []
    v1Trace = []
    v2Trace = []
    v3Trace = []
    v4Trace = []
    v5Trace = []

    with open(pathToDataFile) as infile:
        data = csv.reader(infile, delimiter="\t")
        for row in data:
            if int(row[0]) == 0:
                v0Trace.append(row) 
            elif int(row[0]) == 1:
                v1Trace.append(row)
            elif int(row[0]) == 2:
                v2Trace.append(row)
            elif int(row[0]) == 3:
                v3Trace.append(row)
            elif int(row[0]) == 4:
                v4Trace.append(row)
            elif int(row[0]) == 5:
                v5Trace.append(row)
            elif int(row[0]) == 6:
                v6Trace.append(row)
 
    allTraces = [v0Trace, v1Trace, v2Trace, v3Trace, v4Trace, v5Trace]
    return allTraces

def printTraces(traces):
    for vehicle in traces:
        for item in vehicle:
            print(item)
            
def generatePayloadBytes():
    
    # Header fields individually set for easy configuration changes
    headerByteString = ""

    # llc_dsap
    headerByteString += "aa"
    #llc_ssap = "aa"
    headerByteString += "aa"
    #llc_control = "03"
    headerByteString += "03"
    #llc_org_code = "000000"
    headerByteString += "000000"
    #llc_type = "88dc"
    headerByteString += "88dc"
    #wsmp_n_subtype_opt_version = "03"
    headerByteString += "03"
    #wsmp_n_tpid = "00"
    headerByteString += "00"
    #wsmp_t_headerLengthAndPSID = "00"
    headerByteString += "20"
    #wsmp_t_length = "00"
    headerByteString += "00"    

    headerByteString = "\\x".join(headerByteString[i:i+2] for i in range(0, len(headerByteString), 2))
    
    #headerByteString = "".join(headerByteString[i:i+2] for i in range(0, len(headerByteString), 2))
    headerByteString = "\\x" + headerByteString

    payloadByteString = ""

    # IEEE 1609.2 Header
    
    # Version
    payloadByteString += "03"

    # ContentType (unsecured data = 00, signed data = 01)
    payloadByteString += "01"

    payloadByteString += "00"

    # Unsigned data

    # HashID (SHA-256 -> 00)
    payloadByteString += "00"

    # Payload
    payloadByteString += "00"


    payloadByteString += "000000"

    #payloadByteString = "030000"

    payloadByteString = "\\x".join(payloadByteString[i:i+2] for i in range(0, len(payloadByteString), 2))
    payloadByteString = "\\x" + payloadByteString

    pduPayload = headerByteString + payloadByteString

    return pduPayload

def writeVehicleTraces(traces):
    
    outfiles = [
    os.getcwd() + "/v0path",
    os.getcwd() + "/v1path",
    os.getcwd() + "/v2path",
    os.getcwd() + "/v3path",
    os.getcwd() + "/v4path",
    os.getcwd() + "/v5path"
    ]

    for vehicle in range (0,6):
        with open(outfiles[vehicle], 'w') as outfile:
            for trace in traces:
                for position in trace:
                   if position[0] == str(vehicle):
                       print position[0]
                       outfile.write(str(position[2]) + "," + str(position[3]) + "\n")
            outfile.close()

def sendPacketStream(vehicleNo):
    if vehicleNo < 0 or vehicleNo > 5:
        print "Error - invalid vehicle number. Must be between 0 and 5. Exiting"
        exit()
    for i in range(0,500):
        #os.system("echo -e " + generatePayloadBytes() + " | nc -w1 -u localhost 52001")
        loader = subprocess.Popen(("echo","-n","-e",generatePayloadBytes()), stdout=subprocess.PIPE)
        sender = subprocess.check_output(("nc","-w1","-u","localhost","52001"),stdin=loader.stdout)
        time.sleep(0.5)


# Execution hook
if __name__ == "__main__":
    traces = loadTraces()
    #writeVehicleTraces(traces)
    sendPacketStream(0)
