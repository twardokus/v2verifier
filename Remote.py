import yaml

from multiprocessing import Process
from RemoteVehicle import RemoteVehicle
from Utility import Utility


class Remote:

    def run_remote(self):

        util = Utility()

        with open("init.yml", "r") as confFile:
            config = yaml.load(confFile, Loader=yaml.FullLoader)

        remote_vehicles = []

        # prepare the message queues for all vehicles
        try:
            for i in range(0, config["remoteConfig"]["numberOfVehicles"]):
                trace_file_path = config["remoteConfig"]["traceFiles"][i]
                bsm_queue = util.build_bsm_queue(i, trace_file_path, "keys/" + str(i) + "/p256.key")
                rv = RemoteVehicle(bsm_queue)
                remote_vehicles.append(rv)

        except IndexError:
            print("Error starting vehicles. Ensure you have entered enough trace files and BSM file paths "
                  "in \"init.yml\" to match the number of vehicles specified in that file.")

        # list to hold all spawned processes
        vehicle_processes = []

        # start transmitting packets for all legitimate vehicles
        for rv in remote_vehicles:
            vehicle = Process(target=rv.start)
            vehicle_processes.append(vehicle)
            vehicle.start()
            print("Started legitimate vehicle")

        for vehicle in vehicle_processes:
            vehicle.join()
