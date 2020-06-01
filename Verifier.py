from fastecdsa import ecdsa
from datetime import datetime


class Verifier:

    """
    Wrapper function for fastecdsa.ecdsa.verify()
    See library documentation for that function, inputs are identical.
    """
    def verifySignature(self, r, s, message, publicKey):
        return ecdsa.verify((r,s), message, publicKey)
    
    # Returns true if less than 1s elapsed between message transmission and reception
    def verifyTime(self, timestamp):
        elapsed = self.calculateElapsedTime(timestamp)
        return (elapsed, elapsed < 1000)
    
    # calculate the number of elapsed milliseconds since the message was transmitted
    def calculateElapsedTime(self, timeInMilliseconds):
        unpaddedTimeInMilliseconds = ""
        for i in range(0,len(timeInMilliseconds)):
            if timeInMilliseconds[i] != "0":
                unpaddedTimeInMilliseconds = timeInMilliseconds[i:]
                break
        unpaddedTimeInMilliseconds = int(unpaddedTimeInMilliseconds, 16)
        origin = datetime(2004, 1, 1, 0, 0, 0, 0)
        now = (datetime.now() - origin).total_seconds() * 1000
        return now - unpaddedTimeInMilliseconds
