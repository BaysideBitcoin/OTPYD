#Description : Generates OTP for a given date range, can be used to encode, decode messages. Writes Pad out to CSV and HTML format, also has a print function for Linux
#Author : juju
from otpyutil import sha256
from otpyd import OTPYD

class OTPY:
    def __init__(self, entropy):
        self.entropy = entropy #Source of User Inputted Entropy
        self.hashedentropy = sha256(entropy) #Hex Values we can pull from given the User Inputted Entropy

    def newpad(self, date1, date2):
        pad = OTPYD(self.entropy, self.hashedentropy)
        pad.generatePad(date1,date2)
        return pad