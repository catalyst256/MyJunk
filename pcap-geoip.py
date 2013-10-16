#!/usr/bin/env python

# by @catalyst256

import pygeoip, sys
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *

# Add some colouring for printing packets later
YELLOW = '\033[93m'
GREEN = '\033[92m'
END = '\033[0m'
RED = '\033[91m'

# Change this to point to your geoip database file
gi = pygeoip.GeoIP('/opt/geoipdb/geoipdb.dat')

if len(sys.argv) != 2:
	print 'Usage is ./pcap-geoip.py <input pcap file>'
	print 'Example - ./pcap-geoip.py sample.pcap'
	sys.exit(1)

pkts = rdpcap(sys.argv[1])

def geoip_locate(pkts):

	ip_raw = []
	# Exclude "local" IP address ranges
	ip_exclusions = ['192.168.', '172.', '10.', '127.']

	for x in pkts:
		if x.haslayer(IP):
			src = x.getlayer(IP).src
			if src != '0.0.0.0':
				if src not in ip_raw:
					ip_raw.append(src)

	for s in ip_raw:
		# Check to see if IP address is "local"
		if ip_exclusions[0] in s or ip_exclusions[1] in s or ip_exclusions[2] in s or ip_exclusions[3] in s:
			print YELLOW +  'Error local Address Found ' + str(s) + END
		else:
			# Lookup the IP addresses and return some values
			rec = gi.record_by_addr(s)
			lng = rec['longitude']
			lat = rec['latitude']
			google_map_url = 'https://maps.google.co.uk/maps?z=20&q=%s,%s' %(lat, lng)
			print GREEN + '[*] IP: ' + s + ', Latitude: ' +str(lat)+ ', Longtitude: ' +str(lng) + ', ' + google_map_url + END

geoip_locate(pkts)
