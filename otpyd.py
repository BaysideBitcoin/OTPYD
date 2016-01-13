#Description: Contains Class definiton for a PYD 'pad object'
#Author : juju
import csv, subprocess
from datetime import date
from dateutil.rrule import rrule, DAILY
from otpyutil import sha256, randbytes, gettime

#Generates and Holds our pads information
class OTPYD:
    def __init__(self, entropy, hashedentropy):
        self.pyd = []
        self.entropy = entropy
        self.hashedentropy = hashedentropy
        self.dates = []
        self.hexstrs = []
        self.days = 0

    #Pre: Given a range of dates, populates the dates array for creating a pyd
    #Post: Updates list of dates for a given range used when zipping a pyd, also inputs how many days are in the pad
    def generateDates(self, date1, date2):
        a = date1
        b = date2
        self.dates = []
        x=0
        for dt in rrule(DAILY, dtstart=a, until=b):
            x+=1
            date=dt.strftime("%m-%d-%Y")
            self.dates.append(date)
        self.days = x
        
    #Pre: Generates Hex Strings used for shifting messages
    #Post: Updates the list of hexstrs to contain the same number of strings for the given days range
    def generateHexstrs(self):
        #Get the length of the entropy string as an integer if the length is greather than 1024, set it to 1024 subtract it from the last 3 digits of current unix timestamp)
        entlen = len(self.entropy)
        if entlen > 1024:
            entlen = 1024 - int(str(gettime())[-4:-1])

        if self.days !=0:
            for x in range(1,self.days+1):
                row=''
                row+=sha256(randbytes(32+entlen)+self.hashedentropy)
                row+=sha256(self.hashedentropy + randbytes(32+entlen))
                self.hexstrs.append(row)
                
    #Pre: Given number of days for an OTP
    #Post: Re-writes pad to contain OTP with a row for each number of DAY
    def generatePad(self, date1, date2):
        a = date1
        b = date2
        self.generateDates(a, b)
        self.generateHexstrs()
        self.pyd=zip(self.dates, self.hexstrs)

    #Pre: Given we have a pad generated
    #Post: Creates a .csv file with the current pad in it
    def createCSV(self, filename):
        f = open(filename, 'wt')
        writer = csv.writer(f)
        for row in self.pyd:
            writer.writerow((row[0] , row[1]))
        f.close()
    
    def importPad(self, filename):
        self.pyd = []
        datelist=[]
        keylist=[]
        f = open(filename, 'r')
        try:
            reader = csv.reader(f)
            for row in reader:  
                datelist.append(row[0])
                keylist.append(row[1])
            self.pyd=zip(datelist, keylist)
        except:
            f.close()
            return False
        finally:
            f.close()
            return True
    
    def createHTML(self, filename):
        HTML = """
        <html>
            <head>
                <title>OTPY Padfile</title>
              <meta name="viewport" content="width=device-width, initial-scale=1">
              <link rel="stylesheet" href="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css">
              <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
              <script src="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/js/bootstrap.min.js"></script>
            </head>
            <body>
                <div class="container-fluid">
                	<div class="row">
                		<div class="col-md-4">
                		</div>
                		<div class="col-md-4">
                			<div class="row">
                				<div class="col-md-12">
                				<h1>OTPY Padfile</h1>
                                    <table class="table table-striped table-bordered">
                                        <thead>
                                            <tr>
                                                <th>Date</th>
                                                <th>Key</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                """
        for row in self.pyd:
            HTML+="""
                <tr><td>
                """+ row[0] +"""</td>
                <td>"""+ row[1] +"""</td>
                </tr>
                """
        HTML+="""                   </tbody>
                                    </table>
                    	        </div>
                            </div>
                        </div>
                        <div class="col-md-4">
                        </div>
                    </div>
                </div>
            </body>
        </html>
            """
        f = open(filename, 'w')
        try:
            f.write(HTML)
        except:
            f.close()
            return False
        finally:
            f.close()
            return True
    
    #Pre: Given we have a pad generated
    #Post: Tries to print a version of our pad
    def linuxprint(self):
        #Create a file with our current pad, write each row to the file then close it
        f = open('pad.padfile', 'w')
        for row in self.pyd:
            f.write(row[0] + ' : ' + row[1]+'\n')
        f.close
        #Try to print the pad.padfile we generated, wait for it to finish, then try to delete the padfile.
        try:
            lpr =  subprocess.Popen("/usr/bin/lpr pad.padfile")
            lpr.wait()
            delfile = subprocess.Popen("rm pad.padfile")
            delfile.wait()
            return True
        except:
            print 'Failed Sending Padfile to Printer Queue'
            return False
    
    #Pre: Given we have a pad generated
    #Post: Prints out the pad to the console
    def viewPad(self):
        for row in self.pyd:
            print row[0] + ' : ' + row[1]