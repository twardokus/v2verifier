import eel
import json
import os
import pandas as pd
from pprint import pprint

# def render_all_vehicles(vehicles: pd.DataFrame) -> None:
#     """ Clear existing vehicle markers and generate new markers by invoking JS functions via EEL
#
#     :param vehicles: DataFrame storing the vehicles represented in the GUI
#     :return: None
#     """
#     eel.reset_markers()
#     for i in range(len(vehicles)):
#         eel.add_new_vehicle(vehicles.loc[i, 'longitude'],
#                             vehicles.loc[i, 'latitude'],
#                             vehicles.loc[i, 'heading'].astype(float))
#     eel.update_markers()
#
#
# def update_vehicles_from_json(vehicle_json_data: dict, vehicles: pd.DataFrame) -> pd.DataFrame:
#     """ Update vehicles tracked in the GUI from JSON input data. JSON is expected to be a
#         dictionary parsed out of JSON with a single key (`vehicles`) that maps to a list of
#         dictionaries of vehicle data, where each dictionary contains an id_number,
#         longitude, latitude, and heading value for one vehicle.
#
#     :param vehicle_json_data: dictionary extracted from JSON containing an array of vehicle data
#     :param vehicles: DataFrame used to track vehicles represented on the GUI
#     :return: an updated copy of vehicles with the new information included
#     """
#
#     v_df = pd.DataFrame(vehicle_json_data['vehicles'])
#
#     # For each vehicle that we got new information about in the JSON
#     for i in range(len(v_df)):
#
#         # If this is a new vehicle, make note of it
#         if not v_df.loc[i, 'id_number'] in list(vehicles['id_number']):
#             vehicles.loc[len(vehicles.index)] = [v_df.loc[i, 'id_number'],
#                                                  v_df.loc[i, 'latitude'],
#                                                  v_df.loc[i, 'longitude'],
#                                                  v_df.loc[i, 'heading']]
#
#         # Otherwise, update the relevant row in the vehicles DataFrame
#         else:
#             v_idx = vehicles[vehicles['id_number'] == v_df.loc[i, 'id_number']].index
#
#             vehicles.loc[v_idx] = v_df.loc[i,:].tolist()
#
#     return vehicles
class GUI:

    def __init__(self):
        self.vehicles = pd.DataFrame(columns=['id_number', 'latitude', 'longitude', 'heading'])

    def update_vehicle(self, vehicle_info: dict):
        if self.vehicle_is_known(vehicle_info['id_number']):
            self.vehicles.loc[self.vehicles['id_number']==vehicle_info['id_number']] = [pd.Series(vehicle_info)]
        else:
            new_record = pd.DataFrame(vehicle_info,index=[0])
            self.vehicles = pd.concat([self.vehicles, new_record]).reset_index(drop=True)

    def vehicle_is_known(self, id: int):
        return any([x == id for x in list(self.vehicles['id_number'])])

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

def load_route_from_csv(filename: str):
    return pd.read_csv(filename)

def main():

    gui = GUI()
    # gui.update_vehicle({'id_number': 1,
    #                     'latitude': 43.081062,
    #                     'longitude': -77.671297,
    #                     'heading': 120})
    # gui.show_vehicles()
    # gui.update_vehicle({'id_number': 2,
    #                     'latitude': 43.081062,
    #                     'longitude': -77.681397,
    #                     'heading': 120})
    # gui.show_vehicles()

    route_df = load_route_from_csv("data/out.csv")
    route2_df = load_route_from_csv("data/out2.csv")
    route3_df = load_route_from_csv("data/out3.csv")

    # Initialize EEL
    eel.init(path='webapp',
             allowed_extensions=['.js', 'html', '.css'])

    # Start the webapp (will open in Chrome/Chromium)
    eel.start('osm-gui.html', block=False)

    counter1 = 0
    counter2 = 0
    counter3 = 0

    orig = True
    while True:
        eel.sleep(0.1)

        # Vehicle 0
        gui.update_vehicle({'id_number': 0,
                            'latitude': route_df.loc[counter1, 'lat'],
                            'longitude': route_df.loc[counter1, 'lon'],
                            'heading': 0})

        if orig:
            counter1 += 1
        else:
            counter1 -= 1

        if counter1 >= len(route_df.index):
            counter1 -= 1
            orig = False

        if counter1 < 0:
            counter1 += 1
            orig = True

        # Vehicle 2
        gui.update_vehicle({'id_number': 1,
                            'latitude': route2_df.loc[counter2, 'lat'],
                            'longitude': route2_df.loc[counter2, 'lon'],
                            'heading': 0})

        if orig:
            counter2 += 1
        else:
            counter2 -= 1

        if counter2 >= len(route2_df.index):
            counter2 -= 1
            orig = False

        if counter2 < 0:
            counter2 += 1
            orig = True

        # Vehicle 3
        gui.update_vehicle({'id_number': 2,
                            'latitude': route3_df.loc[counter3, 'lat'],
                            'longitude': route3_df.loc[counter3, 'lon'],
                            'heading': 0})
        if orig:
            counter3 += 1
        else:
            counter3 -= 1

        if counter3 >= len(route3_df.index):
            counter3 -= 1
            orig = False

        if counter3 < 0:
            counter3 += 1
            orig = True

        # eel.add_new_vehicle(1,1,1)
        gui.set_up_vehicle_markers()
        # eel.add_vehicle_markers_to_map()
        gui.render_vehicle_markers()
        eel.sleep(1)
        # eel.reset_markers()
        gui.clear_vehicle_markers()
        # eel.sleep(0)


if __name__ == "__main__":
    main()
