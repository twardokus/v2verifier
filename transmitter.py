# Geoff Twardokus

# Imports
import os
import csv
import time
from collections import OrderedDict
import subprocess
from fastecdsa import keys, ecdsa
from fastecdsa.keys import import_key
from hashlib import sha256

# Constants


# Functions
def loadTracesFromFile(pathToDataFile):

    v0Trace = []
    v1Trace = []
    v2Trace = []
    v3Trace = []
    v4Trace = []
    v5Trace = []
    
    with open(pathToDataFile) as infile:
        data = csv.reader(infile, delimiter=",")
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
            
def generatePayloadBytes(vehicleDataString):
    
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
    
    ####################################################
    # IEEE1609Dot2Data Structure
    payloadByteString = ""
        
    # Protocol Version
    payloadByteString += "03"

    # ContentType ( signed data = 81)
    payloadByteString += "81"

    # HashID (SHA256 = 00)
    payloadByteString += "00"
    
    # Data
    payloadByteString += "40"

    # Protocol Version
    payloadByteString += "03"

    # Content - Unsecured Data
    payloadByteString += "80"

    # Length of Unsecured Data
    payloadByteString += "0"
    vehicleData = str(hex(len(vehicleDataString)).split("x")[1])
    payloadByteString += vehicleData

    # unsecuredData
    payloadByteString += vehicleDataString.encode('hex')
    
    # headerInfo
    payloadByteString += "4001"

    # PSID (BSM = 20)
    payloadByteString += "20"

    # generationTime (8 bytes)
    payloadByteString += "1112131415161718"

    # signer
    payloadByteString += "80"

    # Digest (8 bytes)
    payloadByteString += "2122232425262728"

    # signature (ecdsaNistP256Signature = 80)
    payloadByteString += "80"

    # ecdsaNistP256Signature (r: compressed-y-0 = 82)
    # 80 -> x-only
    # 81 -> fill (NULL)
    # 82 -> compressed-y-0
    # 83 -> compressed-y-1
    # 84 -> uncompressed
    payloadByteString += "80"

    private, public = import_key("/home/administrator/v2v-capstone/keys/p256.key")

    r, s = ecdsa.sign(vehicleDataString.encode('hex'), private, hashfunc=sha256)

    r = hex(r)
    s = hex(s)
    
    r = r.split("x")[1][:len(r)-3]
    s = s.split("x")[1][:len(s)-3]

    # r (32 bytes)
    payloadByteString += str(r)

    # s (32 bytes)
    payloadByteString += str(s)

    payloadByteString = "\\x".join(payloadByteString[i:i+2] for i in range(0, len(payloadByteString), 2))
    payloadByteString = "\\x" + payloadByteString

    pduPayload = headerByteString + payloadByteString

    return pduPayload

def writeVehicleTraceFiles(traces):
    
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
                       outfile.write(str(position[1]) + "," + str(position[2]) + "\n")
            outfile.close()

def sendPacketStream(vehicleNo):
    if vehicleNo < 0 or vehicleNo > 5:
        print "Error - invalid vehicle number. Must be between 0 and 5. Exiting"
        exit()
    trace = open("v"+str(vehicleNo)+"path")
    for i in range(0,400):
        vehicleData = str(vehicleNo) + "," + trace.readline()
        loader = subprocess.Popen(("echo","-n","-e",generatePayloadBytes(vehicleData)), stdout=subprocess.PIPE)
        sender = subprocess.check_output(("nc","-w1","-u","localhost","52001"),stdin=loader.stdout)
        time.sleep(0.1)


# Execution hook
if __name__ == "__main__":
    traces = loadTraces()
    writeVehicleTraces(traces)
    sendPacketStream(0)
