from fastecdsa import ecdsa

"""
Wrapper function for fastecdsa.ecdsa.verify()
See library documentation for that function, inputs are identical.
"""
def verifyMessage(r,s,message,publicKey):
    try:
        return ecdsa.verify((r,s), message, publicKey)
    except:
        return False
