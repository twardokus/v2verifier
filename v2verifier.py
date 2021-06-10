import v2verifier.Vehicle
import v2verifier.Utility
import v2verifier.WebGUI
import v2verifier.TkGUI
import tkinter
from fastecdsa import keys
import argparse
import time
import threading
import sys
import yaml
from threading import Thread


welcome_message = "-"*30 + "\n"
welcome_message += "\""
welcome_message += "V2Verifier: A Testbed for V2V Security\n\n"
welcome_message += ""


def process_args():
    """Wrapper for the argparse module
    """

    parser = argparse.ArgumentParser(description=welcome_message)
    parser.add_argument("perspective",
                        help="choice of perspective",
                        choices=["receiver", "transmitter"]
                        )
    parser.add_argument("-t",
                        "--technology",
                        help="choice of technology",
                        choices=["dsrc", "cv2x"]
                        )
    parser.add_argument("-g",
                        "--with-gui",
                        help="option to launch GUI with receiver",
                        choices=["web", "tk"])
    parser.add_argument("--test",
                        help="run in test mode without SDRs or GNURadio",
                        action="store_true"
                        )
    return parser.parse_args()


def transmit(vehicle_index: int) -> None:
    """Run this V2Verifier instance as the BSM transmitter

    :param vehicle_index: an indicator of which vehicle this is, for use when multiple transmitters are requested
    :type vehicle_index: int
    """

    private, public = keys.import_key("keys/0/p256.key")
    vehicle = v2verifier.Vehicle.Vehicle(public, private)
    vehicle.run(mode="transmitter",
                tech="dsrc",
                pvm_list=v2verifier.Utility.read_data_from_file(config["scenario"]["traceFiles"][vehicle_index]),
                test_mode=args.test)


def receive(with_gui: bool = False, technology: str = "dsrc") -> None:
    """Run this V2Verifier instance as the BSM receiver

    :param with_gui: specify whether to launch GUI with receiver. Default is False (no GUI)
    :type with_gui: bool
    :param technology: choice of dsrc or c-v2x
    :type technology: str
    """

    if with_gui:
        if with_gui == "web":
            print("Launching V2Verifier receiver with WebGUI...")
            gui = v2verifier.WebGUI.WebGUI()
            gui.start_receiver()
            gui.prep()
            time.sleep(1)
            print("WebGUI initialized...")
            gui_thread = threading.Thread(target=gui.run)
            gui_thread.start()
            print("WebGUI launched successfully")
        else:
            print("TkGUI is not currently supported. For the time being, please use V2Verifier v1.1 or "
                  "use the new web-based GUI")
            sys.exit()
            # print("Launching V2Verifier receiver with TkGUI...")
            # gui = v2verifier.TkGUI.TkGUI()
            # gui_thread = threading.Thread(target=gui.run)
            # gui_thread.start()

    private, public = keys.import_key("keys/0/p256.key")
    vehicle = v2verifier.Vehicle.Vehicle(public, private)
    vehicle.run(mode="receiver", tech=technology, pvm_list=[], test_mode=args.test)


if __name__ == "__main__":
    args = process_args()

    with open("init.yml") as config_file:
        config = yaml.load(config_file, Loader=yaml.FullLoader)

    number_of_transmitters = int(config["scenario"]["numberOfVehicles"])
    if len(config["scenario"]["traceFiles"]) < number_of_transmitters:
        raise Exception("Error - too few trace files provided for requested number of vehicles.")

    if args.perspective == "transmitter":
        for i in range(0, number_of_transmitters):
            Thread(target=transmit, args=[i]).start()

    if args.perspective == "receiver":
        receive(with_gui=args.with_gui, technology=args.technology)
