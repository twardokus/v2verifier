# this is the main execution file for the "local vehicle"

import os
import sys

sys.path.append(os.getcwd())

import yaml
from threading import Thread
from Recorder import Recorder
from LocalVehicle import LocalVehicle

with open("init.yml", "r") as confFile:
    config = yaml.load(confFile,Loader=yaml.FullLoader)

if __name__=="__main__":
    
    if os.geteuid() != 0:
        print("Error - you must be root! Try running with sudo")
        exit(1)
    
    receiver = Recorder()
    
    listener = Thread(target=receiver.listenForWSMs)
    listener.start()
    print("Listener running...")
    
