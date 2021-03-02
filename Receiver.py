from scapy.all import sniff
import binascii
import json
from fastecdsa import keys, curve
from Verifier import Verifier
from threading import Thread
import socket


class Receiver:
    
    def __init__(self):
        self.verifier = Verifier()
        self.messageCounter = 1
        
    def run_receiver(self, s=None, lock=None, with_gui=False):
        if with_gui and (not s or not lock):
            print("Error - cannot run GUI without valid socket and thread lock. Exiting")
            exit(1)

        listener = Thread(target=self.listen_for_wsms(s, lock))
        listener.start()
        
    def listen_for_wsms(self, gui_socket, gui_socket_lock):

        print("Listening on localhost:4444 for WSMs")

        listener = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        listener.bind(('127.0.0.1', 4444))

        while True:
            wsm = listener.recv(1024)
            self.process_packet(wsm.hex()[118:], gui_socket, gui_socket_lock)

    def process_packet(self, payload, s, lock):

        print("Processing packet")
        print(payload)

        data = self.parse_wsm(payload)

        print(data)

        bsm_data = bytes.fromhex(data[0]).decode('ascii').replace("\n", "").split(",")

        decoded_data = {}
        
        decoded_data['id'] = bsm_data[0]
        decoded_data['x'] = bsm_data[1]
        decoded_data['y'] = bsm_data[2]
        decoded_data['heading'] = bsm_data[3]
        decoded_data['speed'] = bsm_data[4]
        
    
#       publicKey = keys.import_key("keys/" + decodedData['id'] + "/p256.pub",curve=curve.P256, public=True)
        public_key = keys.import_key("keys/0/p256.pub", curve=curve.P256, public=True)


        is_valid_sig = self.verifier.verify_signature(data[1], data[2], data[0], public_key)
        
        elapsed, is_recent = self.verifier.verify_time(data[3])
        
        decoded_data['sig'] = is_valid_sig
        decoded_data['elapsed'] = elapsed
        decoded_data['recent'] = is_recent
        decoded_data['receiver'] = False
                
        vehicle_data_json = json.dumps(decoded_data)
    
        if s == None or lock == None:
            self.terminal_out(vehicle_data_json)
        else:
            with lock:
                s.send(vehicle_data_json.encode())
    
    # takes the hex payload from an 802.11p frame as an argument, returns tuple of extracted bytestrings
    def parse_wsm(self, WSM):
        # The first 8 bytes are WSMP N/T headers that do not change in size and can be discarded
        ieee1609_dot2_data = WSM[20:]

        # First item to extract is the payload in unsecured data field
    
        # Note that the numbers for positions are double the byte value
        # because this is a string of "hex numbers" so 1 byte = 2 chars
    
        unsecured_data_length = int(ieee1609_dot2_data[12:14], 16)*2
        unsecured_data = ieee1609_dot2_data[14:14 + unsecured_data_length]
        time_position = 14 + unsecured_data_length + 6
        time = ieee1609_dot2_data[time_position:time_position + 16]
    
        # the ecdsaNistP256Signature structure is 66 bytes
        # r - 32 bytes
        # s - 32 bytes
        # field separators - 2 bytes
        signature = ieee1609_dot2_data[len(ieee1609_dot2_data)-(2*66):]
    
        # drop the two field identification bytes at the start of the block
        signature = signature[4:]
        
        # split into r and s
    
        r = signature[:64]
        s = signature[64:128]

        # convert from string into ten-bit integer
        r = int(r, 16)
        s = int(s, 16)
    
        r = int(str(r))
        s = int(str(s))
    
        return unsecured_data, r, s, time
    
    def terminal_out(self, vehicle_data_json):
        bsm = json.loads(vehicle_data_json)
        print("BSM: Position (" + str(bsm["x"]) + "," + str(bsm["y"]) +")" +
              "\tTraveling: " + bsm["heading"] + 
              "\tSpeed: " + bsm["speed"] +
              "\tExpired: " + str(not bsm["recent"]))
        print("Message is ", "validly" if bsm["sig"] else "NOT VALIDLY", "signed\n")
