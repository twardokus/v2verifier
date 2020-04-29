from receiver import *
from transmitter import loadTracesFromFile, writeVehicleTraceFiles

import os
import socket
import threading

def checkIfRoot():
    if os.geteuid() != 0:
        print "Error - you must be root! Try running with sudo"
        exit(1)


if __name__ == "__main__":
    checkIfRoot()
    
    traces = loadTracesFromFile(os.getcwd() + "/traces.csv")
    writeVehicleTraceFiles(traces)


    s = socket.socket()
    s.connect(('127.0.0.1',6666))

    ownVehicleID = 1

    lock = threading.Lock()

    run = threading.Thread(target=runSelf, args=(ownVehicleID, s, lock,))
    run.start()
    
    listen = threading.Thread(target=listen, args=(s,lock,))
    listen.start()
