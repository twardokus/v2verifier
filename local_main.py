# this is the main execution file for the "local vehicle"

import yaml
from threading import Lock
from socket import socket
from v2verifier.Receiver import Receiver


from v2verifier.LocalVehicle import LocalVehicle

with open("init.yml", "r") as confFile:
    config = yaml.load(confFile,Loader=yaml.FullLoader)

if __name__=="__main__":
    s = socket.socket()
    s.connect(('127.0.0.1',6666))
    
    lock = Lock()
    
    receiver = Receiver()
    receiver.runReceiver(s, lock)
    
    