# Distributed Denial of Services - DDoS 

<p align="center">
<a href="https://www.blackhatethicalhacking.com"><img src="https://pbs.twimg.com/profile_banners/770898848197795840/1650879597/1500x500" width="600px" alt="BHEH"></a>
</p>
<p align="center">
<a href="https://www.blackhatethicalhacking.com"><img src="https://www.blackhatethicalhacking.com/wp-content/uploads/2022/06/BHEH_logo.png" width="300px" alt="BHEH"></a>
</p>

<p align="center">
A Layer 7 DDoS tool written by Black Hat Ethical Hacking
</p>

# What is a DDoS-Attack?

A Distributed Denial of Service (DDoS) attack is an attempt to make an online service unavailable
by overwhelming it with traffic from multiple sources. They target a wide variety of important resources from banks to news websites or any kind of business, and present a major challenge to making sure people can publish and access important information and turning the site down, this way no transactions can be made for the time its being DDoSed.

This can be used also to test specific ports running on specific services, that could be vulnerable to DDoS attacks, especially when you find a valid vulnerable issue that can be exploited by such attacks.


# Installation

`git clone https://github.com/blackhatethicalhacking/DDoS-Layer7-bheh.git`

`cd DDoS-Layer7-bheh`

`chmod +x ddos-bheh-attack.py`

`python3 ddos-bheh-attack.py`


# Instructions

All you have to do when you run this tool is provide it with:

- Target IP
- Target Port
- Time to attack

It will then start sending 1337 packets to that port for the time you gave it.

Note the time is in seconds.

It is recommended to use high bandwidth, such as a VPS Server.


# Screenshots

**Main Menu**

![alt text](https://i.ibb.co/6JnTt3B/Main.png)

**Attack in Progress**

![alt text](https://i.ibb.co/0fGDnNZ/Attack.png)


# Compatibility

Tested on Kali Linux, Parrot OS - Any Debian based that uses apt package manager.


# Updates

We just converted this tool from Python2 to Python3! added some colors, added time to perform the attack as well!


# Disclaimer

This tool is provided for educational and research purpose only. The author of this project are no way responsible for any misuse of this tool. 
We use it to test under NDA agreements with clients and their consents for pentesting purposes and we never encourage to misuse or take responsibility for any damage caused !
