#!/usr/bin/env python

import os, sys, logging#, subprocess, shlex
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *

# Add some colouring for printing packets later
YELLOW = '\033[93m'
GREEN = '\033[92m'
END = '\033[0m'

if len(sys.argv) != 3:
	print 'Usage: ./pcap-streams.py pcapfile outputfolder'
	print 'Example: ./pcap-streams.py /tmp/test.pcap /tmp/output'
	sys.exit(1)

pcap = sys.argv[1]
folder = sys.argv[2]

tcp_stream_index = []
tcp_stream_file = []
udp_stream_index = []
udp_stream_file = []

devnull = open('/dev/null', 'w')

# Check to see if the folder exists already
if not os.path.exists(folder):
	print YELLOW + '[!] Folder doesnt exist so creating ' + folder + END
	os.makedirs(folder)

# Function to extract TCP streams
def tcp_stream(pcap):
	print GREEN + '[+] Extracting TCP streams' + END
	# Create a list of the tcp streams in the pcap file and save them as an index
	cmd = 'tshark -r ' + pcap + ' -T fields -e tcp.stream'
	p = os.popen(cmd).readlines()
	for x in p:
		if x not in tcp_stream_index:
			tcp_stream_index.append(x)
	# Now we are going to write out all the streams as a pcap file
	try:
		for y in tcp_stream_index:
			y = y.strip('\n')
			dumpfile = folder + '/tcp-stream' + y + '.pcap'
			if 'tcp-stream.pcap' in dumpfile:
				pass
			else:
				cmd = 'tshark -r ' + pcap + ' tcp.stream eq ' + y + ' -w ' + dumpfile
				if dumpfile not in tcp_stream_file:
					tcp_stream_file.append(dumpfile)
				os.popen(cmd)
	except:
		pass

	print YELLOW + '[!] There are ' + str(len(tcp_stream_file)) + ' TCP streams saved in: ' + folder + END

def udp_stream(pcap):
	print GREEN + '[+] Extracting UDP streams' + END
	pkts = rdpcap(pcap)
	for p in pkts:
		s_ip = ''
		d_ip = ''
		s_port = ''
		d_port = ''
		if p.haslayer(IP) and p.haslayer(UDP):
			if p[IP].src is not None:
				s_ip = p[IP].src
			if p[IP].dst is not None:
				d_ip = p[IP].dst
			if p[UDP].sport is not None:
				s_port = p[UDP].sport
			if p[UDP].dport is not None:
				d_port = p[UDP].dport
			convo = s_ip, s_port, d_ip, d_port
			duplicate = d_ip, d_port, s_ip, s_port
			if convo not in udp_stream_index:
				udp_stream_index.append(convo)
			if duplicate in udp_stream_index:
				udp_stream_index.remove(duplicate)
			else:
				pass
		else:
			pass

	counter = -1
	for s_ip, s_port, d_ip, d_port in udp_stream_index:
		counter += 1
		dumpfile = folder + '/udp-stream' + str(counter) + '.pcap'
		cmd = 'tshark -r ' + pcap + ' -R "(ip.addr eq ' + s_ip + ' and ip.addr eq ' + d_ip + ') and (udp.port eq ' + str(s_port) + ' and udp.port eq ' + str(d_port) + ')" -w ' + dumpfile
		if dumpfile not in udp_stream_file:
			udp_stream_file.append(dumpfile)
			os.popen(cmd)
	print YELLOW + '[!] There are ' + str(len(udp_stream_file)) + ' UDP streams saved in: ' + folder + END


tcp_stream(pcap)
udp_stream(pcap)
