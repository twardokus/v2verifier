# Geoff Twardokus

# Imports
import os
import csv

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
    
    headerFields = {
    "llc_dsap":"aa",
    "llc_ssap":"aa",
    "llc_control":"03",
    "llc_org_code":"00\\x00\\x00",
    "llc_type":"88\\xdc",
    "wsmp_n_subtype_opt_version":"03",
    "wsmp_n_tpid":"00",
    "wsmp_t_headerLengthAndPSID":"00",
    "wsmp_t_length":"00"
    }

    headerByteString = ""

    for field in headerFields:
        headerByteString += "\\x" + headerFields[field]

    print headerByteString

# Execution hook
if __name__ == "__main__":
    traces = loadTraces()
    generatePayloadBytes()
    #printTraces(traces)
