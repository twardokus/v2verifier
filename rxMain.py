from receiver import runReceiver

import os

def checkIfRoot():
    if os.geteuid() != 0:
        print "Error - you must be root! Try running with sudo"
        exit(1)


if __name__ == "__main__":
#    checkIfRoot()
    runReceiver()
