#!/usr/bin/env python

# index Netflow into Splunk (part of Malunk)

import subprocess
import socket

# Add some colouring for printing packets later
YELLOW = '\033[93m'
GREEN = '\033[92m'
END = '\033[0m'
RED = '\033[91m'


def splunk_shot_tcp(s):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('localhost', 9999))
        i = ', '.join("%s=%r" % (key, val) for (key, val) in s.iteritems())
        i = i.replace('\'', '\"')
        # i = re.sub('\w*.\w*.\w*\[\d*\]={', ', ', i)
        # i = re.sub('\w{1,}={', '', i)
        # i = i.replace('{', '').replace('}','').replace('\'', '').replace(': ', '=').replace(' , ', ' ')
        sock.send(i)
    except Exception, e:
        print RED + 'Splunk Import: ' + str(e) + END
    # sock.close()


def parse_netflow(flow):
    try:
        nfdump = '/usr/local/bin/nfdump'.strip('\'')
        real_flows = []
        flows = subprocess.check_output([nfdump, '-r', flow])
        f = flows.split('\n')
        c = len(f) - 5
        f = f[1:c]
        for i in f:
            i = i.split(' ')
            a = [x for x in i if x != '']
            real_flows.append(a)
        return real_flows
    except Exception as e:
        print RED + 'Netflow: ' + str(e) + END


def main():
    nfile = '/Users/Adam/Coding/nfdump-files/nfcapd.201409100910'
    n = parse_netflow(nfile)
    try:
        for i in n:
            src = i[4].split(':')
            dst = i[6].split(':')
            timestamp = ' '.join(i[0:2])
            if '->' in i[5]:
                i[5] = 'outbound'
            if '<-' in i[5]:
                i[5] = 'inbound'
            data = {'file': nfile,  'timestamp': timestamp, 'duration': i[2], 'protocol': i[3],
                    'source_ip': src[0], 'source_port': src[1],  'direction': i[5], 'destination_ip': dst[0],
                    'destination_port': dst[1], 'packets': i[7], 'bytes': i[8], 'flows': i[9]}
            splunk_shot_tcp(data)
    except Exception as e:
        print RED + str(e) + END


if __name__ == '__main__':
    main()