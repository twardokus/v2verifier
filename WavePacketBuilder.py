from fastecdsa import ecdsa, keys, curve
from hashlib import sha256
from X1609 import X1609


class WAVEPacketBuilder:

    def __init__(self):
        private, public = keys.import_key("keys/0/p256.key")
        self.cert = X1609("CSEC490", private).toString()

    def get_wsm_payload(self, bsm_string, key):
        payload = self.get_llc_bytestring() + self.get_wsm_headers() + self.getIeee1609Dot2Data(bsm_string, key)

        return "\\x" + "\\x".join(payload[i:i + 2] for i in range(0, len(payload), 2))

    def get_llc_bytestring(self):
        bytestring = ""

        # Logical Link Control fields

        # llc_dsap = "aa" to indicate SNAP extension in use (for protocol identification)
        bytestring += "aa"

        # llc_ssap = "aa" to indicate SNAP extension in use  (for protocol identification)
        bytestring += "aa"

        # llc_control = "03" for unacknowledged, connectionless mode
        bytestring += "03"

        # llc_org_code = "000000" as we have no assigned OUI
        bytestring += "000000"

        # llc_type = "88dc" to indicate WAVE Short Message Protocol
        bytestring += "88dc"

        return bytestring

    def get_wsm_headers(self):
        bytestring = ""

        # WSM N-Header and T-Header fields

        # wsmp_n_subtype_opt_version = "03"
        bytestring += "03"
        # wsmp_n_tpid = "00"
        bytestring += "00"
        # wsmp_t_headerLengthAndPSID = "20"
        bytestring += "20"
        # wsmp_t_length = "00"
        bytestring += "00"

        return bytestring

    def getIeee1609Dot2Data(self, message, key):
        message = message.encode("utf-8").hex()

        # IEEE1609Dot2Data Structure
        bytestring = ""
        # Protocol Version
        bytestring += "03"
        # ContentType (signed data = 81)
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
        length = hex(int(len(str(message)) / 2)).split("x")[1]
        if len(length) == 1:
            bytestring += "0"
        bytestring += length

        # unsecuredData
        bytestring += message

        # headerInfo
        bytestring += "4001"

        # PSID (Blind Spot Monitoring = 20)
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
        # Assuming digest is 80, set to 81
        bytestring += "81"
        bytestring += self.cert

        # signature (ecdsaNistP256Signature = 80)
        bytestring += "80"

        # ecdsaNistP256Signature
        # 80 -> x-only
        # 81 -> fill (NULL)
        # 82 -> compressed-y-0
        # 83 -> compressed-y-1
        # 84 -> uncompressed
        bytestring += "80"

        private, public = keys.import_key(key)
        r, s = ecdsa.sign(message, private, hashfunc=sha256)
        r = hex(r)
        s = hex(s)

        r = r.split("x")[1][:len(r) - 2]
        s = s.split("x")[1][:len(s) - 2]

        # r (32 bytes)
        bytestring += str(r)

        # s (32 bytes)
        bytestring += str(s)

        return bytestring
