#Description: Library of base utility functions and variables needed to generate pads, encode/decode messages
#Author : juju
import os, hashlib, time, uuid
import random #Only used to sample Mixed Alphabet During Padding of our message before encoding with our OTP key, so we get 1 out of n chars from Mixedbet

MIXEDBET = ',d]+[y$nc%/.4|m( xu3*2;gbl0=s)97pz!&o?@^8#rvw5f1i{6tke_jha-q}' #Mix it up DJ

#Pre: Gets the available Entropy from the kernel
#Post: If entropy is above 300 return True, else Return False
def getEntropy():
    try:
        x = os.popen('cat /proc/sys/kernel/random/entropy_avail').read()
        x = int(x)
        if x >= 300:
            return True
        else:
            return False
    except:
        print 'Error Determining your systems Entropy Level, are you using a Linux System'
        return False

#Post: Generates a random UUID and returns it as string
def randuuid():
    return str(uuid.uuid4())

#Post: Grabs the current Unix timestamp and returns it as an integer
def gettime():
    ts = int(time.time())
    return ts

#Pre: Given an integer n, Generate n number of Random bytes from the Operating Systems 'Random source'
#Post: Returns n number of Random Bytes (Not advised to print this data)
def randbytes(n):
    return os.urandom(n)
        
#Pre: Given a source of data returns 256Bits - 64 Hex Number
#Post: Returns a 64 Hexdecimal Number (256bits of data)
def sha256(DATA):
    return hashlib.sha256(DATA).hexdigest()
    
#Pre: Given an integer n, Generate n number of Hex Digits asked    
#Post: A string of hexdigits sized n number
def randhex(n):
    g = ''
    for x in range(1, n+1):
        g+=sha256(randbytes(32))[-1]
    return g
    
#Pre: Given a Hex Character
#Post: Returns a Shiftvalue as integer
def hexshift(c):
    return  int(c, 16)

#Pre: Given a HEX KEY
#Post: Returns a list of integers which contain how much you need to shift a string by to encode/decode it
def shiftlist(KEY):
    SHIFTLIST = []
    for c in KEY:
        SHIFTLIST.append(hexshift(c))
    return SHIFTLIST    

#Pre: Given a MSG which is shorter than our encryption key
#Post: Pads the MSG to be equal length to our encryption key
def padmessage(MSG, KEY):
    MSG = MSG.lower()
    if len(MSG) < len(KEY):
        x = len(KEY) - len(MSG)
        for y in range(x):
            SHUFFLEBET = ''.join(random.sample(MIXEDBET, len(MIXEDBET)))
            MSG+=SHUFFLEBET[hexshift(randhex(1))]
    return MSG

#Pre: Given a message and a Key
#Post: Returns an Encoded message using the given message and Key
def encode(MSG, KEY):
    ENCODED_MSG = ''
    if len(MSG) <= len(KEY):
        MSG=padmessage(MSG,KEY)
        shifts = shiftlist(KEY)
        for shift, c in zip(shifts, MSG):
            index = MIXEDBET.index(c)
            if index+shift < len(MIXEDBET):
                shiftedchar = MIXEDBET[index+shift]
            else:
                position = (index+shift)-len(MIXEDBET)
                shiftedchar = MIXEDBET[position]
            ENCODED_MSG+=shiftedchar
        return ENCODED_MSG
    else:
        print 'Your message is longer than the KEY'

#Pre: Given an Encoded message and a key
#Post: Returns a decoded Message in readable format
def decode(ENCODED_MSG, KEY):
    DECODED_MSG=''
    if len(ENCODED_MSG) <= len(KEY):
        shifts = shiftlist(KEY)
        for shift, c in zip(shifts, ENCODED_MSG):
            index = MIXEDBET.index(c)
            if index-shift >= 0:
                shiftedchar = MIXEDBET[index-shift]
            else:
                position = index - shift
                shiftedchar = MIXEDBET[position]
            DECODED_MSG+=shiftedchar
        return DECODED_MSG
    else:
        print 'Your encoded message is logner than the Key'