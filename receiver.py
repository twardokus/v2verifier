from verify import verifyMessage
from pcapParser import *
from fastecdsa import keys

from scapy.all import *
import binascii

pcapFileLocation = "/home/administrator/Desktop/out.pcap"

# load the public key - debugging
publicKey = keys.import_key("/home/administrator/v2v-capstone/keys/other_p256.pub")
print publicKey

print ""
# get the packets
packets = parsePcapFile(pcapFileLocation)

for packet in packets:
    
    payload = str(binascii.hexlify(packet[Raw].load))
    data = extractData(payload)
    print "unsecuredData:\t" + data[0]
    print "r-value:\t" + str(data[1])
    print "s-value:\t" + str(data[2])

    print verifyMessage(data[1],data[2],data[0],publicKey)
