from fastecdsa import keys, curve, ecdsa
from hashlib import sha256
import struct
import random
from datetime import datetime
import math


def get_certificate_format_string() -> str:
    """Function to return the format string used by generate_v2v_certificate

    :return: the format string for a V2V certificate to be used in call to struct.unpack()
    :rtype: str
    """
    return "BBBBQBB" + "4s" + "QHLBHLBB24xQBB24xQ31xB"


def get_certificate_fields_list() -> list:
    """Function to get a list of certificate fields for use with struct.unpack()

    :return: a list of certificate fields for use with struct.unpack()
    :rtype: list
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


def get_implicit_certificate(vehicle_hostname: str) -> bytes:
    """Get a byte representation of a 1609.2-compliant implicit certificate

    :return: byte representation of an implicit certificate
    :rtype: bytes
    """

    if len(vehicle_hostname) > 12:
        vehicle_hostname = vehicle_hostname[:12]

    while len(vehicle_hostname) < 12:
        vehicle_hostname = "0" + vehicle_hostname

    version = 3  # 0x03 -> version 3
    certificate_type = 1  # 0x01 -> implicit
    issuer = 128  # 0x80 -> self-issued, use SHA-256
    id = 129  # 0x81 -> hostname
    hostname = vehicle_hostname
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
    """Get a byte representation of a 1609.2-compliant explicit certificate

    :param hostname: the name of the certificate-bearing entity
    :type hostname: str
    :param private_key: the private key used to sign this certificate
    :type private_key: int

    :return: a byte representation of a V2V explicit certificate
    :rtype: bytes
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