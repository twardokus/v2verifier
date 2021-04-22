#!/usr/bin/env python3

import argparse
import os
import yaml
from gui import GUI
import threading
import time
import socket
from Utility import Utility
from Receiver import Receiver
from RemoteVehicle import RemoteVehicle
from LocalVehicle import LocalVehicle
from multiprocessing import Process


def main():
    parser = argparse.ArgumentParser(
        description="Run a V2V security experiment using V2Verifier"
    )
    parser.add_argument(
        "perspective", help="choice of perspective", choices=["local", "remote", "test"]
    )
    args = parser.parse_args()

    if os.geteuid() != 0:
        raise Exception("Error: rerun as root or with sudo")

    try:
        conf_file = open("init.yml", "r")
        config = yaml.load(conf_file, Loader=yaml.FullLoader)
    except Exception as e:
        print(f"Unable to load config file init.yml: {e}")

    if args.perspective == "local":
        gui = GUI()
        gui.start_receiver()
        gui.prep()

        sock = socket.socket()
        sock.connect(("127.0.0.1", 6666))

        lock = threading.Lock()
        receiver = Receiver()

        listener = threading.Thread(target=receiver.run_receiver, args=(sock, lock))
        listener.start()
        print("Listener running")

        lv = LocalVehicle(config["localConfig"]["tracefile"])
        local = threading.Thread(target=lv.start, args=(sock, lock))
        local.start()

        gui.run()
    elif args.perspective == "remote":
        util = Utility()

        remote_vehicles = []
        vehicle_processes = []

        try:
            for i in range(0, config["remoteConfig"]["numberOfVehicles"]):
                trace_file_path = config["remoteConfig"]["traceFiles"][i]
                bsm_queue = util.build_bsm_queue(
                    i, trace_file_path, f"keys/{i}/p256.key"
                )
                rv = RemoteVehicle(bsm_queue)
                remote_vehicles.append(rv)
        except IndexError:
            print(
                f"Error starting vehicles. The config file is missing a trace file or BSM file path for vehicle {i} in init.yml"
            )

        for rv in remote_vehicles:
            vehicle = Process(target=rv.start)
            vehicle_processes.append(vehicle)
            vehicle.start()
            print("Started legitimate vehicle")

        for vehicle in vehicle_processes:
            vehicle.join()

        print("All vehicle processes terminated")
    elif args.perspective == "test":
        gui = GUI()
        gui.start_receiver()
        gui.prep()
        print("Created gui object, calling run")
        gui_thread = threading.Thread(target=gui.run)
        gui_thread.start()
        print("thread started")

        time.sleep(5)
        gui.update_packet_counts(1, 2, 3, 4, 5)
        time.sleep(1)
        gui.process_new_packet("car_1", 43.0812, -77.680235, "N", True, True, True, 0)
        time.sleep(1)
        gui.process_new_packet("car_2", 43.0899, -77.681, "E", True, True, False, 0)
        time.sleep(1)
        gui.process_new_packet("car_3", 43.0845, -77.6802, "S", False, True, False, 0)
        time.sleep(1)
        gui.process_new_packet("car_1", 43.0812, -77.6803, "W", True, True, True, 0)
        for i in range(20):
            gui.add_message("message")

        gui_thread.join()


if __name__ == "__main__":
    main()
