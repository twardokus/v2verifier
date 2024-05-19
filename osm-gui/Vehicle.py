import json
import pandas as pd
import pyproj
import time
import threading

from dataclasses import dataclass
from socket import *

from Utility import Coordinate, generate_coordinate_trace


@dataclass
class BSM:
    id: int
    latitude: float
    longitude: float
    elevation: float
    speed: int
    heading: int


def bsm_to_json(bsm: dict) -> str:
    return json.dumps(bsm)


def dict_from_bsm(bsm: BSM) -> dict:
    return {'id': bsm.id,
            'latitude': bsm.latitude,
            'longitude': bsm.longitude,
            'elevation': bsm.elevation,
            'speed': bsm.speed,
            'heading': bsm.heading}


class Vehicle:

    id_incrementer = 0
    test_mode = False
    GUI_PORT = 9999

    def __init__(self, listen_port, transmit_port, trace_file: str):
        self.id = Vehicle.id_incrementer
        Vehicle.id_incrementer += 1

        self.elevation = 0
        self.speed = 30  # in km/hr
        self.heading = 0

        self.send_port = transmit_port
        self.recv_port = listen_port

        trace_coordinates = pd.read_csv(trace_file, header=None)
        coordinate_list = [Coordinate(trace_coordinates.iloc[i, 0], trace_coordinates.iloc[i, 1])
                           for i in range(0, len(trace_coordinates.index))]

        self.trace = generate_coordinate_trace(coordinate_list)

        self.pos_tracker = 0
        self.position = self.trace[self.pos_tracker]

        listen_thread = threading.Thread(target=self.start_listener)
        receive_thread = threading.Thread(target=self.start_transmitter)

        listen_thread.start()
        receive_thread.start()

        move_thread = threading.Thread(target=self.move, args=(1,))
        move_thread.start()

    def move(self, update_interval: int) -> None:
        while True:
            time.sleep(update_interval)
            self.update_position(update_interval)

    def generate_bsm(self) -> BSM:
        return BSM(id=self.id,
                   latitude=self.position.latitude,
                   longitude=self.position.longitude,
                   elevation=self.elevation,
                   speed=self.speed,
                   heading=self.heading)

    def start_listener(self):
        self.server_socket = socket(AF_INET, SOCK_DGRAM)
        self.server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

        self.server_socket.bind(('', self.recv_port))

        while True:
            message, address = self.server_socket.recvfrom(1024)

            # print(f"Vehicle {self.id} received: '{message}' from {address}")

            self.server_socket.sendto(message, address)

    def start_transmitter(self):
        self.client_socket = socket(AF_INET, SOCK_DGRAM)
        self.client_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

        while True:

            self.client_socket.settimeout(1)

            message = bsm_to_json(dict_from_bsm(self.generate_bsm()))
            addr = ("127.0.0.1", self.send_port)

            print("Transmitting: ", end="")
            print(message)

            start = time.time()
            self.client_socket.sendto(bytes(message, 'utf-8'), addr)
            time.sleep(1)

    def update_position(self, elapsed_time: float):  # elapsed time in seconds

        distance_covered_meters = int(round(((self.speed/(0.001 * 3600)) * elapsed_time), 0))
        distance_covered_interpolation_steps = int(round(distance_covered_meters/1.1))

        original_position = self.position

        next_position_index = self.pos_tracker + distance_covered_interpolation_steps
        if next_position_index >= len(self.trace):
            self.pos_tracker = 0
            self.position = self.trace[self.pos_tracker]
        else:
            self.position = self.trace[next_position_index]
            self.pos_tracker = next_position_index

        geodesic = pyproj.Geod(ellps='WGS84')
        fwd_azimuth, back_azimuth, distance = geodesic.inv(original_position.longitude,
                                                           original_position.latitude,
                                                           self.position.longitude,
                                                           self.position.latitude)

        # print(f"{fwd_azimuth}, {back_azimuth}, {distance}")
        self.heading = fwd_azimuth
        # print(self.position)
        # print(f"Current location: {self.position.latitude}, {self.position.longitude}")