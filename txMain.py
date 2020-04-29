from functions import *

import os

if __name__ == "__main__":


    traces = loadTracesFromFile(os.getcwd() + "/traces.csv")
    writeVehicleTraces(traces)
    sendPacketStream(0)
