import eel
import json
import os
import pandas as pd


from src.Vehicle import Vehicle


def render_all_vehicles(vehicles: list[Vehicle]) -> None:
    """ Clear existing vehicle markers and generate new markers by invoking JS functions via EEL

    :param vehicles: list of vehicles that are represented in the GUI
    :return: None
    """
    eel.reset_markers()
    for v in vehicles:
        eel.add_new_vehicle(v.longitude, v.latitude, v.heading)
    eel.update_markers()


def update_vehicles_from_json(vehicle_json_data: dict, vehicles: list[Vehicle]) -> list[Vehicle]:
    """Test"""

    v_df = pd.DataFrame(vehicle_json_data['vehicles'])

    for i in range(len(v_df)):
        if not v_df.loc[i, 'id_number'] in [x.id_number for x in vehicles]:
            vehicles.append(Vehicle(id_number=v_df.loc[i, 'id_number'],
                                    longitude=v_df.loc[i, 'longitude'],
                                    latitude=v_df.loc[i, 'latitude'],
                                    heading=v_df.loc[i, 'heading']
                                    ))
        else:
            for j in range(len(vehicles)):
                if vehicles[j].id_number == v_df.loc[i, 'id_number']:
                    vehicles[j].update_position(new_longitude=v_df.loc[i, 'longitude'],
                                                new_latitude=v_df.loc[i, 'latitude'],
                                                new_heading=v_df.loc[i, 'heading'])
                    break
    return vehicles


def main():
    # Initialize EEL
    eel.init(path='webapp',
             allowed_extensions=['.js', 'html', '.css'])

    # Start the webapp (will open in Chrome/Chromium)
    eel.start('osm-gui.html', block=False)

    vehicle_test_data = pd.read_excel(os.path.join(os.getcwd(), 'data', 'vehicle_test_data.xlsx'))

    vehicles = []

    for i in range(len(vehicle_test_data)):
        vehicles.append(Vehicle(id_number=vehicle_test_data.loc[i, 'vehicle_number'],
                                longitude=vehicle_test_data.loc[i, 'longitude'],
                                latitude=vehicle_test_data.loc[i, 'latitude'],
                                heading=vehicle_test_data.loc[i, 'heading']))

    while True:
        eel.sleep(3)
        render_all_vehicles(vehicles)
        with open(os.path.join(os.getcwd(), "data", "vehicle_update.json")) as infile:
            data = json.load(infile)
        vehicles = update_vehicles_from_json(data, vehicles)


if __name__ == "__main__":
    main()
