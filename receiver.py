from verify import verifyMessage
from pcapParser import *
from fastecdsa import keys, curve

from scapy.all import *
import binascii

from time import sleep

from socket import AF_INET, SOCK_STREAM
import math

# load the public key of the other "vehicle" (the host connected to the other USRP)
publicKey = keys.import_key("/home/administrator/v2v-capstone/keys/other_p256.pub",curve=curve.P256, public=True)


def processPacket(payload,s,lock):
    
    data = extractData(payload)
    
    status = verifyMessage(data[1],data[2],data[0],publicKey)
    statusText = "valid" if status else "invalid"

    vehicleData = data[0].decode('hex').replace("\n","")
    vehicleData += "," + "True" if int(status) else "False"

    with lock:
        s.send(vehicleData.encode())

def runSelf(vehicleNo, socket, lock):

    trace = open("v" + str(vehicleNo) + "path")
    for i in range(0,400):
        vehicleData = str(vehicleNo) + "," + trace.readline()
        vehicleData += ",True"

        #data = vehicleData.split(",")

        sleep(0.5)

        #data[1] = str(abs(int(data[1])))
        #data[2] = str(int(data[2]) - 3580)

        #vehicleData = ",".join(data)

        with lock:
#            print "Sending own data "
#            print vehicleData
            socket.send(vehicleData.replace("\n","").encode())

def listen(s,lock):

#    s = socket.socket()
#    s.connect(('127.0.0.1',6666))
    print "Listening"
    sniff(iface="lo", filter="udp and port 4444", prn=lambda x: processPacket(str(binascii.hexlify(x.load))[130:],s,lock))

