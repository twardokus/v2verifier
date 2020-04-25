from fastecdsa import ecdsa

# wrapper function for fastecdsa.ecdsa.verify()
def verifyMessage(r,s,message,publicKey):
    return ecdsa.verify((r,s), message, publicKey)
