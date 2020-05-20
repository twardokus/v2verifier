from verify import verifySignature
from pcapParser import *
from fastecdsa import keys, curve

from scapy.all import *
import binascii

from time import sleep

from socket import AF_INET, SOCK_STREAM
import math
import random
from datetime import datetime

# load the public key of the other "vehicle" (the host connected to the other USRP)
publicKey = keys.import_key("/home/administrator/v2v-capstone/keys/other_p256.pub",curve=curve.P256, public=True)

def verifyTime(timeInMicroSeconds):
	unpaddedTimeInMicroseconds = ""
	for i in range(0,len(timeInMicroSeconds)):
		if timeInMicroSeconds[i] != "0":
			unpaddedTimeInMicroseconds = timeInMicroSeconds[i:]
			break
	unpaddedTimeInMicroseconds = int(unpaddedTimeInMicroseconds, 16)

	origin = datetime(2004, 1, 1, 0, 0, 0, 0)
	now = (datetime.now() - origin).total_seconds() * 1000

	#print "Microseconds from packet: " + str(unpaddedTimeInMicroseconds)
	#print "Now, in microseconds: " + str(now)
	#print "Microseconds since transmission: " + str(now - unpaddedTimeInMicroseconds)

	return now - unpaddedTimeInMicroseconds

"""
Function to extract the data string (format id,x-coord,y-coord) from the 
payload of the received DSRC message

Inputs:

payload -   the hexadecimal string representing everything above Layer 2,
	i.e. the WSMP message and embedded ieee1609Dot2Data structure
s -a TCP socket connected to the GUI application
lock	-   a thread lock passed from rxMain.py
"""

def processPacket(payload,s,lock):
	
	data = extractData(payload)

	time = verifyTime(data[3])
	
	status = verifySignature(data[1],data[2],data[0],publicKey)

	vehicleData = data[0].decode('hex').replace("\n","")
	vehicleData += ",True" if int(status) else ",False"
	vehicleData += "," + str(time)

	with lock:
		s.send(vehicleData.encode())

"""
Function to send data about the receiver's "vehicle" to the GUI application

Inputs:

vehicleNo   - the id number, used to open the correct trace file
socket	  - the TCP socket connected to the GUI application
lock		- a thread lock passed from rxMain.py
"""
def runSelf(socket, lock):

	trace = open("v" + str(vehicleNo) + "path")

	for i in range(0,400):
		vehicleData = str(vehicleNo) + "," + trace.readline()
		vehicleData += ",True"

		# sleeping for 0.5 seconds keeps the display update rate reasonable
		sleep(0.5)

		with lock:
			socket.send(vehicleData.replace("\n","").encode())


def listen(s,lock):

	# print a console message to confirm the network connection is active
	print "Listening"

	# listen on localhost:4444 which is the UDP sink from GNURadio in wifi_rx.py
	# received packets are passed to processPacket() for data extraction
	sniff(iface="lo", filter="udp and port 4444", prn=lambda x: processPacket(str(binascii.hexlify(x.load))[130:],s,lock))

if __name__ == "__main__":
	runSelf(None, None)
