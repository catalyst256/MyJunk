#!/usr/bin/python

# This is a modified version of the CORE Security Technologies pcap splitter code.
# This version supports TCP & UDP stream extraction and a modified file naming convention
# Modified by @catalyst256

# --- Original Licensing stuff ---
# This software is provided under under a slightly modified version
# of the Apache Software License. See the accompanying LICENSE file
# for more information.

# Copyright (c) 2003 CORE Security Technologies
# Original Authors:
# Alejandro D. Weil <aweil@coresecurity.com>
# Javier Kohen <jkohen@coresecurity.com>

# Requires pcapy which can be installed by running the following:
# pip install "http://corelabs.coresecurity.com/index.php?module=Wiki&action=attachment&type=tool&page=Pcapy&file=pcapy-0.10.8.tar.gz"


import sys
import string
from exceptions import Exception
from threading import Thread

import pcapy
from pcapy import open_offline
import impacket
from impacket.ImpactDecoder import EthDecoder, LinuxSLLDecoder


class Connection:
    """This class can be used as a key in a dictionary to select a connection
    given a pair of peers. Two connections are considered the same if both
    peers are equal, despite the order in which they were passed to the
    class constructor.
    """

    def __init__(self, p1, p2, p3):
        """This constructor takes two tuples, one for each peer. The first
        element in each tuple is the IP address as a string, and the
        second is the port as an integer.
        """

        self.p1 = p1
        self.p2 = p2
        self.p3 = p3

    def getFilename(self):
        """Utility function that returns a filename composed by the IP
        addresses and ports of both peers.
        """
        return '%s-%s:%d-%s:%d.pcap' % (self.p1, self.p2[0], self.p2[1], self.p3[0], self.p3[1])

    def __cmp__(self, other):
        if (self.p2 == other.p2 and self.p3 == other.p3) or (self.p2 == other.p3 and self.p3 == other.p2):
            return 0
        else:
            return -1

    def __hash__(self):
        return (hash(self.p2[0]) ^ hash(self.p2[1])
                ^ hash(self.p3[0]) ^ hash(self.p3[1]))


class Decoder:
    def __init__(self, pcapObj):
        # Query the type of the link and instantiate a decoder accordingly.
        datalink = pcapObj.datalink()
        if pcapy.DLT_EN10MB == datalink:
            self.decoder = EthDecoder()
        elif pcapy.DLT_LINUX_SLL == datalink:
            self.decoder = LinuxSLLDecoder()
        else:
            raise Exception("Datalink type not supported: " % datalink)

        self.pcap = pcapObj
        self.connections = {}

    def start(self):
        # Sniff ad infinitum.
        # PacketHandler shall be invoked by pcap for every packet.
        self.pcap.loop(0, self.packetHandler)

    def packetHandler(self, hdr, data):
        # Use the ImpactDecoder to turn the rawpacket into a hierarchy
        # of ImpactPacket instances.
        try:
            p = self.decoder.decode(data)
            ip = p.child()
            protocol = ip.get_ip_p()
            # Build a distinctive key for this pair of peers.
            if protocol == 6:
                tcp = ip.child()
                proto = 'TCP'
                src = (ip.get_ip_src(), tcp.get_th_sport())
                dst = (ip.get_ip_dst(), tcp.get_th_dport())
                con = Connection(proto, src, dst)
            elif protocol == 17:
                udp = ip.child()
                proto = 'UDP'
                src = (ip.get_ip_src(), udp.get_uh_sport())
                dst = (ip.get_ip_dst(), udp.get_uh_dport())
                con = Connection(proto, src, dst)

            # If there isn't an entry associated yetwith this connection,
            # open a new pcapdumper and create an association.
            if not self.connections.has_key(con):
                fn = con.getFilename()
                print "Found a new connection, storing into:", fn
                try:
                    dumper = self.pcap.dump_open(fn)
                except pcapy.PcapError, e:
                    print "Can't write packet to:", fn
                    return
                self.connections[con] = dumper

            # Write the packet to the corresponding file.
            self.connections[con].dump(hdr, data)
        except Exception as e:
            print str(e)
            pass


def main(filename):
    # Open file
    p = open_offline(filename)
    # At the moment the callback only accepts TCP/IP packets.
    p.setfilter(r'ip proto \tcp or \udp')
    print "Reading from %s: linktype=%d" % (filename, p.datalink())
    # Start decoding process.
    Decoder(p).start()


# Process command-line arguments.
if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print "Usage: %s <filename>" % sys.argv[0]
        sys.exit(1)
    main(sys.argv[1])
