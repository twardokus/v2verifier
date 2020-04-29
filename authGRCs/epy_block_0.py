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
import time
import ecdsa

sign_keypath = "/home/administrator/v2v-capstone/keys/ecc_private.key"
signlog_path = "/tmp/sign.log"

class msg_block(gr.basic_block):  # other base classes are basic_block, decim_block, interp_block
    """Convert strings to uint8 vectors"""

    def __init__(self):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.basic_block.__init__(
            self,
            name='V2V ECDSA Signing Python Block',   # will show up in GRC
            in_sig=None,
            out_sig=None
        )
        self.message_port_register_out(pmt.intern('msg_out'))
        self.message_port_register_in(pmt.intern('msg_in'))
        self.set_msg_handler(pmt.intern('msg_in'), self.handle_msg)


    def signMessage(self, message):
        start = time.time()
        digest = SHA256.new()
        digest.update(message)
        shatime = time.time() - start
        private_key = False
        start = time.time()
        with open(sign_keypath, "r") as readfile:
            sk = ecdsa.SigningKey.from_string(readfile.read(), curve=ecdsa.NIST256p)
        opentime = time.time() - start
        start = time.time()
        sig = sk.sign(digest.digest())
        signtime = time.time() - start
        with open(signlog_path, "a+") as output:
            output.write(str(time.time())+"\t"+str(shatime)+"\t"+str(opentime)+"\t"+str(signtime)+"\n")
        return sig

    
    def handle_msg(self, msg):
        nvec = pmt.to_python(msg)
        nvec2 = self.signMessage(nvec)
	nvec = nvec+nvec2
        self.message_port_pub(pmt.intern('msg_out'), pmt.cons(pmt.make_dict(), pmt.pmt_to_python.numpy_to_uvector(np.array([ord(c) for c in nvec], np.uint8))))
    
    
    def work(self, input_items, output_items):
        pass
