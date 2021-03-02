from Utility import Utility
import json
import time


def send_to_gui(messages, s, lock):

    for msg in messages:

        bsm = msg.split(",")

        decoded_data = {}

        decoded_data['id'] = bsm[0]
        decoded_data['x'] = bsm[1]
        decoded_data['y'] = bsm[2]
        decoded_data['heading'] = bsm[3]
        decoded_data['speed'] = bsm[4]

        decoded_data['sig'] = True
        decoded_data['elapsed'] = 0
        decoded_data['recent'] = True
        decoded_data['receiver'] = True

        vehicle_data_json = json.dumps(decoded_data)

        with lock:
            s.send(vehicle_data_json.encode())
        time.sleep(0.1)


class LocalVehicle:
    
    def __init__(self, local_trace_file):
        self.util = Utility()
        self.trace = local_trace_file
        
    def start(self, s, lock):
        messages = self.util.build_local_queue(self.trace)
        send_to_gui(messages, s, lock)
