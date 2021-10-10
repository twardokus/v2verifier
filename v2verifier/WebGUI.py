import eel
import threading
import socket
import logging
import struct


class WebGUI:
    """A class to represent the Web-based V2Verifier GUI

    :param enable_logging: choice of whether to enable console logging for GUI, defaults to False
    :type enable_logging: bool
    """

    def __init__(self, enable_logging: bool = False):
        """WebGUI constructor
        """

        self.logging_enabled = True if enable_logging else False

        if self.logging_enabled:
            self.logger = logging.getLogger(__name__)
            self.logger.setLevel(logging.INFO)
            ch = logging.StreamHandler()
            ch.setLevel(logging.INFO)
            self.logger.addHandler(ch)

        self.receive_socket = None
        self.thread_lock = threading.Lock()

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
        self.on_time_packets = 0

        if self.logging_enabled:
            self.logger.info("Initialized GUI")

    def update_vehicle(self, vehicle_id: int, latitude: float, longitude: float, icon_path: str) -> None:
        """Update the GUI marker for a given vehicle

        :param vehicle_id: the ID number of the vehicle whose marker is being updated
        :type vehicle_id: int
        :param latitude: the new latitude where the marker should be placed
        :type latitude: float
        :param longitude: the new longitude where the marker should be placed
        :type longitude: float
        :param icon_path: the file path to an image to use as the marker on the map
        :type icon_path: str
        """
        if self.logging_enabled:
            self.logger.info(f"moving vehicle {vehicle_id} to {latitude}, {longitude}")

        # EEL exposes this function in main.html
        eel.updateMarker(vehicle_id, latitude, longitude, icon_path)

    def add_message(self, message: str) -> None:
        """Wrapper method for eel.addMessage() exposed in main.html

        :param message: the message that EEL should render on the GUI
        :type message: str
        """
        eel.addMessage(message)

    def prep(self):
        """Wrapper method for eel.init() to initialize EEL in this project's web directory
        """
        eel.init("web")

    def run(self) -> None:
        """Launch the EEL GUI by opening main.html in a web browser (Chrome) window
        """
        if self.logging_enabled:
            self.logger.info("called run, starting server")
            self.logger.info("starting for real")

        eel.start(
            "main.html"
        )

    def start_receiver(self) -> None:
        """Initialize web sockets to receive BSM data from V2Verifier and launch threads to receive/render data
        """
        if self.logging_enabled:
            self.logger.info("called start_receiver, creating socket")

        self.receive_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.receive_socket.bind(("127.0.0.1", 6666))

        label_thread = threading.Thread(target=self.update_stats_labels)
        label_thread.start()

        receiver = threading.Thread(target=self.receive)
        receiver.start()

    def update_stats_labels(self) -> None:
        """Continuously update the packet statistics displayed on the GUI
        """

        if self.logging_enabled:
            self.logger.info("starting update_stats_labels")

        while True:

            if self.received_packets == 0:
                continue

            # exposed by EEL in main.html
            eel.updatePacketCounts(
                self.received_packets,
                self.processed_packets,
                self.authenticated_packets,
                self.intact_packets,
                self.on_time_packets,
            )

            eel.sleep(0.1)

    def receive(self) -> None:
        """Listen for BSM data being sent from V2Verifier receiver and spawn thread to update rendered data
        accordingly
        """
        if self.logging_enabled:
            self.logger.info("starting receive")

        while True:
            msg = self.receive_socket.recv(2048)
            data = struct.unpack("!5f??f", msg)

            if self.logging_enabled:
                self.logger.info("received data")

            self.received_packets += 1

            if data[5]:
                self.authenticated_packets += 1
                self.intact_packets += 1

            if data[6]:
                self.on_time_packets += 1

            update = threading.Thread(
                target=self.process_new_packet,
                args=(
                    0,  # data["id"], #TODO also fix this
                    data[0],  # latitude (formerly data["x"])
                    data[1],  # longitude (formerly data["y"])
                    data[2],  # elevation
                    data[3],  # speed
                    "N",  # TODO: fix this
                    # data[4],  # heading (formerly ["heading"])
                    data[5],  # valid_signature (formerly data["sig"])
                    data[6],  # unexpired (formerly data["recent"])
                    False,  # data["receiver"]
                    data[7],  # elapsed_time (formerly data["elapsed"])
                ),
            )
            update.start()

    def process_new_packet(self, vehicle_id: int, latitude: float, longitude: float, elevation: float,
                           speed: float, heading: float, is_valid: bool, is_recent: bool, is_receiver: bool,
                           elapsed_time: float) -> None:
        """Method to render data from a BSM on the GUI

        :param vehicle_id: the ID number of the vehicle which sent the message
        :type vehicle_id: int
        :param latitude: the reported latitude
        :type latitude: float
        :param longitude: the reported longitude
        :type longitude: float
        :param elevation: the reported elevation
        :type elevation: float
        :param speed: the reported speed of travel
        :type speed: float
        :param heading: the reported heading (direction of travel)
        :type heading: float
        :param is_valid: result of message verification
        :type is_valid: bool
        :param is_recent: result of message timestamp verification
        :type is_recent: bool
        :param is_receiver: True if the sender of the message is the receiver (for representing local vehicle)
        :type is_receiver: bool
        :param elapsed_time: the time elapsed between the BSM's generation time and the time this method is called
        :type elapsed_time: float
        """

        if self.logging_enabled:
            self.logger.info(f"processing packet from {vehicle_id}")

        icon = ""
        if is_receiver:
            icon = f"/images/receiver/{heading}.png"
        elif is_valid:
            icon = f"/images/regular/{heading}.png"
        else:
            icon = f"/images/phantom/{heading}.png"

        self.update_vehicle(vehicle_id, latitude, longitude, icon)

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

            message += f'<p class="tab">Vehicle reports location at {latitude}, {longitude} traveling {heading}<p>'
            self.add_message(message)

            self.processed_packets += 1
