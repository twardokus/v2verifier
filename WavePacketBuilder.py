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
        
        # this is a placeholder byte pattern that is unlikely to occur in practice, used to inject actual time
        # when packet is transmitted
        bytestring += "F0E0F0E0F0E0F0E0"

        # Digest (8 bytes) - this is a dummy value as we have not used certificates, which would be involved here
        # NOT NEEDED, for if signerIdentifier = "digest"
        # bytestring += "80"
        # bytestring += "2122232425262728"

        # signerIdentifier = "certificate"
        #Assuming digest is 80, set to 81
        bytestring += "81"
    
        #START CERTIFICATE BASE

        #version = 3
        bytestring += "03"

        # Number of items
        bytestring += "000001"

        #CertificateType = "explicit"
        #@TODO implement ExplicitCertificate structure here

        # Filler?
        bytestring += "00"

        # version
        bytestring += "03"

        # type
        bytestring += "00"

        #Issuer = "sha256AndDigest"
        #dummy value here for issuerID
        bytestring += "002122232425262728"

        #toBeSigned
        # - START ToBeSignedCertificate HERE -

        #id = linkageData
        #this data is used to compare/add certificates to a CRL
        #START linkageData HERE


        #buffer
        bytestring += "0000"
        
        # certificateID choice
        bytestring += "00"
        

        #iCert DUMMY VALUE
        bytestring += "0100"

        #linkage-value(size = 9) DUMMY VALUE
        bytestring += "0fa12245f4c3c1cd54"
        #END linkageData HERE

        #cracaID(size = 3) DUMMY VALUE
        bytestring += "52641c"

        #crlSeries DUMMY VALUE
        bytestring += "2000"

        #START validityPeriod HERE
        #start(time32)
        bytestring += "24c34587"

        #duration
        bytestring += "030005"
        
        # VerificationKeyIndicator
        bytestring += "01"
        
        # EccP256CurvePoint
        bytestring += "00"
        bytestring += "00"*32

        #END validityPeriod HERE

        # - OPTIONAL FIELDS CAN GO HERE -
        # IN ORDER:
        # region, assuranceLevel, appPermissions, certIssuePermissions, certRequestPermissions,
        # canRequestRollover, encryptionKey

        #verifyKeyIndicator
        #@TODO get more information on KeyIndicator

        # - END ToBeSignedCertificate HERE -
    
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
        
        r = r.split("x")[1][:len(r)-2]
        s = s.split("x")[1][:len(s)-2]
        
        # r (32 bytes)
        bytestring += str(r)
    
        # s (32 bytes)
        bytestring += str(s)
        
        return bytestring
