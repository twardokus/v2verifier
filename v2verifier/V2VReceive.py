import V2VTransmit
import struct


def parse_received_spdu(spdu: bytes) -> tuple:
    """Parse a 1609.2 SPDU

    Parameters:
        spdu (bytes): a 1609.2 SPDU

    Returns:
        tuple: the contents of the SPDU

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
        "digest": spdu_contents[24]
    }

    for key in spdu_dict:
        print(key + "\t" + str(spdu_dict[key]))

    return spdu_contents

def verify_spdu(spdu_contents: dict) -> dict:
    """Perform security checks on received SPDU

    Parameters:
        spdu_contents (dict): the contents of a received SPDU as parsed with parse_received_spdu

    Returns:
        dict: security check results for the SPDU

    """




if __name__=="__main__":
    parse_received_spdu(V2VTransmit.generate_1609_spdu(V2VTransmit.generate_v2v_bsm(43, -71, 1543, 45.36, 145.223), 21))
