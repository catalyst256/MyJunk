#!/usr/bin/env python

# Scapy heartbleed pcap searcher...
# by catalyst256@gmail.com

import re
import sys
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *


# Add some colouring for printing packets later
GREEN = '\033[92m'
END = '\033[0m'#!/usr/bin/env python

# Scapy heartbleed pcap searcher...
# by catalyst256@gmail.com

import re
import sys
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *


# Add some colouring for printing packets later
GREEN = '\033[92m'
END = '\033[0m'
RED = '\033[91m'
YELLOW = '\033[93m'

def find_heartbleed(pkts):
  for p in pkts:
    if p.haslayer(TCP) and p.haslayer(Raw):
      # Find the heartbleed requests & responses
      # if p[TCP].sport or p[TCP].dport == 443:
      x = p[Raw].load
      x = hexstr(x)
      x = x.split(' ')
      try:
        if x[0] == '18':
          hb_type = ''
          tls_version = ''.join(x[1:3])
          length = ''.join(x[3:5])
          payload = ''
          if length == '0003':
            hb_type = GREEN + '[!] Heartbleed Request: ' + END
          elif length == '4000':
            hb_type = RED + '[!] Heartbleed Response: ' + END
            payload = ''.join(x[10:])
          if hb_type is not '':
            print hb_type + 'src: ' + p[IP].src + ' dst: ' + p[IP].dst
        else:
          pass
      except Exception, e:
        print e

if __name__ == "__main__":
  
  if len(sys.argv) != 2:
    print 'Usage is ./pcap-heartbleed.py <input pcap file>'
    print 'Example - ./pcap-heartbleed.py sample.pcap'
    sys.exit(1)

  pcap = sys.argv[1]
  print GREEN + '[+] Loading pcap file.. ' + str(pcap) + END
  pkts = rdpcap(pcap)
  print YELLOW + '[-] Number of packets %d' %(len(pkts)) + END
  find_heartbleed(pkts)
  print GREEN + '[-] Scanning complete...Have a nice day!!' + END
RED = '\033[91m'


def find_heartbleed(pkts):
  for p in pkts:
    if p.haslayer(TCP) and p.haslayer(Raw):
      # Find the heartbleed requests & responses
      if p[TCP].sport or p[TCP].dport == 443:
        x = p[Raw].load
        x = hexstr(x)
        x = x.split(' ')
        try:
          if x[0] == '18':
            hb_type = ''
            tls_version = ''.join(x[1:3])
            length = ''.join(x[3:5])
            payload = ''
            if length == '0003':
              hb_type = GREEN + 'Heartbleed Request: ' + END
            elif length == '4000':
              hb_type = RED + 'Heartbleed Response: ' + END
              payload = ''.join(x[10:])
            print hb_type + 'src: ' + p[IP].src + ' dst: ' + p[IP].dst
          else:
            pass
        except Exception, e:
          print e

if __name__ == "__main__":
  
  if len(sys.argv) != 2:
    print 'Usage is ./pcap-heartbleed.py <input pcap file>'
    print 'Example - ./pcap-heartbleed.py sample.pcap'
    sys.exit(1)

  pcap = sys.argv[1]
  pkts = rdpcap(pcap)
  find_heartbleed(pkts)
