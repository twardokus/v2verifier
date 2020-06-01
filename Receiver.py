from scapy.all import sniff
import binascii
import json
from fastecdsa import keys, curve
from Verifier import Verifier
from threading import Thread

class Receiver:
    
    def __init__(self):
        self.verifier = Verifier()
        
    def runReceiver(self, socketToGUI, guiLock):
        listener = Thread(target=self.listenForWSMs(socketToGUI, guiLock))
        listener.start()
        
    def listenForWSMs(self, s, lock):
        # print a console message to confirm the network connection is active
        print("Listening on localhost:4444 for WSMs")
    
        # listen on localhost:4444 which is the UDP sink from GNURadio in wifi_rx.py
        # received packets are passed to processPacket() for data extraction
        sniff(iface="lo", filter="dst port 4444", prn=lambda x: self.processPacket(str(binascii.hexlify(x.load))[130:],s,lock))
    
    # uses returned tuple from parseWSM to verify message and send to GUI
    def processPacket(self, payload, s, lock):
    
        # extract the elements "(unsecuredData,r,s,time)" from the 1609.2 structure
        data = self.parseWSM(payload)
        
        elapsed, isRecent = self.verifier.verifyTime(data[3])
        
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
        
        decodedData['sig'] = isValidSig
        decodedData['elapsed'] = elapsed
        decodedData['recent'] = isRecent
        decodedData['receiver'] = False
    
        vehicleDataJSON = json.dumps(decodedData)
    
        with lock:
            s.send(vehicleDataJSON.encode())
  
    # takes the hex payload from an 802.11p frame as an argument, returns tuple of extracted bytestrings
    def parseWSM(self, WSM):
            
        # The first 8 bytes are WSMP N/T headers that do not change in size and can be discarded
        ieee1609Dot2Data = WSM[8:]

        # First item to extract is the payload in unsecured data field
    
        # Note that the numbers for positions are double the byte value
        # because this is a string of "hex numbers" so 1 byte = 2 chars
    
        unsecuredDataLength = int(ieee1609Dot2Data[14:16],16)*2
        unsecuredData = ieee1609Dot2Data[16:16+(unsecuredDataLength)]
        timePostition = 16 + unsecuredDataLength + 6
        time = ieee1609Dot2Data[timePostition:timePostition+16]
    
        # the ecdsaNistP256Signature structure is 66 bytes
        # r - 32 bytes
        # s - 32 bytes
        # field separators - 2 bytes
        signature = ieee1609Dot2Data[len(ieee1609Dot2Data)-(2*66)-1:]
    
        # drop the two field identification bytes at the start of the block
        signature = signature[4:]
        
        # split into r and s
    
        r = signature[:64]
        s = signature[64:128]
    
        # convert from string into ten-bit integer
        r = int(r,16)
        s = int(s,16)
    
        r = int(str(r))
        s = int(str(s))
    
        return (unsecuredData,r,s,time)
