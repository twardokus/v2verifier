"""
This script handles the USRP playing the "transmitter" role. The host that runs
wifi_tx.py should run this script.
"""

from transmitter import *

from threading import Thread
import os

if __name__ == "__main__":

    #attacker = Thread(target=sendPacketStream, args=("attacker",True,))
    #attacker.start()

    normal = Thread(target=sendPacketStream, args=("normal",False))
    normal.start()
