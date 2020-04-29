from transmitter import *

import os

if __name__ == "__main__":


    traces = loadTracesFromFile(os.getcwd() + "/traces.csv")
    writeVehicleTraceFiles(traces)
    sendPacketStream(0)
