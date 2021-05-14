import argparse
import os
import yaml
import random
import threading
import time
import socket
import sys
from gui import GUI
from GPSVehicle import GPSVehicle
from multiprocessing import Process

from txrx import Remote, Local

if __name__=="__main__":

    parser = argparse.ArgumentParser(description="Run a V2V security experiment using V2Verifier.")
    parser.add_argument("perspective",
                        help="choice of perspective",
                        choices=["local", "remote", "gps", "test"]
    )
    parser.add_argument("-g",
                        "--with-gui",
                        help="enables GUI support for the 'local' perspective. Has no effect for "
                            "remote perspective",
                        action='store_true')
    parser.add_argument("technology",
                        help="choice of DSRC or C-V2X technology stack",
                        choices=["dsrc", "cv2x"])
    parser.add_argument("--device",
                        help="choice of Cohda or SDR for C-V2X",
                        choices=["cohda", "sdr"],
                        required=("cv2x" in sys.argv))

    args = parser.parse_args()    

    if args.perspective == "local":
        if args.with_gui:
            print("Running local perspective with GUI enabled...")
            if args.device == "cohda":
                Local.run_local(with_gui=True, tech=args.technology, cohda=True)
            else:
                Local.run_local(with_gui=True, tech=args.technology)
        else:
            print("Running local perspective in console mode...")
            if args.device == "cohda":
                Local.run_local(tech=args.technology, cohda=True)
            else:
                Local.run_local(tech=args.technology)

    elif args.perspective == "remote":
        Remote.run_remote()

#    elif args.perspective == "gps":
#        util = Utility()
#
#        gui = GUI()
#         gui.start_receiver()
#         gui.prep()
#         time.sleep(1)
#
#         gps_sock = socket.socket()
#         gps_sock.connect(("localhost", 5555))
#
#         sock = socket.socket()
#         sock.connect(("127.0.0.1", 6666))
#
#         lock = threading.Lock()
#         receiver = Receiver()
#
#         listener = threading.Thread(target=receiver.run_receiver, args=(sock, lock))
#         listener.start()
#         print("Listener running")
#
#         gps_vehicle = GPSVehicle(71, gps_sock, sock, lock)
#         gps_thread = threading.Thread(target=gps_vehicle.start)
#         gps_thread.start()
#
#         gui.run()
#     elif args.perspective == "test":
#         gui = GUI()
#         gui.start_receiver()
#         gui.prep()
#         time.sleep(1)
#         print("Created gui object, calling run")
#         gui_thread = threading.Thread(target=gui.run)
#         gui_thread.start()
#         print("thread started")
#
#         with open("coords/coords_1") as coord_file:
#             while True:
#                 for line in coord_file:
#                     lat, lng = line.strip().split(", ")
#                     # update car location
#                     gui.process_new_packet("car_1", lat, lng, "N", True, True, True, 0)
#
#                     # add message
#                     message = "<p>Message from car_1:</p>"
#                     message += (
#                         '<p class="tab">✔️ Message successfully authenticated</p>'
#                     )
#                     message += '<p class="tab">✔️ Message is recent: 31.6 ms since transmission</p>'
#                     message += f'<p class="tab">Vehicle reports location at {lat}, {lng} traveling N</p>'
#                     gui.add_message(message)
#
#                     # update packet counts
#                     gui.received_packets += 1
#                     gui.intact_packets += 1
#                     if random.random() <= 0.8:
#                         gui.authenticated_packets += 1
#                     gui.ontime_packets += 1
#
#                     time.sleep(0.5)
#
#         gui_thread.join()
#
#
# if __name__ == "__main__":
#     main()
