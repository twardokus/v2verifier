#!/usr/bin/env python3

import argparse
import os
import yaml
import random
import threading
import time
import socket
from gui import GUI
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
        time.sleep(1)

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
    elif args.perspective == "gps":
        util = Utility()

        gui = GUI()
        gui.start_receiver()
        gui.prep()
        time.sleep(1)

        gps_sock = socket.socket()
        gps_sock.connect(("localhost", "gps port"))

        sock = socket.socket()
        sock.connect(("127.0.0.1", 6666))

        lock = threading.Lock()
        receiver = Receiver()

        listener = threading.Thread(target=receiver.run_receiver, args=(sock, lock))
        listener.start()
        print("Listener running")

        gps_vehicle = GPSVehicle(gps_sock, sock, lock)
        gps_thread = threading.Thread(gps_vehicle.start)
        gps_thread.start()

        gui.run()
    elif args.perspective == "test":
        gui = GUI()
        gui.start_receiver()
        gui.prep()
        time.sleep(1)
        print("Created gui object, calling run")
        gui_thread = threading.Thread(target=gui.run)
        gui_thread.start()
        print("thread started")

        with open("coords/coords_1") as coord_file:
            while True:
                for line in coord_file:
                    lat, lng = line.strip().split(", ")
                    # update car location
                    gui.process_new_packet("car_1", lat, lng, "N", True, True, True, 0)

                    # add message
                    message = "<p>Message from car_1:</p>"
                    message += (
                        '<p class="tab">✔️ Message successfully authenticated</p>'
                    )
                    message += '<p class="tab">✔️ Message is recent: 31.6 ms since transmission</p>'
                    message += f'<p class="tab">Vehicle reports location at {lat}, {lng} traveling N</p>'
                    gui.add_message(message)

                    # update packet counts
                    gui.received_packets += 1
                    gui.intact_packets += 1
                    if random.random() <= 0.8:
                        gui.authenticated_packets += 1
                    gui.ontime_packets += 1

                    time.sleep(0.5)

        gui_thread.join()


if __name__ == "__main__":
    main()
