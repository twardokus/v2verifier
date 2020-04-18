"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
import pylab
from gnuradio import gr
import pmt
from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5
from Crypto.PublicKey import RSA
import time
import timeit

private_keypath = "/home/user/private_key.pem"
sign_path = "/tmp/simsign.log"
public_keypath = "/home/user/key.pub"
ver_path = "/tmp/simverify.log"

mess = "asdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasd"

def signMessage(message, keypath):
    digest = SHA256.new()
    digest.update(message)

    private_key = False
    with open(keypath, "r") as readfile:
        private_key = RSA.importKey(readfile.read())

    signer = PKCS1_v1_5.new(private_key)
    sig = signer.sign(digest)
    return sig


def timesign( msg):
    start = time.clock()
    nvec2 = signMessage(msg, private_keypath)
    perf = time.clock()-start
    with open(sign_path, "a+") as output:
        output.write("Sign Time: "+str(time.time())+ " perf: "+str(perf)+"\n")
    return nvec2

def verifyMessage(sig, message):        
    digest = SHA256.new()
    digest.update(message)
    public_key = False
    with open (public_keypath, "r") as readfile:
        public_key = RSA.importKey(readfile.read())
    verifier = PKCS1_v1_5.new(public_key)
    verified = verifier.verify(digest, sig)
    if verified:
        return True
    return False

def timeverify(msg, sig):
    start = time.clock()
    result = verifyMessage(sig, msg)
    perf = time.clock()-start
    with open(ver_path, "a+") as output:
        output.write("Time: "+str(time.time())+ " perf: "+str(perf) + "\n")

while 1:
    timeverify(mess, timesign(mess))
