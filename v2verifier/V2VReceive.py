from typing import Tuple

import v2verifier.V2VCertificates
import struct
import os
import math
from datetime import datetime
import socket
from fastecdsa import ecdsa, point


def parse_received_spdu(spdu: bytes) -> dict:
    """Parse a 1609.2 SPDU. Assumes input spdu bytes begins with LLC (0xaaaa...) string;
    any preceding radio headers (or other prepended bytes) must be stripped before
    being passed to this function.

    :param spdu: a 1609.2 SPDU
    :type spdu: bytes

    :return: a dictionary containing the contents of the SPDU keyed by SPDU field
    :rtype: dict
    """

    spdu_dict = {}

    # llc_format_string = "!HbxxxH"
    # wsm_header_format_string = "bbbb"

    spdu_dict["llc"] = spdu[:8]

    spdu_dict["wsm_header"] = spdu[8:12]

    # Ieee1609Dot2Data structure is remainder of message after LLC and WSM headers are parsed
    dot2data = spdu[12:]

    current_byte = 0

    spdu_dict["protocol_version"] = dot2data[current_byte:current_byte + 1]
    current_byte += 1

    spdu_dict["content_type"] = dot2data[current_byte:current_byte + 1]
    current_byte += 1

    spdu_dict["hash_id"] = dot2data[current_byte:current_byte + 1]
    current_byte += 1

    spdu_dict["tbs_data"] = {}
    current_byte += 1  # 0x40 -> field delimiter, no need to save

    spdu_dict["tbs_data"]["protocol_version"] = dot2data[current_byte:current_byte + 1]
    current_byte += 1

    spdu_dict["tbs_data"]["content_type"] = dot2data[current_byte: current_byte + 1]
    current_byte += 1

    spdu_dict["tbs_data"]["length"] = dot2data[current_byte: current_byte + 1]
    current_byte += 1

    spdu_dict["tbs_data"]["unsecured_data"] = \
        dot2data[current_byte: current_byte + int.from_bytes(spdu_dict["tbs_data"]["length"], 'big')]
    current_byte += int.from_bytes(spdu_dict["tbs_data"]["length"], 'big')

    spdu_dict["header_info"] = {}
    current_byte += 2  # delimiter is 0x4001

    spdu_dict["header_info"]["psid"] = dot2data[current_byte:current_byte + 1]
    current_byte += 1

    spdu_dict["header_info"]["generation_time"] = dot2data[current_byte:current_byte + 8]
    current_byte += 8

    spdu_dict["signer_type"] = dot2data[current_byte:current_byte + 1]
    current_byte += 1

    if spdu_dict["signer_type"] == b'\x80':  # 0x80 -> digest
        spdu_dict["digest"] = dot2data[current_byte:current_byte + 8]
        current_byte += 8

    elif spdu_dict["signer_type"] == b'\x81':  # 0x81 -> certificate
        spdu_dict["certificate"], current_byte = parse_spdu_certificate(dot2data, current_byte)

    spdu_dict["signature_choice"] = dot2data[current_byte:current_byte + 1]
    current_byte += 1

    spdu_dict["signature"] = {}

    if spdu_dict["signature_choice"] == b'\x80':  # EcdsaP256Signature
        spdu_dict["signature"]["r_choice"] = dot2data[current_byte:current_byte + 1]
        current_byte += 1

        if spdu_dict["signature"]["r_choice"] == b'\x80' or \
            spdu_dict["signature"]["r_choice"] == b'\x81' or \
            spdu_dict["signature"]["r_choice"] == b'\x82' or \
            spdu_dict["signature"]["r_choice"] == b'\x83':

            spdu_dict["signature"]["r"] = dot2data[current_byte:current_byte + 32]
            current_byte += 32

        elif spdu_dict["signature"]["r_choice"] == b'\x84':  # uncompressed
            spdu_dict["signature"]["r"] = {}
            spdu_dict["signature"]["r"]["x"] = dot2data[current_byte:current_byte + 32]
            current_byte += 32
            spdu_dict["signature"]["r"]["y"] = dot2data[current_byte:current_byte + 32]
            current_byte += 32

        else:
            raise Exception("Unknown signature type specified.")

        spdu_dict["signature"]["s"] = dot2data[current_byte:current_byte + 32]
        current_byte += 32

    else:
        print("Received signature type - ", spdu_dict["signature_choice"])
        print(spdu_dict)
        raise Exception("Signatures other than ECDSA P256 not currently supported")

    return spdu_dict


def parse_spdu_certificate(dot2data: bytes, current_byte: int) -> Tuple[dict, int]:
    """Parse a certificate-type Signer substructure within an SPDU

    :param dot2data: the bytes of an Ieee1609Dot2Data structure
    :type dot2data: bytes
    :param current_byte: the byte offset where the certificate starts within dot2data
    :type current_byte: int

    :return a tuple containing a dictionary of the certificate fields/values and byte offset of end of certificate
    :rtype tuple
    """

    cert_dict = {}

    cert_dict["version"] = dot2data[current_byte:current_byte + 1]
    current_byte += 1

    cert_dict["cert_type"] = dot2data[current_byte:current_byte + 1]
    current_byte += 1
    
    if cert_dict["cert_type"] == b'\x01':  # 0x01 -> implicit certificate
        cert_dict["issuer"] = dot2data[current_byte:current_byte + 1]
        current_byte += 1
        
        cert_dict["id"] = dot2data[current_byte:current_byte + 1]
        current_byte += 1
        
        cert_dict["hostname"] = dot2data[current_byte:current_byte + 12]
        current_byte += 12

        cert_dict["craca_id"] = dot2data[current_byte:current_byte + 3]
        current_byte += 3

        cert_dict["crlseries"] = dot2data[current_byte:current_byte + 2]
        current_byte += 2

        cert_dict["validity_start"] = dot2data[current_byte:current_byte + 4]
        current_byte += 4

        cert_dict["validity_choice"] = dot2data[current_byte:current_byte + 1]
        current_byte += 1

        cert_dict["validity_duration"] = dot2data[current_byte:current_byte + 2]
        current_byte += 2

        cert_dict["verify_key_indicator_choice"] = dot2data[current_byte:current_byte + 1]
        current_byte += 1

        cert_dict["reconstruction_value_choice"] = dot2data[current_byte:current_byte + 1]
        current_byte += 1

        cert_dict["reconstruction_value"] = dot2data[current_byte:current_byte + 32]
        current_byte += 32

    else:
        raise Exception("Explicit certificates cannot be received at this time.")

    return cert_dict, current_byte


def parse_received_cv2x_spdu(spdu: bytes) -> dict:
    """Parse a 1609.2 SPDU received from COTS C-V2X equipment

    :param spdu: a 1609.2 SPDU with SAE J2735 BSM
    :type spdu: bytes

    :return: a dictionary containing the contents of the SPDU keyed by SPDU field
    :rtype: dict
    """
    # Return an empty dict if this SPDU is too short to be a BSM (e.g., a control message)
    if len(spdu) < 150:
        return {}

    # drop headers
    spdu = spdu[42:]

    spdu_dict = {
        "latitude": struct.unpack("!f", spdu[10:14]),
        "longitude": struct.unpack("!f", spdu[14:18]),
        "elevation": struct.unpack("!f", spdu[18:19]),
        "speed": struct.unpack("!f", spdu[25:26]),
        "heading": struct.unpack("!f", spdu[26:27])
    }

    return spdu_dict


def verify_spdu(spdu_dict: dict, public_key: point.Point) -> dict:
    """Perform security checks on received SPDU

    :param spdu_dict: the contents of a received SPDU as parsed with parse_received_spdu
    :type spdu_dict: dict
    :param public_key: the public key to use for verifying the message signature
    :type public_key: fastecdsa.point.Point

    :return: security check results for the SPDU
    :rtype: dict
    """

    # Verify the timestamp

    # SAE J2945, 30sec delay is allowed
    max_allowed_elapsed_microseconds = 30000

    elapsed = math.floor((datetime.now() -
                          datetime(2004, 1, 1, 0, 0, 0, 0)).total_seconds() * 1000) \
                                - int.from_bytes(spdu_dict["header_info"]["generation_time"],'big')

    unexpired = True if elapsed < max_allowed_elapsed_microseconds else False

    # Verify the signature
    if spdu_dict["signature_choice"] == b'\x80':  # ECDSA P256

        r = int.from_bytes(spdu_dict["signature"]["r"], 'big')
        s = int.from_bytes(spdu_dict["signature"]["s"], 'big')

        # openssl dgst -sha256 -verify public.pem -signature test.sha256 test.py
        # openssl_verify_command = "openssl dgst -sha256 -verify public.pem -signature SIGNATURE_DIGEST SIGNED_DATA"

        valid_signature = ecdsa.verify((r, s), spdu_dict["tbs_data"]["unsecured_data"], public_key)

        signature_type = "ecdsa_p256"

    else:
        raise Exception("Verification for signatures other than ECDSA P256 is not supported.")

    return {"signature_type": signature_type,
            "valid_signature": valid_signature,
            "unexpired": unexpired,
            "elapsed": elapsed}


def report_bsm_gui(bsm: tuple, verification_dict: dict, ip_address: str, port: int) -> None:
    """Send BSM data and verification status to the V2Verifier GUI via UDP datagram

    :param bsm: a tuple of BSM information matching the format returned by v2verifier.V2VTransmit.generate_v2v_bsm()
    :type bsm: tuple
    :param verification_dict: a dictionary containing verification information about the BSM
    :type verification_dict: dict
    :param ip_address: the IP address of the GUI
    :type ip_address: str
    :param port: the port on ip_address where the GUI service is running
    :type port: int
    """

    data = struct.pack("!5f??f",
                       bsm[0],
                       bsm[1],
                       bsm[2],
                       bsm[3],
                       bsm[4],
                       verification_dict["valid_signature"],
                       verification_dict["unexpired"],
                       verification_dict["elapsed"]
                       )

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(data, (ip_address, port))


def extract_bsm_data(bsm: bytes, verification_dict: dict) -> tuple:
    """Return a tuple containing the data elements of a BSM

    :param bsm: the bsm bytes to parse
    :type bsm: bytes
    :param verification_dict: verification information from verify_spdu()
    :type verification_dict: dict

    :return: the BSM data elements
    :rtype: tuple
    """
    return struct.unpack("!fffff", bsm)


def get_bsm_report(bsm: bytes, verification_dict: dict) -> str:
    """Create a report about a received SPDU. Intended to generate output for printing to console.

    :param bsm: BSM data in byte format as packed by v2verifier.V2VTransmit.generate_bsm()
    :type bsm: bytes
    :param verification_dict: a dictionary containing verification information about an SPDU
    :type verification_dict: dict

    :return: a string containing information about an SPDU to be displayed (e.g., printed to console)
    :rtype: str
    """
    bsm = struct.unpack("!fffff", bsm)

    report = ""
    report += "Vehicle reports location "
    report += str(round(bsm[0], 5))
    report += ", "
    report += str(round(bsm[1], 5))
    report += " at elevation " + str(round(bsm[2], 3)) + " meters"
    report += "\n"

    report += "Current speed " + str(round(bsm[3], 3)) + " m/s on bearing " + str(round(bsm[4], 3)) + " degrees"
    report += "\n"

    report += "Message is "
    report += "validly" if verification_dict["valid_signature"] else "NOT VALIDLY"
    report += " signed"

    report += "\n"

    report += "Message is "
    report += "unexpired " if verification_dict["unexpired"] else "EXPIRED "
    report += "(" + str(verification_dict["elapsed"]) + " microseconds elapsed)"

    report += "\n"

    return report


def report_spdu(spdu_dict: dict) -> str:
    """A testing/debugging function that returns a printable report of SPDU contents after parsing

    :param spdu_dict: a dictionary containing SPDU fields such as returned from parse_received_spdu()
    :type spdu_dict: dict

    :return: a string representation of the SPDU fields
    :rtype str
    """

    report = ""

    for key in spdu_dict.keys():
        report += key + "\t\t\t" + str(spdu_dict[key]) + "\n"

    return report


def report_cots_cv2x_bsm(bsm: dict) -> str:
    """A function to report the BSM information contained in an SPDU from a COTS C-V2X device

    :param bsm: a dictionary containing BSM fields from a C-V2X SPDU
    :type bsm: dict

    :return: a string representation of the BSM fields
    :rtype: str
    """
    report = ""

    for key in bsm.keys():
        report += key + "\t\t\t" + str(bsm[key]) + "\n"

    report += "\n"

    return report
