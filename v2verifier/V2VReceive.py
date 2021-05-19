import v2verifier.V2VTransmit
import struct
import math
from datetime import datetime
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
    ieee1609_dot2_data_format_string += "BBBQBQ"
    ieee1609_dot2_data_format_string += "BB"

    spdu_format_string = llc_format_string + wsm_header_format_string + ieee1609_dot2_data_format_string

    payload, signature = spdu[:-64], spdu[-64:]

    # spdu_contents will be a tuple containing each element of the 1609.2 SPDU as constructed
    # using V2VTransmit.generate_1609_spdu()
    spdu_contents = struct.unpack(spdu_format_string, payload)

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
        "psid": spdu_contents[21],
        "generation_time": spdu_contents[22],
        "signer_identifier": spdu_contents[23],
        "digest": spdu_contents[24],
        "signature": signature
    }

    return spdu_dict


def verify_spdu(spdu_dict: dict, public_key: point.Point) -> dict:
    """Perform security checks on received SPDU

    Parameters:
        spdu_dict (dict): the contents of a received SPDU as parsed with parse_received_spdu
        public_key (fastecdsa.point.Point): the public key to use for verifying the message signature

    Returns:
        dict: security check results for the SPDU

    """

    # SAE J2945, 30sec delay is allowed
    max_allowed_elapsed_microseconds = 30000

    elapsed = math.floor((datetime.now() -
                          datetime(2004, 1, 1, 0, 0, 0, 0)).total_seconds() * 1000) - spdu_dict["generation_time"]

    unexpired = True if elapsed < max_allowed_elapsed_microseconds else False

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

    return {"valid_signature": valid_signature}


def report_bsm(bsm: tuple, verification_dict: dict) -> str:
    """Generate a report about a received SPDU

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
    report += "VALIDLY" if verification_dict["valid_signature"] else "NOT VALIDLY"
    report += " signed"

    report += "\n"

    return report
