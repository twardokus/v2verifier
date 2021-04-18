from fastecdsa import keys, curve, ecdsa
from hashlib import sha256

class X1609:
    
    def __init__(self, hostname, private_key):
        # version (uint8)
        # default = 3
        self.version = "03"

        # type
        # 80 -> explicit
        # 81 -> implicit
        self.type = "80"

        # issuer
        # 80 -> (self) sha256
        self.issuer = "80"

        # to be signed certificate
        self.toBeSigned = ToBeSignedCertificate(hostname).toString()

        # signature
        # 80 -> ecdsaNistP256Signature
        #
        # ecdsaNistP256Signature
        # 80 -> x-only (octet string size(32))
        # 81 -> fill (null)
        # 82 -> compressed-y-0 (octet string size(32))
        # 83 -> compressed-y-1 (octet string size(32))
        # 84 -> uncompressed (octet string size(64))
        self.signature = "80"
        self.ecdsa_nist_p256 = "80"

        r, s = ecdsa.sign(self.toBeSigned.encode("utf-8").hex(), private_key, hashfunc=sha256)
        
        r = hex(r)
        s = hex(s)
        
        r = r.split("x")[1][:len(r) - 2]
        s = s.split("x")[1][:len(s) - 2]
        
        self.r = str(r)
        self.s = str(s)

    def toString(self):
        bytestring = self.version
        bytestring += self.type
        bytestring += self.issuer
        bytestring += self.toBeSigned
        bytestring += self.signature
        bytestring += self.ecdsa_nist_p256
        bytestring += self.r
        bytestring += self.s

        return bytestring

class ToBeSignedCertificate():

    def __init__(self, hostname):
        # cert id
        # 80 -> linkage data
        # 81 -> hostname
        # 82 -> binary id
        # 83 -> null
        self.id = "81"
        if len(hostname) % 2 == 0:
            self.hostname = hostname
        else:
            self.hostname = "0" + hostname

        # craca id (octet string size(3))
        self.craca_id = "000000"

        # crl series (uint16)
        self.crl_series = "0000"

        # validity period
        # 80 -> microseconds
        # 81 -> milliseconds
        # 82 -> seconds
        # 83 -> minutes
        # 84 -> hours
        # 85 -> sixty hours
        # 86 -> years
        #
        # start (uint32)
        # duration (uint16)
        self.validity_period = "86"
        self.start = "00000000"
        self.duration = "0001"

        # region type (optional)
        # 80 -> circular
        # 81 -> rectangular
        # 82 -> polygonal
        # 83 -> indentified
        #
        # identified region type
        # 80 -> country only
        # 81 -> country and regions
        # 82 -> country and subregions
        #
        # country (uint16)
        # 348 -> USA
        #
        # regions (uint8)
        # 24 -> NY
        #
        # subregions (uint16)
        # 8CD7 -> Monroe County
        self.region_type = "83"
        self.identified_region_type = "82"
        self.country = "0348"
        self.region = "24"
        self.subregion = "8CD7"

        # assurance level (octet string size(1)) (optional)
        # bit number        7   6   5   4   3   2   1   0
        # interpretation    A   A   A   R   R   R   C   C
        #
        # A -> assurance level
        # R -> reserved bit
        # C -> confidence
        self.assurance_level = "E3"

        # app permissions
        # psid (int)
        # 32 -> vehicle to vehicle saftey and awareness
        #
        # ssp opaque (octect string) (optional)
        self.psid = "32"
        self.ssp_opaque = ""

        # cert issue permissions
        # issue subject permissions
        # psid -> explicit
        # null -> all
        #
        # issue min chain depth (default = 1)
        # issue chain depth range (default = 0)
        #
        # issue end entity type (bit string size(8))
        # 0 -> app
        # 1 -> enroll
        self.issue_subject_permission = ""
        self.issue_min_chain_depth = "01"
        self.issue_chain_depth_range = "00"
        self.issue_end_entity_type = "00000000"

        # cert request permissions
        # request subject permissions
        # psid -> explicit
        # null -> all
        #
        # request min chain depth (default = 1)
        # request chain depth range (default = 0)
        #
        # request end entity type (bit string size(8))
        # 0 -> app
        # 1 -> enroll
        self.request_subject_permission = ""
        self.request_min_chain_depth = "01"
        self.request_chain_depth_range = "00"
        self.request_end_entity_type = "00000000"

        # can request rollover (optional)
        # 0 = false
        # 1 = true
        self.can_request_rollover = "00"

        # public encryption key (optional)
        # supported symmetric algorithm
        # 80 -> aes128Ccm
        #
        # encyrption
        # 80 -> ecies nist p256
        # 81 -> ecies brainpool p256r1
        #
        # ecc p256 curve point
        # 80 -> x-only (octet string size(32))
        # 81 -> fill (null)
        # 82 -> compressed-y-0 (octet string size(32))
        # 83 -> compressed-y-1 (octet string size(32))
        # 84 -> uncompressed (octet string size(64))
        self.supported_symm_alg = "80"
        self.public_encryption = "81"
        self.public_curve_point = "80"
        self.public_curve_data = "00" * 32

        # verification key indicator
        # encyrption
        # 80 -> ecies nist p256
        # 81 -> ecies brainpool p256r1
        #
        # ecc p256 curve point
        # 80 -> x-only (octet string size(32))
        # 81 -> fill (null)
        # 82 -> compressed-y-0 (octet string size(32))
        # 83 -> compressed-y-1 (octet string size(32))
        # 84 -> uncompressed (octet string size(64))
        self.verification_encyrption = "81"
        self.verification_curve_point = "80"
        self.verification_curve_data = "00" * 32

    def toString(self):
        bytestring = self.id
        bytestring += self.hostname
        bytestring += self.craca_id
        bytestring += self.crl_series
        bytestring += self.validity_period
        bytestring += self.start
        bytestring += self.duration
        bytestring += self.region_type
        bytestring += self.identified_region_type
        bytestring += self.country
        bytestring += self.region
        bytestring += self.subregion
        bytestring += self.assurance_level
        bytestring += self.psid
        bytestring += self.ssp_opaque
        bytestring += self.issue_subject_permission
        bytestring += self.issue_min_chain_depth
        bytestring += self.issue_chain_depth_range
        bytestring += self.issue_end_entity_type
        bytestring += self.request_subject_permission
        bytestring += self.request_min_chain_depth
        bytestring += self.request_chain_depth_range
        bytestring += self.request_end_entity_type
        bytestring += self.can_request_rollover
        bytestring += self.supported_symm_alg
        bytestring += self.public_encryption
        bytestring += self.public_curve_point
        bytestring += self.public_curve_data
        bytestring += self.verification_encyrption
        bytestring += self.verification_curve_point
        bytestring += self.verification_curve_data

        return bytestring
