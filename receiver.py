from verify import verifyMessage
from pcapParser import *
from fastecdsa import keys, curve

from scapy.all import *
import binascii

pcapFileLocation = "/home/administrator/Desktop/out.pcap"

# load the public key - debugging
publicKey = keys.import_key("/home/administrator/v2v-capstone/keys/other_p256.pub",curve=curve.P256, public=True)


# get the packets
packets = parsePcapFile(pcapFileLocation)

for packet in packets:
    
    payload = str(binascii.hexlify(packet[Raw].load))
    data = extractData(payload)

    status = verifyMessage(data[1],data[2],data[0],publicKey)


