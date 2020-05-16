from verify import verifyMessage
from pcapParser import *
from fastecdsa import keys, curve

from scapy.all import *
import binascii

from time import sleep

from socket import AF_INET, SOCK_STREAM
import math
import random

# load the public key of the other "vehicle" (the host connected to the other USRP)
publicKey = keys.import_key("/home/administrator/v2v-capstone/keys/other_p256.pub",curve=curve.P256, public=True)

"""
Function to extract the data string (format id,x-coord,y-coord) from the 
payload of the received DSRC message

Inputs:

payload -   the hexadecimal string representing everything above Layer 2,
            i.e. the WSMP message and embedded ieee1609Dot2Data structure
s       -   a TCP socket connected to the GUI application
lock    -   a thread lock passed from rxMain.py
"""

def processPacket(payload,s,lock):
    
    data = extractData(payload)
    
    status = verifyMessage(data[1],data[2],data[0],publicKey)
    statusText = "valid" if status else "invalid"

    vehicleData = data[0].decode('hex').replace("\n","")
    vehicleData += "," + "True" if int(status) else "False"

    with lock:
        s.send(vehicleData.encode())

"""
Function to send data about the receiver's "vehicle" to the GUI application

Inputs:

vehicleNo   - the id number, used to open the correct trace file
socket      - the TCP socket connected to the GUI application
lock        - a thread lock passed from rxMain.py
"""
def runSelf(vehicleNo, socket, lock):

    trace = open("v" + str(vehicleNo) + "path")

    for i in range(0,400):
        vehicleData = str(vehicleNo) + "," + trace.readline()
        vehicleData += ",True"

        # sleeping for 0.5 seconds keeps the display update rate reasonable
        sleep(0.5)

        with lock:
            socket.send(vehicleData.replace("\n","").encode())

def runSelfAndOthers(socket, lock):

    NUM_VEHICLES = 4
    vehicleIDs = []

    for i in range(1,NUM_VEHICLES):
        vehicleIDs.append(i)    

    traces = []
    for i in range(1,NUM_VEHICLES):
        traceFile = open("v" + str(i) + "path")
        trace = []
        for j in range(0,400):
            #if j % random.randint(1,10) == 0 and i == random.randint(1,NUM_VEHICLES):
            #    vehicleData = str(i) + "," + traceFile.readline().replace("\n","") + ",False"
            #else:
            vehicleData = str(i) + "," + traceFile.readline().replace("\n","") + ",True"
            trace.append(vehicleData)
        traces.append(trace)

#    print traces
    for i in range(0,400):
        random.shuffle(vehicleIDs)
        for currentID in vehicleIDs:
            print vehicleIDs
            sleep(0.1)
            with lock:
                print traces[currentID-1][i]
                socket.send(traces[currentID-1][i].encode())
        


def listen(s,lock):

    # print a console message to confirm the network connection is active
    print "Listening"

    # listen on localhost:4444 which is the UDP sink from GNURadio in wifi_rx.py
    # received packets are passed to processPacket() for data extraction
    sniff(iface="lo", filter="udp and port 4444", prn=lambda x: processPacket(str(binascii.hexlify(x.load))[130:],s,lock))

if __name__ == "__main__":
    runSelfAndOthers(None, None)
