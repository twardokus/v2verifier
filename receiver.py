from verify import verifyMessage
from pcapParser import *
from fastecdsa import keys, curve

from scapy.all import *
import binascii

from time import sleep

pcapFileLocation = "/home/administrator/Desktop/out.pcap"

# load the public key - debugging
publicKey = keys.import_key("/home/administrator/v2v-capstone/keys/other_p256.pub",curve=curve.P256, public=True)

def processPacket(payload):
    #payload = str(binascii.hexlify(packet[Raw].load))
    data = extractData(payload)
    status = verifyMessage(data[1],data[2],data[0],publicKey)
    statusText = "valid" if status else "invalid"
    print "Message is " + statusText + ", contents: " + data[0].decode('hex').replace("\n","")

sniff(iface="lo", filter="udp and not icmp and port 4444", prn=lambda x: processPacket(str(binascii.hexlify(x.load))[130:]))

