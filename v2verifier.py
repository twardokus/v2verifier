import v2verifier.Vehicle
import v2verifier.Utility
from fastecdsa import keys
import argparse


def process_args():
    """Wrapper for the argparse module"""

    parser = argparse.ArgumentParser(description="Run a V2V security experiment with V2Verifier")
    parser.add_argument("perspective",
                        help="choice of perspective",
                        choices=["receiver", "transmitter"]
                        )
    return parser.parse_args()


def transmit() -> None:
    """Run this V2Verifier instance as the BSM transmitter"""

    private, public = keys.import_key("keys/0/p256.key")
    vehicle = v2verifier.Vehicle.Vehicle(public, private)
    vehicle.run(mode="transmitter",
                pvm_list=v2verifier.Utility.read_data_from_file("test_gps_coords.csv"))


def receive() -> None:
    """Run this V2Verifier instance as the BSM receiver"""

    private, public = keys.import_key("keys/0/p256.key")
    vehicle = v2verifier.Vehicle.Vehicle(public, private)
    vehicle.run(mode="receiver", pvm_list=[])


if __name__ == "__main__":
    args = process_args()

    if args.perspective == "transmitter":
        transmit()

    if args.perspective == "receiver":
        receive()
