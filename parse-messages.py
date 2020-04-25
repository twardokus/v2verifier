from scapy.all import *
import binascii

#PCAP file location
pcapPath = "/home/administrator/Desktop/out.pcap"

packets = rdpcap(pcapPath)

for packet in packets:
    # the payload is everything encapsulated inside LLC
    payload = str(binascii.hexlify(packet[Raw].load))
    
    # The first 8 bytes are WSMP N/T headers that do not change size
    ieee1609Dot2Data = payload[8:]
    
    # First item to extract is the payload in unsecured data field

    # Note that the numbers for positions are double the byte value
    # because this is a string of "hex numbers" so 1 byte = 2 chars

    unsecuredDataLength = int(ieee1609Dot2Data[12:14],16)

    unsecuredData = ieee1609Dot2Data[14:14+(unsecuredDataLength*2)]
    
