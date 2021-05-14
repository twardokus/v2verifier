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

    return spdu_contents


if __name__=="__main__":
    parse_received_spdu(V2VTransmit.generate_1609_spdu(V2VTransmit.generate_v2v_bsm(43, -71, 1543, 45.36, 145.223), 21))
