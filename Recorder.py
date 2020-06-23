from scapy.all import sniff
import binascii
import json
from fastecdsa import keys, curve
from Verifier import Verifier
from threading import Thread
from Receiver import Receiver
import os

class Recorder(Receiver):

    def __init__(self):
        self.createOutFile()
        self.verifier = Verifier()
        self.messageCounter = 1

    def createOutFile(self):
        self.outfile = open("results.csv","w")
        os.chmod("results.csv",0o777)
        self.outfile.write("X,Y,Dir,Speed,ValidSig,Time,Expired\n")
        self.outfile.close()

    def listenForWSMs(self):
        # print a console message to confirm the network connection is active
        print("Listening on localhost:4444 for WSMs")
        
        # listen on localhost:4444 which is the UDP sink from GNURadio in wifi_rx.py
        # received packets are passed to processPacket() for data extraction
        sniff(iface="lo", filter="dst port 4444", prn=lambda x: self.filterDuplicatePackets(str(binascii.hexlify(x.load))[130:]))
    
    def filterDuplicatePackets(self, payload):
        if self.messageCounter % 2 == 1:
            self.processPacket(payload)
        self.messageCounter += 1

    # uses returned tuple from parseWSM to verify message and send to GUI
    def processPacket(self, payload):
    	
        # extract the elements "(unsecuredData,r,s,time)" from the 1609.2 structure
        data = self.parseWSM(payload)
        
        #BSMData = data[0].decode('hex').replace("\n","").split(",")
        BSMData = bytes.fromhex(data[0]).decode('ascii').replace("\n","").split(",")

        # create a dictionary to pack and send
        decodedData = {}    
        
        decodedData['id'] = BSMData[0]
        decodedData['x'] = BSMData[1]
        decodedData['y'] = BSMData[2]
        decodedData['heading'] = BSMData[3]
        decodedData['speed'] = BSMData[4]

        publicKey = keys.import_key("keys/" + decodedData['id'] + "/p256.pub",curve=curve.P256, public=True)
        
        # verify the signature
        isValidSig = self.verifier.verifySignature(data[1],data[2],data[0],publicKey)
        
        elapsed, isRecent = self.verifier.verifyTime(data[3])
        
        decodedData['sig'] = isValidSig
        decodedData['elapsed'] = elapsed
        decodedData['recent'] = isRecent
        decodedData['receiver'] = False
    
        vehicleDataJSON = json.dumps(decodedData)

        print(vehicleDataJSON)
        self.outfile = open("results.csv","a")
        self.outfile.write(decodedData['x'] + "," + decodedData['y'] + "," + decodedData['heading'] + "," + decodedData['speed'] + "," + str(decodedData['sig']) + "," + str(decodedData['elapsed']) + "," + str(decodedData['recent']) + "\n")

        self.outfile.close()
	
