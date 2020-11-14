from WavePacketBuilder import WAVEPacketBuilder
import random


class AttackerWave(WAVEPacketBuilder):
    
    def get_wsm_payload(self, bsm_string):
        
        payload = super().get_llc_bytestring() + super().get_wsm_headers() + self.getIeee1609Dot2Data(bsm_string)
       
        return "\\x" + "\\x".join(payload[i:i+2] for i in range(0, len(payload), 2))

    def getIeee1609Dot2Data(self, message):
        
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
        
        # this is a placeholder byte pattern that is unlikely to occur in practice, used to inject actual time
        # when packet is transmitted
        bytestring += "F0E0F0E0F0E0F0E0"
        
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
        
        # since an attacker will not have a legitimate key, generate a random 32-byte (64-character)
        # hex string for r and s
        r = "".join(random.choice("0123456789ABCDEF") for i in range(0,64))
        s = "".join(random.choice("0123456789ABCDEF") for i in range(0,64))
        
        bytestring += r
        
        bytestring += s
        
        return bytestring
