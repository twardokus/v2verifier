import math
import time
import v2v_security


def generate_16092_spdu(payload, private_key):

    # specify options that never change
    # Version = 0x03
    # ContentType = 0x81 (signedData)
    # HashAlgorithm = 0x00 (SHA-256)
    # ContentType = 0x80 (unsecuredData)
    spdu = b'\x03\x81\x00\x40\x03\x80'

    # Length
    spdu += b'\x38'

    # insert payload (goes into unsecuredData field)
    spdu += payload

    # begin headerInfo substructure
    spdu += b'\x40\x01'

    # PSID
    spdu += b'\x20'

    # generationTime64
    spdu += math.floor(time.time() * 1000).to_bytes(8, 'big')

    # begin signer substructure
    spdu += b'\x80'

    # HashedID
    # TODO: replace this with function call to retrieve signer's cert. hashID
    spdu += b'\x00\x00\x00\x00\x00\x00\x00\x00'

    # begin signature
    spdu += b'\x80\x80'

    r, s = v2v_security.ecdsa_sign_message(payload, private_key)
    r = r.to_bytes(32, 'big')
    s = s.to_bytes(32, 'big')

    spdu += r + s

    return spdu

