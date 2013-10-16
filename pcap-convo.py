#!/usr/bin/env python

# by @catalyst256

# Code is in the Scapy conversations function, 
# however doesn't seem to like outputting to file so added it into new file

import pygraph, os, sys, logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *

if len(sys.argv) != 3:
	print 'Usage is ./pcap-convo.py pcapfile outputfile'
	print 'Example - ./pcap-convo.py sample.pcap output.jpg'
	sys.exit(1)

# Add some colouring for printing packets later
YELLOW = '\033[93m'
GREEN = '\033[92m'
END = '\033[0m'
RED = '\033[91m'

# Welcome message
print GREEN + '[!] Scapy based pcap to convo script by @catalyst256' + END

pkts = rdpcap(sys.argv[1])
o_type = 'jpg'
target = sys.argv[2]
getsrc = lambda x:x.getlayer(IP).src
getdst = lambda x:x.getlayer(IP).dst

def write_convo(pkts):
	print YELLOW + '[-] Starting the creation process.. (fingers crossed)' + END
	conv = {}
	for p in pkts:
		try:
			c = (getsrc(p), getdst(p))
		except:
			continue
		conv[c] = conv.get(c,0)+1

	gr = 'digraph "conv" {\n'
	for s,d in conv:
		gr += '\t "%s" -> "%s"\n' % (s,d)
	gr += "}\n"

	w,r = os.popen2("dot -T%s -o%s" % (o_type, target))
	w.write(gr)
	w.close
	print GREEN + "[!] File written to " + target + END

write_convo(pkts)

