from scapy.all import sniff
import binascii
import json
from fastecdsa import keys, curve
from Verifier import Verifier
from threading import Thread


class Receiver:
    
    def __init__(self):
        self.verifier = Verifier()
        self.messageCounter = 1
        
    def run_receiver(self, s, lock):
        listener = Thread(target=self.listen_for_wsms(s, lock))
        listener.start()
        
    def listen_for_wsms(self, s, lock):

        print("Listening on localhost:4444 for WSMs")
    
        # port 4444 corresponds to UDP interface in wifi_rx.grc
        sniff(iface="lo", filter="dst port 4444", prn=lambda x: 
              self.filter_duplicate_packets(str(binascii.hexlify(x.load))[130:], s, lock))
    
    def filter_duplicate_packets(self, payload, s, lock):
        if self.messageCounter % 2 == 1:
            self.process_packet(payload, s, lock)
        self.messageCounter += 1

    def process_packet(self, payload, s, lock):
    
        data = self.parse_wsm(payload)

        bsm_data = bytes.fromhex(data[0]).decode('ascii').replace("\n", "").split(",")

        decoded_data = {}
        
        decoded_data['id'] = bsm_data[0]
        decoded_data['x'] = bsm_data[1]
        decoded_data['y'] = bsm_data[2]
        decoded_data['heading'] = bsm_data[3]
        decoded_data['speed'] = bsm_data[4]

        # public_key = keys.import_key("keys/" + decodedData['id'] + "/p256.pub",curve=curve.P256, public=True)
        public_key = keys.import_key("keys/0/p256.pub", curve=curve.P256, public=True)

        is_valid_sig = self.verifier.verify_signature(data[1], data[2], data[0], public_key)
        
        elapsed, is_recent = self.verifier.verify_time(data[3])
        
        decoded_data['sig'] = is_valid_sig
        decoded_data['elapsed'] = elapsed
        decoded_data['recent'] = is_recent
        decoded_data['receiver'] = False

        vehicle_data_json = json.dumps(decoded_data)
    
        with lock:
            s.send(vehicle_data_json.encode())
        
    # takes the hex payload from an 802.11p frame as an argument, returns tuple of extracted bytestrings
    def parse_wsm(self, WSM):
        # The first 8 bytes are WSMP N/T headers that do not change in size and can be discarded
        ieee1609_dot2_data = WSM[8:]

        # First item to extract is the payload in unsecured data field
    
        # Note that the numbers for positions are double the byte value
        # because this is a string of "hex numbers" so 1 byte = 2 chars
    
        unsecured_data_length = int(ieee1609_dot2_data[14:16],16)*2
        unsecured_data = ieee1609_dot2_data[16:16 + unsecured_data_length]
        time_position = 16 + unsecured_data_length + 6
        time = ieee1609_dot2_data[time_position:time_position + 16]

        # @TODO pull out cert

        # the ecdsaNistP256Signature structure is 66 bytes
        # r - 32 bytes
        # s - 32 bytes
        # field separators - 2 bytes
        signature = ieee1609_dot2_data[len(ieee1609_dot2_data)-(2*66)-1:]
    
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
