import v2verifier.Vehicle
import v2verifier.Utility
import v2verifier.WebGUI
from fastecdsa import keys
import argparse
import time
import threading
import sys


def process_args():
    """Wrapper for the argparse module"""

    parser = argparse.ArgumentParser(description="Run a V2V security experiment with V2Verifier")
    parser.add_argument("perspective",
                        help="choice of perspective",
                        choices=["receiver", "transmitter"]
                        )
    parser.add_argument("-g",
                        "--with-gui",
                        help="option to launch GUI with receiver",
                        action="store_true")
    parser.add_argument("-t",
                        "--test",
                        help="run in test mode without SDRs or GNURadio",
                        action="store_true"
                        )
    return parser.parse_args()


def transmit() -> None:
    """Run this V2Verifier instance as the BSM transmitter"""

    private, public = keys.import_key("keys/0/p256.key")
    vehicle = v2verifier.Vehicle.Vehicle(public, private)
    vehicle.run(mode="transmitter",
                pvm_list=v2verifier.Utility.read_data_from_file("test_gps_coords.csv"),
                test_mode=args.test)


def receive(with_gui: bool = False) -> None:
    """Run this V2Verifier instance as the BSM receiver

    Parameters:
        with_gui (bool): specify whether to launch GUI with receiver. Default is False (no GUI)

    """

    if with_gui:
        print("Launching V2Verifier receiver with GUI...")
        gui = v2verifier.WebGUI.WebGUI()
        gui.start_receiver()
        gui.prep()
        time.sleep(1)
        print("GUI initialized...")
        gui_thread = threading.Thread(target=gui.run)
        gui_thread.start()
        print("GUI launched successfully")

    private, public = keys.import_key("keys/0/p256.key")
    vehicle = v2verifier.Vehicle.Vehicle(public, private)
    vehicle.run(mode="receiver", pvm_list=[], test_mode=args.test)


if __name__ == "__main__":
    args = process_args()

    if args.perspective == "transmitter":
        transmit()

    if args.perspective == "receiver":
        receive(args.with_gui)