
from scapy.all import *

def pkt_callback(pkt):
    if TCP in pkt:
        print "TCP pkt"
    elif UDP in pkt:
        print "UDP pkt"

# call without filter to get all packets
sniff(iface="enp0s25", prn=pkt_callback, store=0)
#sniff(iface="enp0s25", prn=pkt_callback, filter="tcp", store=0)

