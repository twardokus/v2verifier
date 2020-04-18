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
import ecdsa
import time
import random

public_keypath = "/home/user/ecc_public.key"

private_keypath = "/home/user/ecc_private.key"
sign_path = "/tmp/simsign.log"
ver_path = "/tmp/simverify.log"

mess = ''.join(random.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890-=!@#$%^&*()_+][}{;:/.,?><") for x in range(5000))

def signMessage(message, keypath):
    start = time.clock()
    digest = SHA256.new()
    digest.update(message)
    shatime = time.clock() - start
    start = time.clock()
    private_key = False
    with open(keypath, "r") as readfile:
        sk = ecdsa.SigningKey.from_string(readfile.read(), curve=ecdsa.NIST256p)
    opentime = time.clock() - start
    start = time.clock()
    sig = sk.sign(digest.digest())
    signtime = time.clock() - start
    with open(sign_path, "a+") as output:
        output.write(str(time.time())+"\t"+str(shatime)+"\t"+str(opentime)+"\t"+str(signtime)+"\n")
    return sig


def timesign( msg):
    nvec2 = signMessage(msg, private_keypath)
    return nvec2

def verifyMessage(sig, message): 
    start = time.clock()
    digest = SHA256.new()
    digest.update(message)
    shatime = time.clock() - start
    start = time.clock()
    public_key = False
    with open (public_keypath, "r") as readfile:
        vk = ecdsa.VerifyingKey.from_string(readfile.read(), curve=ecdsa.NIST256k1)
    opentime = time.clock() - start
    start = time.clock()
    verified = vk.verify(sig, digest.digest())
    verifytime = time.clock() - start
    with open(ver_path, "a+") as output:
        output.write(str(time.time())+"\t"+str(shatime)+"\t"+str(opentime)+"\t"+str(verifytime)+"\n")
    if verified:
        return True
    return False

def timeverify(msg, sig):
    result = verifyMessage(sig, msg)

with open(sign_path, "a+") as output:
    output.write("Time\t\tSHAtime\t\t\tfileopenTime\tsignTime\tmessLen="+str(len(mess))+'\n')
with open(ver_path, "a+") as output:
        output.write("Time\t\tSHAtime\t\t\tfileopenTime\tverifyTime\tmessLen="+str(len(mess))+'\n')

while 1:
    timeverify(mess, timesign(mess))
