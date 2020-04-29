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
from Crypto.Hash import SHA384
import time
import random
from fastecdsa.keys import import_key
from fastecdsa import curve, ecdsa
from fastecdsa.encoding.der import DEREncoder
MESS_LEN = 5
public_keypath = "/home/user/fastecc_public.key"
private_keypath = "/home/user/fastecc_private.key"
sign_path = "/tmp/simsign.log"
ver_path = "/tmp/simverify.log"

#MESSAGE = ''.join(random.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890-=!@#$%^&*()_+][}{;:/.,?><") for x in range(MESS_LEN))
MESSAGE = "asd"

def signMessage(message):
    start = time.clock()
    digest = SHA384.new()
    digest.update(message)
    shatime = time.clock() - start
    start = time.clock()
    private_key, asd = import_key(private_keypath)
    #print("private_key:" + str(private_key))
    opentime = time.clock() - start
    start = time.clock()
    r, s = ecdsa.sign(message, private_key)
    sig = DEREncoder.encode_signature(r, s)
    signtime = time.clock() - start
    #print(len(sig))
    #print(sig)
    with open(sign_path, "a+") as output:
        output.write(str(time.time())+"\t"+str(shatime)+"\t"+str(opentime)+"\t"+str(signtime)+"\n")
    return sig


def timesign( msg):
    nvec2 = signMessage(msg) + msg
    return nvec2

def verifyMessage(sig, message): 
    start = time.clock()
    digest = SHA384.new()
    digest.update(message)
    shatime = time.clock() - start
    start = time.clock()
    r, s = DEREncoder.decode_signature(sig)
    empty, public_key = import_key(public_keypath)
    opentime = time.clock() - start
    start = time.clock()
    verified = ecdsa.verify((r, s), message, public_key, curve=curve.P256)
    verifytime = time.clock() - start
    with open(ver_path, "a+") as output:
        output.write(str(time.time())+"\t"+str(shatime)+"\t"+str(opentime)+"\t"+str(verifytime)+"\n")
    if verified:
        return True
    return False


with open(sign_path, "a+") as output:
    output.write("Time\t\tSHAtime\t\t\tfileopenTime\tsignTime\tmessLen="+str(MESS_LEN)+'\n')
with open(ver_path, "a+") as output:
        output.write("Time\t\tSHAtime\t\t\tfileopenTime\tverifyTime\tmessLen="+str(MESS_LEN)+'\n')

while 1:
    packet = timesign(MESSAGE)
    siglen = ord(packet[1]) + 2
    sig = packet[:siglen]
    mess = packet[siglen:]
    print(verifyMessage(sig, mess))
