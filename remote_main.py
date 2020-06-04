"""
This is the main execution file for the remote vehicle
"""

# Imports
import yaml
from multiprocessing import Process
from RemoteVehicle import RemoteVehicle
from Utility import Utility
from ReplayAttacker import ReplayAttacker
import time
import os
import random

if os.geteuid() != 0:
        print("Error - you must be root! Try running with sudo")
        exit(1)

util = Utility()

with open("init.yml", "r") as confFile:
    config = yaml.load(confFile,Loader=yaml.FullLoader)

remoteVehicles = []

# prepare the message queues for all vehicles
try:
    for i in range(0, config["remoteConfig"]["numberOfVehicles"]):
        traceFilePath = config["remoteConfig"]["traceFiles"][i]
        bsmQueue = util.buildBSMQueue(i, traceFilePath, "keys/" + str(i) + "/p256.key")
        rv = RemoteVehicle(bsmQueue)
        remoteVehicles.append(rv)
        
except IndexError:
    print("Error starting vehicles. Ensure you have entered enough trace files and BSM file paths in \"init.yml\" to match the number of vehicles specified in that file.")

# start transmitting packets for all vehicles
for rv in remoteVehicles:
    vehicle = Process(target=rv.start)
    vehicle.start()
    print("started")

"""
# start running the replay attacker
replayer = ReplayAttacker()
replay = Process(target=replayer.replayAttack, args=(5,)) 
replay.start()
"""

# start a spoofing attack
traceFilePath = config["spoofer"]["traceFile"]
spoofedBSMQueue = util.buildSpoofedBSMQueue(random.randint(0,10), traceFilePath)
spoofer = RemoteVehicle(spoofedBSMQueue)
spoofProc = Process(target=spoofer.start)
spoofProc.start()


