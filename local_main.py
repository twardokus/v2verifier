# this is the main execution file for the "local vehicle"

import os
import sys

print(os.getcwd())
sys.path.append("/home/administrator/eclipse-workspace/v2verifier/v2verifier")

import yaml
from threading import Lock, Thread
from socket import socket
from Recorder import Recorder
from GUI import GUI
import tkinter as tk


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
    
