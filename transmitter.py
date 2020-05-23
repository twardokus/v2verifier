import os
import csv
import time
import subprocess
from fastecdsa import keys, ecdsa
from fastecdsa.keys import import_key
from hashlib import sha256
from datetime import datetime
import math


"""
Function to generate a hexidecimal string representation of the bytes composing 
everything above layer 2. 

Details: The wifi_tx.py file, as modified by us and included
in this repo, directly encapsulates the bytes received on a UDP listener within
a standard 802.11p frame. This function generates the bytes that compose a simple
WSMP message and an IEEE1609Dot2Data cryptographic structure embedded in the WSMP
message. The format of the WSMP message is compliant with the IEEE 1609.3 standard,
and the IEEE 1609.2 structure is compliant with the IEEE 1609.2b (2019) standard 
with the exception that certificates and PKI are not implemented here.

Inputs:

vehicleDataString - a string containing simple CSV data like
					"vehicleIDNumber,x-coord,y-coord" for use with the GUI application.

"""
def generatePayloadBytes(vehicleDataString,option):
	
	# Header fields individually set for easy configuration changes
	headerByteString = ""

	# Logical Link Control fields
	#llc_dsap = "aa" to indicate SNAP extension in use (for protocol identification)
	headerByteString += "aa"
	#llc_ssap = "aa" to indicate SNAP extension in use  (for protocol identification)
	headerByteString += "aa"
	#llc_control = "03" for unacknowledged, connectionless mode
	headerByteString += "03"
	#llc_org_code = "000000" as we have no assigned OUI
	headerByteString += "000000"
	#llc_type = "88dc" to indicate WAVE Simple Message Protocol
	headerByteString += "88dc"
	
	# WSMP N-Header and T-Header fields
	#wsmp_n_subtype_opt_version = "03"
	headerByteString += "03"
	#wsmp_n_tpid = "00"
	headerByteString += "00"
	#wsmp_t_headerLengthAndPSID = "20"
	headerByteString += "20"
	#wsmp_t_length = "00"
	headerByteString += "00"	

	
	headerByteString = "\\x".join(headerByteString[i:i+2] for i in range(0, len(headerByteString), 2))
	
	#headerByteString = "".join(headerByteString[i:i+2] for i in range(0, len(headerByteString), 2))
	headerByteString = "\\x" + headerByteString
	
	####################################################
	# IEEE1609Dot2Data Structure

	### Calculate timestamp first so that hash of timestamp can be used in message
	### to include the timestamp in the signature verification
	# IEEE 1609.2 defines timestamps as an estimate of the microseconds elapsed since
	# 12:00 AM on January 1, 2004
	origin = datetime(2004, 1, 1, 0, 0, 0, 0)
	
	# get the offset since the origin time in microseconds
	offset = (datetime.now() - origin).total_seconds() * 1000
	timestr = hex(int(math.floor(offset)))
        timestr  = timestr[2:]
	if len(timestr) < 16:
		for i in range(0, 16 - len(timestr)):
			timestr = "0" + timestr
	
	# begin assembling structure
	payloadByteString = ""
		
	# Protocol Version
	payloadByteString += "03"

	# ContentType ( signed data = 81)
	payloadByteString += "81"

	# HashID (SHA256 = 00)
	payloadByteString += "00"
	
	# Data
	payloadByteString += "40"

	# Protocol Version
	payloadByteString += "03"

	# Content - Unsecured Data
	payloadByteString += "80"

	# Length of Unsecured Data
	"""
	payloadByteString += "0"
	print vehicleDataString
	print str(hex(len(vehicleDataString)))
	"""	
	vehicleData = str(hex(len(vehicleDataString)).split("x")[1])
	if len(vehicleData) == 1:
		payloadByteString += "0"
	payloadByteString += vehicleData

	# unsecuredData
	payloadByteString += (vehicleDataString + ",").encode('hex') + timestr[:8]
	
	"""
	# extDataHash
	payloadByteString += "8020"
	payloadByteString += "FF"*32
	"""

	# headerInfo
	payloadByteString += "4001"

	# PSID (BSM = 20)
	payloadByteString += "20"

	# generationTime (8 bytes)
	payloadByteString += timestr

	# signer
	payloadByteString += "80"

	# Digest (8 bytes) - this is a dummy value as we have not used certificates, which would be involved here
	payloadByteString += "2122232425262728"

	# signature (ecdsaNistP256Signature = 80)
	payloadByteString += "80"

	# ecdsaNistP256Signature (r: compressed-y-0 = 82)
	# 80 -> x-only
	# 81 -> fill (NULL)
	# 82 -> compressed-y-0
	# 83 -> compressed-y-1
	# 84 -> uncompressed
	payloadByteString += "80"
        
        r = None
        s = None
        private = None
        public = None
        if option == "normal":
        	private, public = import_key("/home/administrator/v2v-capstone/keys/p256.key")
	        r, s = ecdsa.sign(vehicleDataString.encode('hex'), private, hashfunc=sha256)
                r = hex(r)
	        s = hex(s)
	
	        r = r.split("x")[1][:len(r)-3]
	        s = s.split("x")[1][:len(s)-3]
                #print "Valid r:\t" + str(r)
                #print "Valid s:\t" + str(s)
        else:
                r = "00"*32
                s = "00"*32
                #print "Attack r:\t" + str(r)
                #print "Attack s:\t" + str(s)
	
        # r (32 bytes)
	payloadByteString += str(r)

	# s (32 bytes)
	payloadByteString += str(s)

	payloadByteString = "\\x".join(payloadByteString[i:i+2] for i in range(0, len(payloadByteString), 2))
	payloadByteString = "\\x" + payloadByteString

	pduPayload = headerByteString + payloadByteString

	return pduPayload

def loadTrace(option):
        trace = []
	with open("path" if option == "normal" else "attacker_path") as traceFile:	
		trace = traceFile.read().splitlines()
	return trace

"""
Function to transmit the crafted WSMP messages to the GNURadio listner on port 4444
that will encapsulate the WSMP message in an 802.11p frame and send it over the USRP.

Inputs:

vehicleNo - the ID number of the vehicle whose trace will be used
"""
def calculateHeading(now, next):
	xNow, yNow = now.split(",")
	xNow = int(xNow)
	yNow = int(yNow)

	xNext, yNext = next.split(",")
	xNext = int(xNext)
	yNext = int(yNext)

	if xNext == xNow and yNext == yNow:
		return "none"
	else:
		if xNext > xNow:
			if yNext > yNow:
				return "southeast"
			elif yNext == yNow:
				return "east"
			else:
				return "northeast"
		elif xNext == xNow:
			return "south" if yNext > yNow else "north"
		elif xNext < xNow:
			if yNext > yNow:
				return "southwest"
			elif yNext == yNow:
				return "west"
			else:
				return "northwest"

#option should either be "attacker" or "normal"
def sendPacketStream(option):
	trace = loadTrace(option)
	for i in range(0,len(trace)-2):

		heading = calculateHeading(trace[i],trace[i+1])		

		vehicleData = trace[i] + "," + heading
		
		dataToSend = generatePayloadBytes(vehicleData,option)

		# Use the native echo utility to send the crafted message payload into a pipe 
		loader = subprocess.Popen(("echo","-n","-e",dataToSend), stdout=subprocess.PIPE)
		# Send the contents of the pipe to GNURadio using the native Netcat (nc) utility
		sender = subprocess.check_output(("nc","-w1","-u","localhost","52001"),stdin=loader.stdout)
		# Pause 100ms to emulate the pulse rate of real BSMs
		time.sleep(0.1)


# Execution hook
if __name__ == "__main__":
	print "You executed the wrong file. Please run txMain.py instead."
	exit(0)
