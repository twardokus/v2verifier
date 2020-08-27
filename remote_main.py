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

# Loop until the user chooses to exit the program
while True:
    
    # Make the user choose a (valid) option
    validResponse = False
    while not validResponse:
        option = input("Please choose an option: ")
        if option in ['0', '1', '2', 'q', 'Q']:
            validResponse = True
        else:
            print("Invalid response. Please enter 0, 1, 2, or press Q to quit.")
    
    # If the user wants to exit the program, quit with a message.
    if option in ['q', 'Q']:
        print("Goodbye!")
        break
    
    # If not 'q' or 'Q', then the user entered an integer choice that must be cast from string input
    option = int(option)
    
    # list to hold all spawned processes
    vehicleProcesses = []
    
    # start transmitting packets for all legitimate vehicles
    for rv in remoteVehicles:
        vehicle = Process(target=rv.start)
        vehicleProcesses.append(vehicle)
        vehicle.start()
        print("Started legitimate vehicle")
    
    if option == 1:
        # start running the replay attacker
        replayer = ReplayAttacker()
        replay = Process(target=replayer.replayAttack, args=(2,))
        vehicleProcesses.append(replay)
        replay.start()
        print("Started replay attacker")
        
    elif option == 2:
        # start a spoofing attack
        traceFilePath = config["spoofer"]["traceFile"]
        spoofedBSMQueue = util.buildSpoofedBSMQueue(random.randint(0,10), traceFilePath)
        spoofer = RemoteVehicle(spoofedBSMQueue)
        spoofProc = Process(target=spoofer.start)
        vehicleProcesses.append(spoofProc)
        spoofProc.start()
        print("Started spoofing attacker")
        
        
    for vehicle in vehicleProcesses:
        vehicle.join()
    
    
    