##
# @file     gui.py
# @brief    Python program to launch and run the OSM-based GUI for V2Verifier


# Imports
import eel
import json
import pandas as pd
import threading

from pprint import pprint
from socket import *


class GUI:
    """! The GUI class to manage the interface"""

    def __init__(self):
        """! Initializer for the GUI"""
        self.vehicles = pd.DataFrame(columns=['id', 'latitude', 'longitude', 'elevation', 'speed', 'heading'])
        self.recv_port = 9999

        listener = threading.Thread(target=self.start_listener)
        listener.start()

    def update_vehicle(self, vehicle_info: dict):
        """! Updates information about vehicles in the system

        @param vehicle_info 
        """

        if self.vehicle_is_known(vehicle_info['id']):
            self.vehicles.loc[self.vehicles['id']==vehicle_info['id'], vehicle_info.keys()] = vehicle_info.values()
        else:
            new_record = pd.DataFrame(vehicle_info,index=[0])
            self.vehicles = pd.concat([self.vehicles, new_record]).reset_index(drop=True)

    def vehicle_is_known(self, id: int):
        return any([x == id for x in list(self.vehicles['id'])])

    def show_vehicles(self):
        pprint(self.vehicles)

    def set_up_vehicle_markers(self):
        for i in range(len(self.vehicles.index)):
            eel.add_new_vehicle(self.vehicles.loc[i,'longitude'],
                                self.vehicles.loc[i,'latitude'],
                                self.vehicles.loc[i,'heading'])

    def render_vehicle_markers(self):
        eel.add_vehicle_markers_to_map()

    def clear_vehicle_markers(self):
        eel.reset_markers()

    def start_listener(self):
        self.server_socket = socket(AF_INET, SOCK_DGRAM)
        self.server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

        self.server_socket.bind(('', self.recv_port))

        while True:
            message, address = self.server_socket.recvfrom(1024)
            print("Received:" + str(json.loads(message)))
            self.update_vehicle(json.loads(message))

def load_route_from_csv(filename: str):
    return pd.read_csv(filename)

def main():

    gui = GUI()

    # Initialize EEL
    eel.init(path='webapp',
             allowed_extensions=['.js', 'html', '.css'])

    # Start the webapp (will open in Chrome/Chromium)
    eel.start('osm-gui.html', block=False)

    while True:
        eel.sleep(0.1)
        gui.set_up_vehicle_markers()
        gui.render_vehicle_markers()
        eel.sleep(1)
        gui.show_vehicles()
        gui.clear_vehicle_markers()


if __name__ == "__main__":
    main()
