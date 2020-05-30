from fastecdsa import keys, curve, ecdsa
from fastecdsa.keys import import_key, export_key
from hashlib import sha256

"""
Little in this file is customized - the keys are generated and stored
using the standard functions from the imported cryptographic libraries.
"""

# The directory tree needs to be created before running this script
publicKeyPath = "/home/administrator/v2v-capstone/keys/p256.pub"
privateKeyPath = "/home/administrator/v2v-capstone/keys/p256.key"

privateKey, publicKey = keys.gen_keypair(curve.P256)

export_key(privateKey, curve=curve.P256, filepath=privateKeyPath)
export_key(publicKey, curve=curve.P256, filepath=publicKeyPath)
