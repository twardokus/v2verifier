import v2v_security
import bsm
import fastecdsa.keys as keys
import socket
from multiprocessing import Process, Lock
import time


class Vehicle:

    def __init__(self):
        self.private_key, self.public_key = keys.import_key('keys/0/p256.key')

        # variables for a UDP socket where BSMs are sent
        self.send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.SENDER_IP_TARGET = '127.0.0.1'
        self.SENDER_IP_PORT = 52001

    def run(self):
        sender = Process(target=self.send_bsms,)
        sender.start()

    def send_bsms(self):

        # self.send_socket.sendto(message, (self.SENDER_IP_TARGET, self.SENDER_IP_PORT))
