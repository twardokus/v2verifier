import V2VTransmit

def parse_received_spdu(spdu: bytes) -> tuple:
    llc_format_string = "HbxxxH"
    wsm_header_format_string = "bbbb"

    ieee1609_dot2_data_format_string = "bBbbbBB"
    bsm_format_string = "fffff"
    ieee1609_dot2_data_format_string += bsm_format_string
    ieee1609_dot2_data_format_string += "BBBQBQ"
    ieee1609_dot2_data_format_string += "BB"

    spdu_format_string = llc_format_string + wsm_header_format_string + ieee1609_dot2_data_format_string

    payload, signature = spdu[:-64], spdu[-64:]



if __name__=="__main__":
    parse_received_spdu(V2VTransmit.generate_1609_spdu(b'test',0))
