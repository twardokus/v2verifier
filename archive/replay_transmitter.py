import os
import csv
import time
import subprocess
import math
import transmitter

from fastecdsa import keys, ecdsa
from fastecdsa.keys import import_key
from hashlib import sha256
from datetime import datetime


#option should either be "attacker" or "normal"
def sendPacketStream(option):
	
	if option == "normal":
		
		trace = transmitter.loadTrace(option)
		for i in range(0,len(trace)-2):

			heading = transmitter.calculateHeading(trace[i],trace[i+1])		

			vehicleData = trace[i] + "," + heading
			
			dataToSend = transmitter.generatePayloadBytes(vehicleData,option)

			# Use the native echo utility to send the crafted message payload into a pipe 
			loader = subprocess.Popen(("echo","-n","-e",dataToSend), stdout=subprocess.PIPE)
			# Send the contents of the pipe to GNURadio using the native Netcat (nc) utility
			sender = subprocess.check_output(("nc","-w1","-u","localhost","52001"),stdin=loader.stdout)
			# Pause 100ms to emulate the pulse rate of real BSMs
			time.sleep(0.1)
	else:
		trace = ["100,100","105,105"]

		heading = transmitter.calculateHeading(trace[0],trace[1])		

		vehicleData = trace[0] + "," + heading
		
		dataToSend = transmitter.generatePayloadBytes(vehicleData,option)

		for i in range(0,100):
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
