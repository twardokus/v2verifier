import json
import time
from Utility import Utility


class GPSVehicle:
    def __init__(self, gps_sock, gui_sock, gui_lock):
        self.gps_sock = gps_sock
        self.sock = gui_sock
        self.lock = gui_lock
        self.util = Utility()

    def start(self):
        while True:
            message = self.gps_sock.recv(1024)

            self.send_to_radio(message)
            self.send_to_gui(message)

    def send_to_radio(self, message):
        print("Sending BSM to radio")

        bsm = self.util.inject_time(bsm)

        loader = subprocess.Popen(("echo", "-n", "-e", bsm), stdout=subprocess.PIPE)
        sender = subprocess.check_output(
            ("nc", "-w0", "-u", "localhost", "52001"), stdin=loader.stout
        )

    def send_to_gui(self, message):
        print("Sending BSM to GUI")

        bsm = msg.split(",")

        decoded_data = {}

        decoded_data["id"] = bsm[0]
        decoded_data["x"] = bsm[1]
        decoded_data["y"] = bsm[2]
        decoded_data["heading"] = bsm[3]
        decoded_data["speed"] = bsm[4]

        decoded_data["sig"] = True
        decoded_data["elapsed"] = 0
        decoded_data["recent"] = True
        decoded_data["receiver"] = True

        vehicle_data_json = json.dumps(decoded_data)

        with lock:
            self.sock.send(vehicle_data_json.encode())

    def send_to_gui(self, messages):
        for msg in messages:
            bsm = msg.split(",")

            time.sleep(0.1)
