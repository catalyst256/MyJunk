#!/usr/bin/env python
import logging, sys
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *

interface = 'mon0'

# Add some colouring for printing packets later
GREEN = '\033[92m'
END = '\033[0m'

def sniffBeacons(p):
	if p.haslayer(Dot11Beacon):
		enc = ''
		ssid = p[Dot11Elt].info
		bssid = p[Dot11].addr3
		channel = int(ord(p[Dot11Elt:3].info))
		capability = p.sprintf("{Dot11Beacon:%Dot11Beacon.cap%}{Dot11ProbeResp:%Dot11ProbeResp.cap%}")
		rssi = (ord(p.notdecoded[-4:-3])-256)
		if re.search("privacy", capability): 
			enc = 'Y'
		else:
			enc = 'N'
		entity = ssid, bssid, channel, enc, rssi, interface
		print GREEN + 'SSID: ' + str(entity[0]) + ' BSSID: ' + str(entity[1]) + ' Channel: ' + str(entity[2]) + ' Encryption: ' + str(entity[3]) + ' RSSI: ' + str(entity[4]) + ' via Interface ' + str(entity[5]) + END
			
sniff(iface=interface, prn=sniffBeacons)

