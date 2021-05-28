from fastecdsa import keys, curve, ecdsa
from hashlib import sha256
import struct
import random
from datetime import datetime
import math


def get_certificate_format_string() -> str:
    """Function to return the format string used by generate_v2v_certificate



    Returns:
        str: the format string for a V2V certificate to be used in call to struct.unpack()

    """
    return "BBBBQBB" + "4s" + "QHLBHLBB24xQBB24xQ31xB"


def get_certificate_fields_list() -> list:
    """Function to get a list of certificate fields for use with struct.unpack()

    Returns:
        list: a list of certificate fields for use with struct.unpack()

    """
    return [
        "signer",
        "certificate_version_type",
        "certificate_type",
        "issuer",
        "hashedID",
        "start_tbs_data",
        "hostname_length",
        "hostname",
        "craca_id",
        "crl_series",
        "start_validity",
        "spacer",
        "certificate_duration",
        "filler",
        "psid",
        "verification_key_indicator",
        "ecc_public_key_y",
        "start_signature",
        "ecc_public_key_x_indicator",
        "ecc_public_key_x",
        "s"
    ]


def get_implicit_certificate() -> bytes:
    """Get a byte representation of a 1609.2-compliant implicit certificate

    :return: byte representation of an implicit certificate
    :rtype: bytes

    """
    version = 3  # 0x03 -> version 3
    certificate_type = 129  # 0x81 -> implicit
    issuer = 128  # 128 -> self-issued, use SHA-256
    id = 129  # 0x81 -> hostname
    hostname = "demo_vehicle"  # fixed, do not change
    craca_id = 0  # 0x000000 -> we have no certificate revocation authority (yet)
    crlseries = 0 # 0x0000 -> we have no CRLs issued by a CRLCA, either
    validity_period_start = math.floor((datetime.now() - datetime(2004, 1, 1, 0, 0, 0, 0)).total_seconds())
    validity_period_choice = 132  # 0x84 -> hours
    validity_period_duration = 24  # 0x0018 -> 24 hours
    verify_key_indicator_choice = 129  # 0x81 -> reconstructionValue
    reconstruction_value_choice = 128  # 0x80 -> x-only
    reconstruction_value = 0  # 32-byte null field as we don't support this yet

    implicit_certificate = struct.pack("!BBBB12s3s2sLBHBB32x",
                                       version,
                                       certificate_type,
                                       issuer,
                                       id,
                                       hostname.encode(),
                                       bytes([craca_id]),
                                       bytes([crlseries]),
                                       validity_period_start,
                                       validity_period_choice,
                                       validity_period_duration,
                                       verify_key_indicator_choice,
                                       reconstruction_value_choice,
                                       # reconstruction_value
                                       )

    return implicit_certificate


def get_explicit_certificate(hostname: str, private_key: int) -> bytes:
    """Generate a V2V certificate to use for signing messages

    Parameters:
        hostname (str): the name of the certificate-bearing entity
        private_key (int): the private key of the requester

    Returns:
        bytes: a byte representation of a V2V certificate

    """

    signer = 129  # 0x81 -> certificate
    certificate_version_type = 3  # 0x03 -> version 3
    certificate_type = 1  # 0x01 -> implicit
    issuer = 128  # 0x80 -> sha256Digest
    hashed_id = random.randint(1, 10000000)  # since we aren't actually hashing anything

    v2v_certificate = struct.pack("!BBBBQ",
                                  signer,
                                  certificate_version_type,
                                  certificate_type,
                                  issuer,
                                  hashed_id
                                  )

    start_tbs_data = 16  # 0x10 -> start of structure
    hostname_length = len(hostname)

    v2v_certificate += struct.pack("!BB",
                                   start_tbs_data,
                                   hostname_length
                                   )

    v2v_certificate += hostname.encode()

    craca_id = 0  # 0x000000 -> placeholder
    crl_series = 0  # 0x0000 -> placeholder

    # time in seconds (per 1609.2, section 6.4.15) since 00:00:00 UTC, 1 Jan. 2004
    start_validity = math.floor((datetime.now() - datetime(2004, 1, 1, 0, 0, 0, 0)).total_seconds())

    spacer = 132  # 0x84 -> ?? TODO: why?

    certificate_duration = 24  # time in hours, we'll default to 1-day periods for now

    filler = 16842753  # TODO: why?

    psid = 32  # 0x20 -> "vehicle safety and awareness" (per Wireshark, likely an SAE designation)

    v2v_certificate += struct.pack("!QHLBHLB",
                                   craca_id,
                                   crl_series,
                                   start_validity,
                                   spacer,
                                   certificate_duration,
                                   filler,
                                   psid
                                   )

    verification_key_indicator = 129  # 0x81 -> reconstructionValue

    v2v_certificate += struct.pack("!B", verification_key_indicator)

    ecc_public_key_y = random.randint(1, 1000000)  # should be calculated TODO: fix this
    v2v_certificate += struct.pack("!24xQ", ecc_public_key_y)  # TODO: fix this to remove null bytes

    start_signature = 128  # 0x80 -> start of signature substructure
    ecc_public_key_x_indicator = 128  # 0x80 -> choice of format for r-value (x-coord)

    v2v_certificate += struct.pack("!BB", start_signature, ecc_public_key_x_indicator)

    # TODO: this should be the actual public key (or signature?) of the requesting entity
    ecc_public_key_x = random.randint(1, 1000000)
    s = 32
    v2v_certificate += struct.pack("!24xQ31xB", ecc_public_key_x, s)

    return v2v_certificate


class V2VCertificate:
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
        self.toBeSigned = ToBeSignedCertificate(hostname).toString().encode("utf-8").hex()

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

        r, s = ecdsa.sign(self.toBeSigned, private_key, hashfunc=sha256)
        
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


if __name__ == "__main__":
    """Test code"""
    print(get_implicit_certificate().hex())
