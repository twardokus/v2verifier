import eel
import json
import os
import pandas as pd


def render_all_vehicles(vehicles: pd.DataFrame) -> None:
    """ Clear existing vehicle markers and generate new markers by invoking JS functions via EEL

    :param vehicles: DataFrame storing the vehicles represented in the GUI
    :return: None
    """
    eel.reset_markers()
    for i in range(len(vehicles)):
        eel.add_new_vehicle(vehicles.loc[i, 'longitude'],
                            vehicles.loc[i, 'latitude'],
                            vehicles.loc[i, 'heading'].astype(float))
    eel.update_markers()


def update_vehicles_from_json(vehicle_json_data: dict, vehicles: pd.DataFrame) -> pd.DataFrame:
    """ Update vehicles tracked in the GUI from JSON input data. JSON is expected to be a
        dictionary parsed out of JSON with a single key (`vehicles`) that maps to a list of
        dictionaries of vehicle data, where each dictionary contains an id_number,
        longitude, latitude, and heading value for one vehicle.

    :param vehicle_json_data: dictionary extracted from JSON containing an array of vehicle data
    :param vehicles: DataFrame used to track vehicles represented on the GUI
    :return: an updated copy of vehicles with the new information included
    """

    v_df = pd.DataFrame(vehicle_json_data['vehicles'])

    # For each vehicle that we got new information about in the JSON
    for i in range(len(v_df)):

        # If this is a new vehicle, make note of it
        if not v_df.loc[i, 'id_number'] in list(vehicles['id_number']):
            vehicles.loc[len(vehicles.index)] = [v_df.loc[i, 'id_number'],
                                                 v_df.loc[i, 'latitude'],
                                                 v_df.loc[i, 'longitude'],
                                                 v_df.loc[i, 'heading']]

        # Otherwise, update the relevant row in the vehicles DataFrame
        else:
            v_idx = vehicles[vehicles['id_number'] == v_df.loc[i, 'id_number']].index

            vehicles.loc[v_idx] = v_df.loc[i,:].tolist()

    return vehicles


def main():
    # Initialize EEL
    eel.init(path='webapp',
             allowed_extensions=['.js', 'html', '.css'])

    # Start the webapp (will open in Chrome/Chromium)
    eel.start('osm-gui.html', block=False)


    while True:
        eel.sleep(1)
        eel.add_new_vehicle(1,1,1)
        eel.add_vehicle_markers_to_map()
        eel.sleep(1)
        eel.reset_markers()
        eel.sleep(1)


if __name__ == "__main__":
    main()
