"""
This script handles the USRP playing the "transmitter" role. The host that runs
wifi_tx.py should run this script.
"""

from transmitter import *

import os

if __name__ == "__main__":

    sendPacketStream()
