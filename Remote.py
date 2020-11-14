import yaml
import os

from multiprocessing import Process
from RemoteVehicle import RemoteVehicle
from Utility import Utility


class Remote:

    def run_remote(self):

        util = Utility()

        with open("init.yml", "r") as confFile:
            config = yaml.load(confFile, Loader=yaml.FullLoader)

        remoteVehicles = []

        # prepare the message queues for all vehicles
        try:
            for i in range(0, config["remoteConfig"]["numberOfVehicles"]):
                traceFilePath = config["remoteConfig"]["traceFiles"][i]
                bsmQueue = util.build_bsm_queue(i, traceFilePath, "keys/" + str(i) + "/p256.key")
                rv = RemoteVehicle(bsmQueue)
                remoteVehicles.append(rv)

        except IndexError:
            print("Error starting vehicles. Ensure you have entered enough trace files and BSM file paths in \"init.yml\" t"
                  "o match the number of vehicles specified in that file.")

        # list to hold all spawned processes
        vehicleProcesses = []

        # start transmitting packets for all legitimate vehicles
        for rv in remoteVehicles:
            vehicle = Process(target=rv.start)
            vehicleProcesses.append(vehicle)
            vehicle.start()
            print("Started legitimate vehicle")

        for vehicle in vehicleProcesses:
            vehicle.join()
