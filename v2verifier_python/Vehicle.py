import time
import socket
from threading import Thread

import yaml

import v2verifier_python.V2VReceive
import v2verifier_python.V2VTransmit
import v2verifier_python.Utility
from fastecdsa import point


class Vehicle:
    """A class to represent a vehicle.

    :param public_key: the vehicle's public key
    :type public_key: fastecdsa.point.Point
    :param private_key: the vehicle's private key
    :type private_key: int
    """

    def __init__(self, public_key: point.Point, private_key: int, hostname: str) -> None:
        """Constructor for the vehicle class

        :param public_key: the vehicle's public key
        :type public_key: fastecdsa.point.Point
        :param private_key: the vehicle's private key
        :type private_key: int
        """

        self.public_key = public_key
        self.private_key = private_key
        self.bsm_interval = 0.1  # interval specified in seconds, 0.1 -> every 100ms
        self.known_vehicles = {}
        self.local_id_counter = 0
        self.hostname = hostname

    def run(self, mode: str, tech: str, pvm_list: list, hostname: str, test_mode: bool = False) -> None:
        """Launch the vehicle

        :param mode: selection of "transmitter" or "receiver"
        :type mode: str
        :param tech: choice of DSRC or C-V2X as V2V communication technology
        :type tech: str
        :param pvm_list: a list of vehicle position/motion data elements
        :type pvm_list: list
        :param test_mode: indicate whether test mode (w/o USRPs and GNURadio) should be used. Affects ports used.
        :type test_mode: bool, optional
        """

        if mode == "transmitter":
            if tech == "cv2x":
                print("C-V2X is currently not supported")
                exit(1)
            else:
                for pvm_element in pvm_list:
                    latitude, longitude, elevation, speed, heading = pvm_element.split(",")
                    bsm = v2verifier_python.V2VTransmit.generate_v2v_bsm(float(latitude),
                                                                         float(longitude),
                                                                         float(elevation),
                                                                         float(speed),
                                                                         float(heading))

                spdu = v2verifier_python.V2VTransmit.generate_1609_spdu(bsm, self.private_key, hostname)

                    if test_mode:  # in test mode, send directly to receiver on port 4444
                        v2verifier_python.V2VTransmit.send_v2v_message(spdu, "localhost", 4444)
                    else:  # otherwise, send to wifi_tx.grc listener on port 52001 to become 802.11 payload
                        v2verifier_python.V2VTransmit.send_v2v_message(spdu, "localhost", 52001)

                    time.sleep(self.bsm_interval)

        elif mode == "receiver":
            local_vehicle = Thread(target=self.run_self, args=[test_mode])
            local_vehicle.start()

            if tech == "dsrc":
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.bind(("127.0.0.1", 4444))
                while True:
                    data = sock.recv(2048)

                    if test_mode:  # in test mode, there are no 802.11 headers, so parse all received data
                        spdu_data = v2verifier_python.V2VReceive.parse_received_spdu(data)
                    else:  # otherwise (i.e., w/ GNURadio), 802.11 PHY/MAC headers must be stripped before parsing SPDU
                        spdu_data = v2verifier_python.V2VReceive.parse_received_spdu(data[57:])

                    verification_data = v2verifier_python.V2VReceive.verify_spdu(spdu_data, self.public_key)

                    bsm_data_tuple = v2verifier_python.V2VReceive.extract_bsm_data(spdu_data["tbs_data"]["unsecured_data"],
                                                                                   verification_data)
                    self.update_known_vehicles(spdu_data["certificate"]["hostname"], bsm_data_tuple,
                                               verification_data)

                    print(v2verifier_python.V2VReceive.get_bsm_report(spdu_data["tbs_data"]["unsecured_data"],
                                                                      verification_data))
                    v2verifier_python.V2VReceive.report_bsm_gui(bsm_data_tuple, verification_data, "127.0.0.1", 6666,
                                                                self.get_vehicle_number_by_id(
                                                             spdu_data["certificate"]["hostname"]
                                                         )
                                                                )

# =======             
                    # bsm_data_tuple = v2verifier_python.V2VReceive.extract_bsm_data(spdu_data["tbs_data"]["unsecured_data"], verification_data)
                    # self.update_known_vehicles(spdu_data["certificate"]["hostname"], bsm_data_tuple, verification_data)

                    # print(v2verifier_python.V2VReceive.get_bsm_report(spdu_data["tbs_data"]["unsecured_data"], verification_data))
                    # v2verifier_python.V2VReceive.report_bsm_gui(bsm_data_tuple, verification_data, "127.0.0.1", 6666)
# >>>>>>> cv2x-integration
            elif tech == "cv2x":
                print("C-V2X is currently not supported")
                exit(1)
            elif tech == "cohda":
                # use IPv6 on the Ethernet interface to get messages from COTS device
                sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
                sock.bind(("fe80::ca89:f53:4108:d142%enp3s0", 4444, 0, 2))
                while True:
                    data = sock.recv(2048)
                    bsm_data = v2verifier_python.V2VReceive.parse_received_cv2x_spdu(data)

                    # v2verifier_python.V2VReceive.parse_received_cv2x_spdu() returns empty dict if
                    # the SPDU is below a certain length threshold. This prevents attempting
                    # to parse non-BSMs, e.g., control messages, as if they were BSMs
                    if bsm_data == {}:
                        continue

                    print(v2verifier_python.V2VReceive.report_cots_cv2x_bsm(bsm_data))
            else:
                raise Exception("Technology must be specified as \"dsrc\" or \"cv2x\".")

        else:
            raise Exception("Error - Vehicle.run() requires that mode be specified as either "
                            "\"transmitter\" or \"receiver\".\nCheck your inputs and try again.")

    def update_known_vehicles(self, id: str, bsm_data: tuple, verification_data: dict) -> None:
        """Update the vehicle's threat tracking \"database\"

        :param id: the vehicle identifier from the BSM
        :type id: str
        :param bsm_data: BSM data from an SPDU
        :type bsm_data: tuple
        :param verification_data: security information from verify_spdu()
        :type verification_data: dict
        """

        # don't show the local vehicle as a remote one
        if id != b'reserved9999':

            if id not in self.known_vehicles.keys():
                self.known_vehicles[id] = {"id_number": self.local_id_counter}
                self.local_id_counter += 1

            self.known_vehicles[id]["latitude"] = bsm_data[0]
            self.known_vehicles[id]["longitude"] = bsm_data[1]
            self.known_vehicles[id]["elevation"] = bsm_data[2]
            self.known_vehicles[id]["speed"] = bsm_data[3]
            self.known_vehicles[id]["heading"] = bsm_data[4]

            self.known_vehicles[id]["signature_type"] = verification_data["signature_type"]
            self.known_vehicles[id]["valid_signature"] = verification_data["valid_signature"]
            self.known_vehicles[id]["unexpired"] = verification_data["unexpired"]
            self.known_vehicles[id]["elapsed"] = verification_data["elapsed"]

    def get_vehicle_number_by_id(self, id_number: str):
        if id_number == b'reserved9999':
            return 99
        else:
            return self.known_vehicles[id_number]["id_number"]

    def report_known_vehicles(self):
        """Print out report of all known vehicles and all data elements for each known vehicle
        """
        for vehicle in self.known_vehicles.keys():
            print("Vehicle: ", vehicle)
            for item in self.known_vehicles[vehicle]:
                print("\t", item, self.known_vehicles[vehicle][item])

    def run_self(self, test_mode=False):
        print("Running self")
        with open("init.yml") as config_file:
            config = yaml.load(config_file, Loader=yaml.FullLoader)

        pvm_list = v2verifier_python.Utility.read_data_from_file("trace_files/" + config["local"]["tracefile"])
        for pvm_element in pvm_list:
            latitude, longitude, elevation, speed, heading = pvm_element.split(",")
            bsm = v2verifier_python.V2VTransmit.generate_v2v_bsm(float(latitude),
                                                                 float(longitude),
                                                                 float(elevation),
                                                                 float(speed),
                                                                 float(heading))

            spdu = v2verifier_python.V2VTransmit.generate_1609_spdu(bsm, self.private_key, "reserved9999")
            if not test_mode:
                spdu = b'\xFE'*57 + spdu

            v2verifier_python.V2VTransmit.send_v2v_message(spdu, "localhost", 4444)

            time.sleep(self.bsm_interval)
