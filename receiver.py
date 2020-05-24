from verify import verifySignature
from pcapParser import *
from fastecdsa import keys, curve
from transmitter import calculateHeading

from scapy.all import *
import binascii

from time import sleep

from socket import AF_INET, SOCK_STREAM
import math
import random
from datetime import datetime

import json

# load the public key of the other "vehicle" (the host connected to the other USRP)
publicKey = keys.import_key("/home/administrator/v2v-capstone/keys/other_p256.pub",curve=curve.P256, public=True)

def calculateElapsedTime(timeInMicroSeconds):
	unpaddedTimeInMicroseconds = ""
	for i in range(0,len(timeInMicroSeconds)):
		if timeInMicroSeconds[i] != "0":
			unpaddedTimeInMicroseconds = timeInMicroSeconds[i:]
			break
	unpaddedTimeInMicroseconds = int(unpaddedTimeInMicroseconds, 16)

	origin = datetime(2004, 1, 1, 0, 0, 0, 0)
	now = (datetime.now() - origin).total_seconds() * 1000

	return now - unpaddedTimeInMicroseconds

def verifyTime(elapsedMicroseconds):
	return elapsedMicroseconds < 100

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
	
	# create a dictionary to pack and send
	decodedData = {}	
	
	# extract the elements "r,s,vehicleData,timestamp" from the 1609.2 structure
	data = extractData(payload)

	elapsedMicroseconds = calculateElapsedTime(data[3])
	isRecent = verifyTime(elapsedMicroseconds)
	
	# verify the signature
	print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
	print [data[0]]
	print [data[3]]
	print [data[0] + data[3].encode('hex')]
	print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
	isValidSig = verifySignature(data[1],data[2],(data[0] + data[3]),publicKey)

	# decode and break up the BSM data string "x,y"
	BSMData = data[0].decode('hex').replace("\n","").split(",")
	
	decodedData['x'] = BSMData[0]
	decodedData['y'] = BSMData[1]
	decodedData['heading'] = BSMData[2]
	decodedData['sig'] = isValidSig
	decodedData['elapsed'] = elapsedMicroseconds
	decodedData['recent'] = isRecent
	decodedData['receiver'] = False

	vehicleDataJSON = json.dumps(decodedData)

	print "vehicleDataJSON: " + vehicleDataJSON

	with lock:
		s.send(vehicleDataJSON.encode())
	
	

"""
Function to send data about the receiver's "vehicle" to the GUI application

Inputs:

vehicleNo   - the id number, used to open the correct trace file
socket	  - the TCP socket connected to the GUI application
lock		- a thread lock passed from rxMain.py
"""
def runSelf(socket, lock):

	trace = None
	with open("receiver_path") as traceFile:
		trace = traceFile.read().splitlines()
		for i in range(0,len(trace)-2):

			vehicleData = {}

			vehicleData['x'], vehicleData['y'] = trace[i].split(",")
			vehicleData['heading'] = calculateHeading(trace[i],trace[i+1])
			vehicleData['sig'] = True
			vehicleData['recent'] = True
			vehicleData['receiver'] = True
			vehicleData['elapsed'] = 0

			vehicleDataJSON = json.dumps(vehicleData)
			
			print "vehicleDataJSON: " + vehicleDataJSON

			sleep(0.1)

			with lock:
				socket.send(vehicleDataJSON.encode())

def listen(s,lock):

	# print a console message to confirm the network connection is active
	print "Listening"

	# listen on localhost:4444 which is the UDP sink from GNURadio in wifi_rx.py
	# received packets are passed to processPacket() for data extraction
	sniff(iface="lo", filter="udp and dst port 4444", prn=lambda x: processPacket(str(binascii.hexlify(x.load))[130:],s,lock))

if __name__ == "__main__":
	print "You executed the wrong file. Please run rxMain.py"
	exit(0)
