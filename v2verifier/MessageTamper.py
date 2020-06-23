from v2verifier.attacks.ReplayAttacker import ReplayAttacker

class MessageTamper(ReplayAttacker):
    
    def __init__(self, pattern, replacement):
        self.pattern = pattern
        self.replacement = replacement
        super()
    
    def messageTamperingAttack(self, interval):
        self.collect(interval)
        self.replay()
    
    def storeMessage(self, message):
        message = self.modify(message, self.pattern, self.replacement)
        ReplayAttacker.storeMessage(self, message)
    
    def modify(self, message, pattern, replacement):
        if len(pattern) == len(replacement) and self.isHex(replacement):
            message = message.replace(pattern, replacement)
        return message
    
    def isHex(self, value):
        for char in value:
            if char not in "0123456789abcdefABCDEF":
                return False
        return True