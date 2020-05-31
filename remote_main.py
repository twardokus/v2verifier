"""
This is the main execution file for the remote vehicle
"""

# Imports
import yaml
from threading import Thread
from RemoteVehicle import RemoteVehicle
from Utility import Utility

util = Utility()

with open("init.yml", "r") as confFile:
    config = yaml.load(confFile,Loader=yaml.FullLoader)

remoteVehicles = []

try:
    for i in range(0, config["remoteConfig"]["numberOfVehicles"]):
        traceFilePath = config["remoteConfig"]["traceFiles"][i]
        bsmQueue = util.buildBSMQueue(i, traceFilePath, "keys/" + config["remoteConfig"]["keys"][i])
        rv = RemoteVehicle(bsmQueue)
        remoteVehicles.append(rv)
        
except IndexError:
    print("Error starting vehicles. Ensure you have entered enough trace files and BSM file paths in \"init.yml\" to match the number of vehicles specified in that file.")
    
for vehicle in remoteVehicles:
    print("starting vehicle")
    v = Thread(target=vehicle.start(),)
    v.start()