# Distributed Denial of Services - DDoS 



<p align="center">
<a href="https://www.blackhatethicalhacking.com"><img src="https://www.blackhatethicalhacking.com/wp-content/uploads/2022/06/BHEH_logo.png" width="300px" alt="BHEH"></a>
</p>

<p align="center">
An Advanced Layer 7 DDoS tool written by Black Hat Ethical Hacking
</p>

# Description

**DDoSlayer** is an Offensive Security Tool written in Python3 by Chris 'SaintDruG' Abou-Chabke from Black Hat Ethical Hacking, designed to perform **Distributed Denial of Service (DDoS)** attacks.

### **Focus on Layer 7 Attacks**

The focus of the tool is on **layer 7 attacks**, which are known to be the most advanced types of DDoS attacks. The tool offers the user a choice between three different DDoS attack methods: 

- UDP Flood
- SYN Flood
- HTTP Flood

### **What is DDoS?**

DDoS is an abbreviation for **Distributed Denial of Service**, a type of attack aimed at disrupting the availability of a targeted website, network, or service. This attack is typically carried out by overwhelming the target with a large amount of traffic from multiple sources. In the context of red teaming and pentesting, DDoS attacks are simulated to evaluate the ability of the blue team to withstand such sophisticated attacks.

### **Optimized for Speed and Efficiency**

"DDoSlayer" is optimized for speed and efficiency, making it a great choice for those looking to execute DDoS attacks in a timely and effective manner. The tool provides real-time feedback on the number of packets sent during the attack, enabling the user to monitor its progress.

### **User-Friendly and Easy to Use**

Moreover, the tool is designed with ease of use in mind, allowing even novice users to carry out advanced DDoS attacks with ease.


# New Features in Version: 2.0

• Focus on Layer 7 attacks: The tool is re-designed to specifically target the most sophisticated types of DDoS attacks, known as layer 7 attacks.

• Multiple attack types: The tool offers three different types of DDoS attacks: UDP Flood, SYN Flood, and HTTP Flood, giving the user flexibility in their choice of attack.

• Optimized for speed: DDoSlayer is designed to perform attacks quickly and efficiently, making it an ideal choice for those looking to disrupt the target as quickly as possible.

• Real-time feedback: The tool provides real-time feedback on the number of packets sent during the attack, allowing the user to monitor the progress of the attack.

• User-friendly: The tool is designed to be user-friendly, with a simple and intuitive interface, allowing even inexperienced users to perform sophisticated DDoS attacks with ease.


# Installation

`git clone https://github.com/blackhatethicalhacking/DDoSlayer.git`

`cd DDoSlayer`

`chmod +x DDoSlayer.py`

`python3 DDoSlayer.py`


# Instructions

All you have to do when you run this tool is provide it with:

- Target IP
- Target Port
- Duration to attack

It will then start sending 1337 packets to that port for the time you gave it.

Note, the time is in seconds.

It is recommended to use high bandwidth, such as a VPS Server.


# Screenshots

**Main Menu**

![DDoSlayer](https://github.com/blackhatethicalhacking/DDoSlayer/assets/13942386/991d82f4-b497-4783-8bc1-2b72fff513f5)

# Compatibility

Tested on Kali Linux, Parrot OS & MacOS


# Updates

V2.0

Added 3 attack options to choose from
Error Handlings
Optimizations
Check Features!

V1.2

We just converted this tool from Python2 to Python3! added some colors, added time to perform the attack as well!


# Disclaimer

This tool is provided for educational and research purpose only. The author of this project are no way responsible for any misuse of this tool. 
We use it to test under NDA agreements with clients and their consents for pentesting purposes and we never encourage to misuse or take responsibility for any damage caused !

# Support

If you would like to support us, you can always buy us coffee(s)! :blush:

<a href="https://www.buymeacoffee.com/bheh" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a>
