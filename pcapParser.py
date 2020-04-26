from scapy.all import *
import binascii

#PCAP file location
pcapPath = "/home/administrator/Desktop/out.pcap"

def extractData(payload):
	
	# The first 8 bytes are WSMP N/T headers that do not change size
	ieee1609Dot2Data = payload[8:]

	# First item to extract is the payload in unsecured data field

	# Note that the numbers for positions are double the byte value
	# because this is a string of "hex numbers" so 1 byte = 2 chars

	unsecuredDataLength = int(ieee1609Dot2Data[12:14],16)*2
	unsecuredData = ieee1609Dot2Data[14:14+(unsecuredDataLength)]

	# Next extract the signature components r,s
	# total IEEE1609Dot2Data size is 93 bytes plus length of unsecured data
	totalSize = (93*2) + unsecuredDataLength

	# the ecdsaNistP256Signature structure is 66 bytes
	# r - 32 bytes
	# s - 32 bytes
	# field separators - 2 bytes

	signature = ieee1609Dot2Data[len(ieee1609Dot2Data)-(2*66):]

	# drop the two field identification bytes at the start of the block
	signature = signature[4:]

	# split into r and s

	r = signature[:64]
        s = signature[64:]

        # convert from string into ten-bit integer
	r = int(r,16)
	s = int(s,16)

	r = int(str(r))
	s = int(str(s))

	return (unsecuredData,r,s)


def parsePcapFile(pcapPath):
   	packets = rdpcap(pcapPath)

	return packets



