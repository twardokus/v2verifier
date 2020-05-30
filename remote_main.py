"""
This is the main execution file for the remote vehicle
"""

# Imports
import yaml
from threading import Thread
from v2verifier.RemoteVehicle import RemoteVehicle
from v2verifier.Utility import Utility
from v2verifier.wave import WAVEPacketBuilder

util = Utility()

with open("init.yml", "r") as confFile:
    config = yaml.load(confFile,Loader=yaml.FullLoader)

remoteVehicles = []

try:
    for i in range(0, config["remoteConfig"]["numberOfVehicles"]):
        traceFilePath = config["remoteConfig"]["traceFiles"][i]
        
        bsmQueue = util.buildBSMQueue(traceFilePath)
        
        rv = RemoteVehicle(bsmQueue)
        remoteVehicles.append(rv)
        
except IndexError:
    print("Error starting vehicles. Ensure you have entered enough trace files and BSM file paths in \"init.yml\" to match the number of vehicles specified in that file.")
    
for vehicle in remoteVehicles:
    v = Thread(target=vehicle.start(),)
    v.start()