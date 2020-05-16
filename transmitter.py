import os
import csv
import time
import subprocess
from fastecdsa import keys, ecdsa
from fastecdsa.keys import import_key
from hashlib import sha256

"""
ADD NEW DESCRIPTION
"""
def loadTrace(pathToDataFile):
	
	trace = []
	
	with open(pathToDataFile) as infile:
		data = csv.reader(infile, delimiter=",")
		for item in data:
			print item

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
def generatePayloadBytes(vehicleDataString):
	
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
	payloadByteString += "0"
	vehicleData = str(hex(len(vehicleDataString)).split("x")[1])
	payloadByteString += vehicleData

	# unsecuredData
	payloadByteString += vehicleDataString.encode('hex')
	
	# headerInfo
	payloadByteString += "4001"

	# PSID (BSM = 20)
	payloadByteString += "20"

	# generationTime (8 bytes) - this is a dummy value
	payloadByteString += "1112131415161718"

	# signer
	payloadByteString += "80"

	# Digest (8 bytes) - this is also a dummy value
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

	private, public = import_key("/home/administrator/v2v-capstone/keys/p256.key")

	r, s = ecdsa.sign(vehicleDataString.encode('hex'), private, hashfunc=sha256)

	r = hex(r)
	s = hex(s)
	
	r = r.split("x")[1][:len(r)-3]
	s = s.split("x")[1][:len(s)-3]

	# r (32 bytes)
	payloadByteString += str(r)

	# s (32 bytes)
	payloadByteString += str(s)

	payloadByteString = "\\x".join(payloadByteString[i:i+2] for i in range(0, len(payloadByteString), 2))
	payloadByteString = "\\x" + payloadByteString

	pduPayload = headerByteString + payloadByteString

	return pduPayload

"""
Function to write vehicle traces loaded from a master CSV file to individual 
files for each vehicle. This is more efficient at run time as only the files 
for the specific vehicles appearing in the simulation need to be loaded.

Inputs:

traces -	a list containing sequential coordinate pairs. Intended to be the output
			from loadTracesFromFile()
"""
def writeVehicleTraceFiles(traces):
	
	outfiles = [
	os.getcwd() + "/v0path",
	os.getcwd() + "/v1path",
	os.getcwd() + "/v2path",
	os.getcwd() + "/v3path",
	os.getcwd() + "/v4path",
	os.getcwd() + "/v5path"
	]

	# We support up to six vehicles, but more can be added by changing the 
	# loop maximum to a higher integer.
	for vehicle in range (0,6):
		with open(outfiles[vehicle], 'w') as outfile:
			for trace in traces:
				for position in trace:
					# position[0] is the vehicleID
					if position[0] == str(vehicle):
						# only one vehicle in the output file, so only write the coords
						outfile.write(str(position[1]) + "," + str(position[2]) + "\n")
			outfile.close()

"""
Function to transmit the crafted WSMP messages to the GNURadio listner on port 444
that will encapsulate the WSMP message in an 802.11p frame and send it over the USRP.

Inputs:

vehicleNo - the ID number of the vehicle whose trace will be used
"""
def sendPacketStream(vehicleNo):
	if vehicleNo < 0 or vehicleNo > 5:
		print "Error - invalid vehicle number. Must be between 0 and 5. Exiting"
		exit()
	trace = open("v"+str(vehicleNo)+"path")
	for i in range(0,400):
		vehicleData = str(vehicleNo) + "," + trace.readline()
		
		# Use the native echo utility to send the crafted message payload into a pipe 
		loader = subprocess.Popen(("echo","-n","-e",generatePayloadBytes(vehicleData)), stdout=subprocess.PIPE)
		# Send the contents of the pipe to GNURadio using the native Netcat (nc) utility
		sender = subprocess.check_output(("nc","-w1","-u","localhost","52001"),stdin=loader.stdout)
		# Pause 100ms to emulate the pulse rate of real BSMs
		time.sleep(0.1)


# Execution hook
if __name__ == "__main__":
	traces = loadTraces()
	writeVehicleTraces(traces)
	sendPacketStream(0)
