import eel
import os
import pandas as pd


from src.Vehicle import Vehicle


def render_all_vehicles(vehicles: list[Vehicle]) -> None:
    eel.reset_markers()
    for v in vehicles:
        eel.add_new_vehicle(v.longitude, v.latitude, v.heading)
    eel.update_markers()


def main():

    # Initialize EEL
    eel.init(path='webapp',
             allowed_extensions=['.js', 'html', '.css'])

    # Start the webapp (will open in Chrome/Chromium)
    eel.start('osm-gui.html', block=False)

    vehicle_test_data = pd.read_excel(os.path.join(os.getcwd(),
                                                   'data',
                                                   'vehicle_test_data.xlsx')
                                      )

    vehicles = []

    for i in range(len(vehicle_test_data)):
        vehicles.append(Vehicle(longitude=vehicle_test_data.loc[i, 'longitude'],
                                latitude=vehicle_test_data.loc[i, 'latitude'],
                                heading=vehicle_test_data.loc[i, 'heading']))

    while True:
        eel.sleep(1)
        render_all_vehicles(vehicles)


if __name__ == "__main__":
    main()
