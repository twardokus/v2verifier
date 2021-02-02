import v2v_security
import bsm
import fastecdsa.keys as keys
import socket
import time

from multiprocessing import Process, Lock


class Vehicle:

    def __init__(self):
        self.private_key, self.public_key = keys.import_key('keys/0/p256.key')

        # variables for a UDP socket where BSMs are sent
        self.send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.SENDER_IP_TARGET = '127.0.0.1'
        self.SENDER_IP_PORT = 52001
        self.RECEIVER_IP_TARGET = '127.0.0.1'
        self.RECEIVER_IP_PORT = 4444

    """
    Follow up on sending functionality after receiving is implemented
    def run(self):
        # sender = Process(target=self.send_bsms,)
        # sender.start()


    

    def send_bsms(self):
        while(True):
            bsm = self.generate_bsm()
            self.send_socket.sendto(bsm, (self.SENDER_IP_TARGET,
                                          self.SENDER_IP_PORT))
            time.wait(0.1)

    def generate_bsm(self):
    """

    def receive_bsms(self):
        receive_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        receive_socket.bind((self.RECEIVER_IP_TARGET, self.RECEIVER_IP_PORT))

        while True:
            bsm = receive_socket.recv(1024)
            print(bsm)
            print()
