import v2v_security
import bsm
import fastecdsa.keys as keys
import socket


class Vehicle:

    def __init__(self):
        self.private_key, self.public_key = keys.import_key('keys/0/p256.key')

    def send_message(self):
        message = bsm.generate_16092_spdu(b'test', self.private_key)
        UDP_IP = "127.0.0.1"
        UDP_PORT = 52001
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.sendto(message, (UDP_IP, UDP_PORT))