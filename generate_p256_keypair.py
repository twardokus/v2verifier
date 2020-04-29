from fastecdsa import keys, curve, ecdsa
from fastecdsa.keys import import_key, export_key
from hashlib import sha256

publicKeyPath = "/home/administrator/v2v-capstone/keys/p256.pub"
privateKeyPath = "/home/administrator/v2v-capstone/keys/p256.key"

privateKey, publicKey = keys.gen_keypair(curve.P256)

print privateKey
print publicKey

export_key(privateKey, curve=curve.P256, filepath=privateKeyPath)
export_key(publicKey, curve=curve.P256, filepath=publicKeyPath)

"""
# Test code

def testKeys():
	private, public = import_key(privateKeyPath)

	print private
	print public

	message = "Test message"

	r, s = ecdsa.sign(message, private, hashfunc=sha256)
	print ecdsa.verify((r,s),message, public, hashfunc=sha256)

if __name__=="__main__":
	testKeys()
"""
