import time
import socket
import v2verifier.V2VReceive
import v2verifier.V2VTransmit
from fastecdsa import point


class Vehicle:
    """A class to represent a vehicle

    Attributes:
    ----------
    public_key : int
        the vehicle's public key
    private_key : int
        the vehicle's private key

    Methods
    -------
    run(pvm_list):
        Send a BSM every 100ms based on the data inputs of pvm_list

    """

    def __init__(self, public_key: point.Point, private_key: int) -> None:
        """Constructor for the vehicle class

        Parameters:
            public_key (fastecdsa.point.Point): the vehicle's public key
            private_key (int): the vehicle's private key

        Returns:
            None
        """

        self.public_key = public_key
        self.private_key = private_key

    def run(self, mode: str, pvm_list: list) -> None:
        """Launch the vehicle's BSM transmitter

        Parameters:
            mode (str): selection of "transmitter" or "receiver"
            pvm_list (list): a list of vehicle position/motion data elements

        Returns:
            None

        """

        if mode == "transmitter":
            for pvm_element in pvm_list:
                latitude, longitude, elevation, speed, heading = pvm_element.split(",")
                bsm = v2verifier.V2VTransmit.generate_v2v_bsm(float(latitude),
                                                              float(longitude),
                                                              float(elevation),
                                                              float(speed),
                                                              float(heading))
                spdu = v2verifier.V2VTransmit.generate_1609_spdu(bsm, self.private_key)
                print(spdu.hex())
                v2verifier.V2VTransmit.send_v2v_message(spdu, "localhost", 52001)
                time.sleep(0.1)

        elif mode == "receiver":
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.bind(("127.0.0.1", 4444))
            while True:
                data = sock.recv(2048)
                print(data[57:].hex())
                spdu_data = v2verifier.V2VReceive.parse_received_spdu(data[57:])
                print(v2verifier.V2VReceive.verify_spdu(spdu_data, self.public_key))
        else:
            raise Exception("Error - Vehicle.run() requires that mode be specified as either "
                            "\"transmitter\" or \"receiver\".")
