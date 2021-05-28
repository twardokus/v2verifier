import v2verifier.V2VCertificates
import struct
import math
from datetime import datetime
import socket
from fastecdsa import ecdsa, point


def parse_received_spdu(spdu: bytes) -> dict:
    """Parse a 1609.2 SPDU

    Parameters:
        spdu (bytes): a 1609.2 SPDU

    Returns:
        dict: the contents of the SPDU

    """

    llc_format_string = ">HbxxxH"
    wsm_header_format_string = "bbbb"

    ieee1609_dot2_data_format_string = "bBbbbBB"
    bsm_format_string = "fffff"
    ieee1609_dot2_data_format_string += bsm_format_string
    ieee1609_dot2_data_format_string += "BBBQB"
    ieee1609_dot2_data_format_string += "BBBB12s3s2sLBHBB32x"
    ieee1609_dot2_data_format_string += "BB"

    spdu_format_string = llc_format_string + wsm_header_format_string + ieee1609_dot2_data_format_string

    payload, signature = spdu[:-64], spdu[-64:]

    # spdu_contents will be a tuple containing each element of the 1609.2 SPDU as constructed
    # using V2VTransmit.generate_1609_spdu()
    spdu_contents = struct.unpack(spdu_format_string, payload)

    # spdu_dict = {
    #     "llc_dsap_and_ssap": spdu_contents[0],
    #     "llc_control": spdu_contents[1],
    #     "llc_type": spdu_contents[2],
    #     "wsmp_n_subtype_opt_version": spdu_contents[3],
    #     "wsmp_n_tpid": spdu_contents[4],
    #     "wsmp_t_header_length_and_psid": spdu_contents[5],
    #     "wsmp_t_length": spdu_contents[6],
    #     "wsmp_protocol_version": spdu_contents[7],
    #     "wsmp_content_type": spdu_contents[8],
    #     "wsmp_hash_id": spdu_contents[9],
    #     "bsm_length": spdu_contents[13],
    #     "bsm": spdu_contents[14:19],
    #     "header_psid": spdu_contents[21],
    #     "generation_time": spdu_contents[22],
    #     "signer_identifier": spdu_contents[23],
    #     "signer": spdu_contents[24],
    #     "certificate_version_type": spdu_contents[25],
    #     "certificate_type": spdu_contents[26],
    #     "issuer": spdu_contents[27],
    #     "hashedID": spdu_contents[28],
    #     "start_tbs_data": spdu_contents[29],
    #     "hostname_length": spdu_contents[30],
    #     "hostname": spdu_contents[31],
    #     "craca_id": spdu_contents[32],
    #     "crl_series": spdu_contents[33],
    #     "start_validity": spdu_contents[34],
    #     "spacer": spdu_contents[35],
    #     "certificate_duration": spdu_contents[36],
    #     "filler": spdu_contents[37],
    #     "psid": spdu_contents[38],
    #     "verification_key_indicator": spdu_contents[39],
    #     "ecc_public_key_y": spdu_contents[40],
    #     "start_signature": spdu_contents[41],
    #     "ecc_public_key_x_indicator": spdu_contents[42],
    #     "ecc_public_key_x": spdu_contents[43],
    #     "s": spdu_contents[44],
    #     "signature": signature
    # }
    spdu_dict = {
        "llc_dsap_and_ssap": spdu_contents[0],
        "llc_control": spdu_contents[1],
        "llc_type": spdu_contents[2],
        "wsmp_n_subtype_opt_version": spdu_contents[3],
        "wsmp_n_tpid": spdu_contents[4],
        "wsmp_t_header_length_and_psid": spdu_contents[5],
        "wsmp_t_length": spdu_contents[6],
        "wsmp_protocol_version": spdu_contents[7],
        "wsmp_content_type": spdu_contents[8],
        "wsmp_hash_id": spdu_contents[9],
        "bsm_length": spdu_contents[13],
        "bsm": spdu_contents[14:19],
        "header_psid": spdu_contents[21],
        "generation_time": spdu_contents[22],
        "signer_identifier": spdu_contents[23],
        "version": spdu_contents[24],
        "certificate_type": spdu_contents[25],
        "issuer": spdu_contents[26],
        "id": spdu_contents[27],
        "hostname": spdu_contents[28],
        "craca_id": spdu_contents[29],
        "crlseries": spdu_contents[30],
        "validity_period_start": spdu_contents[31],
        "validity_period_choice": spdu_contents[32],
        "validity_period_duration": spdu_contents[33],
        "verify_key_indicator_choice": spdu_contents[34],
        "reconstruction_value_choice": spdu_contents[35],
        "digest": spdu_contents[24],
        "signature": signature
    }
    print(spdu_dict)
    return spdu_dict


def verify_spdu(spdu_dict: dict, public_key: point.Point) -> dict:
    """Perform security checks on received SPDU

    Parameters:
        spdu_dict (dict): the contents of a received SPDU as parsed with parse_received_spdu
        public_key (fastecdsa.point.Point): the public key to use for verifying the message signature

    Returns:
        dict: security check results for the SPDU

    """

    # Verify the timestamp

    # SAE J2945, 30sec delay is allowed
    max_allowed_elapsed_microseconds = 30000

    elapsed = math.floor((datetime.now() -
                          datetime(2004, 1, 1, 0, 0, 0, 0)).total_seconds() * 1000) - spdu_dict["generation_time"]

    unexpired = True if elapsed < max_allowed_elapsed_microseconds else False

    # Verify the signature

    r = int.from_bytes(spdu_dict["signature"][:32], "little")
    s = int.from_bytes(spdu_dict["signature"][32:], "little")

    reassembled_message = struct.pack(">fffff",
                                      spdu_dict["bsm"][0],
                                      spdu_dict["bsm"][1],
                                      spdu_dict["bsm"][2],
                                      spdu_dict["bsm"][3],
                                      spdu_dict["bsm"][4]
                                      )

    valid_signature = ecdsa.verify((r, s), reassembled_message, public_key)

    return {"valid_signature": valid_signature, "unexpired": unexpired, "elapsed": elapsed}


def report_bsm_gui(bsm: tuple, verification_dict: dict, ip_address: str, port: int) -> None:
    """Send BSM data and verification status to the V2Verifier GUI

    Parameters:
        bsm (tuple): a tuple containing BSM information
        verification_dict (dict): a dictionary containing verification information about the BSM
        ip_address (str): the IP address of the GUI
        port (int): the port on ip_address where the GUI service is running

    Returns:
        None

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


def report_bsm(bsm: tuple, verification_dict: dict) -> str:
    """Generate a report about a received SPDU. Intended to generate output for printing to console.

    Parameters:
        bsm (tuple): a tuple containing BSM information
        verification_dict (dict): a dictionary containing verification information about an SPDU

    Returns:
        str: a string containing information to be displayed (e.g., to console) about an SPDU

    """

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
