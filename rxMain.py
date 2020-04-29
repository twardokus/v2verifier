from receiver import *

import os
import socket

def checkIfRoot():
    if os.geteuid() != 0:
        print "Error - you must be root! Try running with sudo"
        exit(1)


if __name__ == "__main__":
    checkIfRoot()
    
    s = socket.socket()
    s.connect(('127.0.0.1',6666))
    
    listen(s)
