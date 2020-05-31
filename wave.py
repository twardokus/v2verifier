from fastecdsa import ecdsa
from fastecdsa.keys import import_key
from hashlib import sha256
from datetime import datetime
import math

class WAVEPacketBuilder():
    
    def getWSMPayload(self, bsmString, key):
        
        payload = self.getLLCBytestring() + self.getWSMHeaders() + self.getIeee1609Dot2Data(bsmString,key)
       
        return "\\x" + "\\x".join(payload[i:i+2] for i in range(0, len(payload), 2))
    
    def getLLCBytestring(self):
        
        bytestring = ""
        
        # Logical Link Control fields
        
        #llc_dsap = "aa" to indicate SNAP extension in use (for protocol identification)
        bytestring += "aa"
        #llc_ssap = "aa" to indicate SNAP extension in use  (for protocol identification)
        bytestring += "aa"
        #llc_control = "03" for unacknowledged, connectionless mode
        bytestring += "03"
        #llc_org_code = "000000" as we have no assigned OUI
        bytestring += "000000"
        #llc_type = "88dc" to indicate WAVE Short Message Protocol
        bytestring += "88dc"
        
        return bytestring
    
    def getWSMHeaders(self):
        
        bytestring = ""
        
        # WSM N-Header and T-Header fields
        
        #wsmp_n_subtype_opt_version = "03"
        bytestring += "03"
        #wsmp_n_tpid = "00"
        bytestring += "00"
        #wsmp_t_headerLengthAndPSID = "20"
        bytestring += "20"
        #wsmp_t_length = "00"
        bytestring += "00"
        
        return bytestring
    
    def getIeee1609Dot2Data(self, message, key):
        
        message = message.encode("utf-8").hex()
    
        # IEEE1609Dot2Data Structure
        
        # begin assembling structure
        bytestring = ""
            
        # Protocol Version
        bytestring += "03"
    
        # ContentType ( signed data = 81)
        bytestring += "81"
    
        # HashID (SHA256 = 00)
        bytestring += "00"
        
        # Data
        bytestring += "40"
    
        # Protocol Version
        bytestring += "03"
    
        # Content - Unsecured Data
        bytestring += "80"
    
        # Length of Unsecured Data
        length = hex(int(len(str(message))/2)).split("x")[1]
        if len(length) == 1:
            bytestring += "0"
        bytestring += length
    
        # unsecuredData
        bytestring += message
        
        # headerInfo
        bytestring += "4001"
    
        # PSID (BSM = 20)
        bytestring += "20"
    
        # generationTime (8 bytes)
        
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
    
        bytestring += timestr
    
        # signer
        bytestring += "80"
    
        # Digest (8 bytes) - this is a dummy value as we have not used certificates, which would be involved here
        bytestring += "2122232425262728"
    
        # signature (ecdsaNistP256Signature = 80)
        bytestring += "80"
    
        # ecdsaNistP256Signature (r: compressed-y-0 = 82)
        # 80 -> x-only
        # 81 -> fill (NULL)
        # 82 -> compressed-y-0
        # 83 -> compressed-y-1
        # 84 -> uncompressed
        bytestring += "80"
        
        private, public = import_key(key)        
        r, s = ecdsa.sign(message, private, hashfunc=sha256)
        r = hex(r)
        s = hex(s)
    
        r = r.split("x")[1][:len(r)-3]
        s = s.split("x")[1][:len(s)-3]
        
        # r (32 bytes)
        bytestring += str(r)
    
        # s (32 bytes)
        bytestring += str(s)
    
        return bytestring
