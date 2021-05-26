import eel
import threading
import yaml
import folium
import time
import socket
import logging
import json
import struct


class WebGUI:
    """A class to represent the Web-based V2Verifier GUI

    TODO: complete this docstring entry

    Methods:

    """

    def __init__(self):
        """Initialize the WebGUI class instance"""

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        self.logger.addHandler(ch)

        self.threadlock = threading.Lock()

        #
        # with open("../init.yml", "r") as conf_file:
        #     self.config = yaml.load(conf_file, Loader=yaml.FullLoader)
        #
        # self.num_vehicles = self.config["remoteConfig"]["numberOfVehicles"] + 1
        # self.totalPackets = self.config["remoteConfig"]["traceLength"] * (
        #     self.num_vehicles - 1
        # )

        self.received_packets = 0
        self.processed_packets = 0
        self.authenticated_packets = 0
        self.intact_packets = 0
        self.ontime_packets = 0

        self.logger.info("Initialized GUI")

    def update_vehicle(self, vehicle_id, lat, lng, icon_path):
        self.logger.info(f"moving vehicle {vehicle_id} to {lat}, {lng}")
        eel.updateMarker(vehicle_id, lat, lng, icon_path)

    def update_packet_counts(self, received, processed, authenticated, intact, ontime):
        self.logger.info("called update_packet_counts in python")
        self.received_packets = received
        self.processed_packets = processed
        self.authenticated_packets = authenticated
        self.intact_packets = intact
        self.ontime_packets = ontime

    def add_message(self, message):
        eel.addMessage(message)

    def prep(self):
        eel.init("web")

    def run(self):
        self.logger.info("called run, starting server")
        self.logger.info("starting for real")
        eel.start(
            "main.html",
            #mode="custom",
            #cmdline_args=["firefox", "http://localhost:8000"],
        )

    def start_receiver(self):
        self.logger.info("called start_receiver, creating socket")
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("127.0.0.1", 6666))

        # eel.spawn(self.update_stats_labels)
        label_thread = threading.Thread(target=self.update_stats_labels)
        label_thread.start()

        # eel.spawn(self.receive)
        self.receiver = threading.Thread(target=self.receive)
        self.receiver.start()

    def update_stats_labels(self):
        self.logger.info("starting update_stats_labels")

        while True:

            if self.received_packets == 0:
                continue

            eel.updatePacketCounts(
                self.received_packets,
                self.processed_packets,
                self.authenticated_packets,
                self.intact_packets,
                self.ontime_packets,
            )

            eel.sleep(0.1)

    def receive(self):
        self.logger.info("starting receive")

        # BUFFER_SIZE = 200

        # self.sock.listen(4)
        # conn = self.sock.accept()[0]

        while True:
            # try:
            msg = self.sock.recv(2048)
            data = struct.unpack("!5f??", msg)

            # data = json.loads(msg)

            self.logger.info("received data")

            # if not data["receiver"]:
            #     self.received_packets += 1
            #     self.intact_packets += 1

            if data[5]:
                self.authenticated_packets += 1

            if data[6]:
                self.ontime_packets += 1

            update = threading.Thread(
                target=self.process_new_packet,
                args=(
                    0,  # data["id"],
                    data[0],  # data["x"],
                    data[1],  # data["y"],
                    "N",  # TODO: fix this
                    # data[4],  # ["heading"],
                    data[5],  # data["sig"],
                    data[6],  # data["recent"],
                    False,  # data["receiver"],
                    999,  # data["elapsed"],
                ),
            )
            update.start()

            # except json.decoder.JSONDecodeError:
            #     self.logger.error("JSON decoding error, discarding invalid data")
            # except Exception as e:
            #     self.logger.error(f"exception: {e}")

    def process_new_packet(
        self,
        vehicle_id,
        lat,
        lng,
        heading,
        is_valid,
        is_recent,
        is_receiver,
        elapsed_time,
    ):
        self.logger.info(f"processing packet from {vehicle_id}")

        icon = ""
        if is_receiver:
            icon = f"/images/receiver/{heading}.png"
        elif is_valid:
            icon = f"/images/{heading}.png"
        else:
            icon = f"/images/phantom/{heading}.png"

        self.update_vehicle(vehicle_id, lat, lng, icon)

        # print messages to gui

        # acquire lock

        message = f"<p>Message from {vehicle_id}:</p>"
        if not is_receiver:
            if is_valid:
                message += '<p class="tab">✔️ Message successfully authenticated</p>'
            else:
                message += '<p class="tab">❌ Invalid signature!\n</p>'

            if is_recent:
                rounded_time = 0
                if elapsed_time > 0:
                    rounded_time = str(round(elapsed_time, 2))

                message += f'<p class="tab">✔️ Message is recent: {rounded_time} ms since transmission<p>'

            else:
                rounded_time = str(round(elapsed_time, 2))
                message += '<p class="tab">❌ Message is out-of-date: {rounded_time} ms since transmission<p>'

            if not is_valid and not is_recent:
                message += '<p class="tab">❌❌❌ Invalid signature and message expired, replay attack likely ❌❌❌</p>'

            message += f'<p class="tab">Vehicle reports location at {lat}, {lng} traveling {heading}<p>'
            self.add_message(message)

            self.processed_packets += 1
