from verify import verifyMessage
from pcapParser import *
from fastecdsa import keys, curve

from scapy.all import *
import binascii

from time import sleep

from socket import AF_INET, SOCK_STREAM


pcapFileLocation = "/home/administrator/Desktop/out.pcap"

# load the public key
publicKey = keys.import_key("/home/administrator/v2v-capstone/keys/other_p256.pub",curve=curve.P256, public=True)

def processPacket(payload,s):
    data = extractData(payload)
    status = verifyMessage(data[1],data[2],data[0],publicKey)
    statusText = "valid" if status else "invalid"

    result = "Message is " + statusText + ", contents: " + data[0].decode('hex').replace("\n","")
    


    vehicleData = data[0].decode('hex').replace("\n","")
#    print vehicleData

#    fields = vehicleData.split(",")

#    print(fields)

#    result = carID, mssafge, x, y
#    fields = data[0].split(",")
    
    #s = socket.socket()
    #s.connect(('127.0.0.1',6666))
    
    s.send(vehicleData.encode())
    
    #s.shutdown(socket.SHUT_RDWR)
    #s.close()


s = socket.socket()
s.connect(('127.0.0.1',6666))


#    print "Message is " + statusText + ", contents: " + data[0].decode('hex').replace("\n","")

sniff(iface="lo", filter="udp and port 4444", prn=lambda x: processPacket(str(binascii.hexlify(x.load))[130:],s))


