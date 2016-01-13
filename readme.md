# OTPyd

OTPyd is an implementation of a one time pad written in python. This project was designed for educational purposes, their is no gurantee of the security of the pad as the code has not yet been reviewed. [One Time Pad]

  - Generates a Pad between two date ranges
  - Entropy Checks, Linux Printing, CSV and HTML output
  - Encode and Decode functions

### Version
0.0.1

### Usage

```python
from datetime import date
#Import OTPY Library
from otpy import OTPY
from otpyutil import getEntropy, encode, decode, MIXEDBET

#Using the OTPY Library
#If the OS has a good amount of entropy available should be above above 300 or this will fail
if getEntropy():
    #Create OTPY Object with your given entropy
    OTP = OTPY('EFDS#WEDAWEasdasd213####234#@#!@asd#ASDcsxdvlkn(*)&&$%@Q#$!@$@RWERF@324234$#!#@WEDA@#$R@#QW!WEDA@#!@#!@#!ASDFFGHHKJ%^&$%#TFE')

    #Create your date range 11/26/2015 - 11/26/2015
    date1 = date(2015, 11, 26)
    date2 = date(2016, 11, 26)

    #Create a Pad with range date1 to date2
    pad = OTP.newpad(date1, date2)
    
    #View your pad
    pad.viewPad()
        
    #Write the Pad out to a csv file
    pad.createCSV('pad.csv')
        
    #Try to print your csv file to paper (Only Linux Supported)
    #pad.linuxprint()

    #Write the pad to an HTML document
    pad.createHTML('pad.html')
        
    #Create a new pad and import the old CSV Pad into it, then compare that they are the same
    newpad = OTP.newpad(date1, date2) #Right now they dont match
        
    #If needed you can recreate the pad from a csv file
    newpad.importPad('pad.csv') #Now they should match
        
    #Quick Check to verify the Import function works
    #if pad.pyd == newpad.pyd:
        #print 'Successful Import'
    
    print '----------------------------------------------------------------------------------------------------------------------------------'
    #How to Encode and Decode messages using a daily key
    KEY = '382cb4a86545b35d44a2755aabf9ce796fb5ca1741b2012cce1c4280da7944e25830ba02a011d92a14d9b84f313382d8c052df06ed03e8fa5453d80c41ccf6fe'
    MSG = '1238h01i23jdf sdf meet me at the old abandoned barn at 9pm  random shit 2103498yh12384rinwef'
    print 'MSG: ', MSG
    print 'KEY: ', KEY
    print 'Alphabet:', MIXEDBET
    ENCODED_MSG = encode(MSG, KEY)
    print  'Encoded MSG: ', ENCODED_MSG
    DECODED_MSG = decode(ENCODED_MSG,KEY)
    print 'Decoded MSG: ', DECODED_MSG   
    
    if DECODED_MSG == MSG:
        print 'Message Encode/Decode Successful'
else: 
    'Not enough Entropy'
```

### Development

Want to contribute? Great! Make a pull request, if someone wants to review it also let me know.

### Todos

 - Code Review
 - Windows Printing
 - Offline/Online Checks
 - Additional sources of entropy

License
----

MIT


**Free Software, Hell Yeah!**

[One Time Pad]: <https://en.wikipedia.org/wiki/One-time_pad>
