"""
This file is the master execution script for the host playing the part of "receiver."
The host that is running "wifi_rx.py" should run this script along with the GUI 
application (see the README).
"""

# Local imports
from receiver import *

# Library imports
import os
import socket
import threading

def checkIfRoot():
    if os.geteuid() != 0:
        print "Error - you must be root! Try running with sudo"
        exit(1)

if __name__ == "__main__":
    
    # This script needs root access in order to connect to a TCP socket
    checkIfRoot()

    # TCP connection to the GUI application's listener
    s = socket.socket()
    s.connect(('127.0.0.1',6666))

    lock = threading.Lock()
    
    # This is the thread that updates the "vehicle" that is represented by
    # by the receiving USRP. No actual transmission for this vehicle.
#    run = threading.Thread(target=runSelf, args=(ownVehicleID, s, lock,))
#    run.start()

    #run = threading.Thread(target=runSelfAndOthers, args=(s, lock,))
    #run.start()

    # This is the thread that accepts data from the other vehicle (via USRP)
    # and sends it to the GUI
    listen = threading.Thread(target=listen, args=(s,lock,))
    listen.start()
