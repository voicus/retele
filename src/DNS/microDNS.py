import socket
from scapy.all import *

simple_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, proto=socket.IPPROTO_UDP)
simple_udp.bind(('0.0.0.0', 53))

blacklist = {}

def parse_blocked_list():
    with open("/elocal/adservers.txt") as f:
        for _ in range(24):
           next(f)
        
        for line in f:
            if len(line.split()) < 2:
                print(line)
            else:
                blacklist[line.split()[1]] = True


parse_blocked_list()

output_file = open("/elocal/blocked.txt", "w")

while True:
    request, adresa_sursa = simple_udp.recvfrom(65535)
    packet = DNS(request)
    dns = packet.getlayer(DNS)
    print (packet.qd.qname.decode('utf-8')[:-1])
    if dns is not None and dns.opcode == 0: # dns QUERY
        print ("got: ")
        print (packet.qd.qname.decode('utf-8')[:-1])
        server = packet.qd.qname.decode('utf-8')[:-1]
        if server in blacklist:
            print(server, file=output_file)
            output_file.flush()
            dns_answer = DNSRR(
                rrname=dns.qd.name,
                ttl=330,
                type="A",
                rclass="IN",
                rdata="0.0.0.0")
        else:
            google_dns_query = IP(dst="8.8.8.8") / UDP(sport=5000, dport=53) / DNS (rd = 1, qd=dns.qd)
            reply = sr1(google_dns_query, verbose=0)
            if reply is None or reply.getlayer(DNS).an is None:
                dns_answer = DNSRR(
                    rrname=dns.qd.name,
                    ttl=330,
                    type="A",
                    rclass="IN",
                    rdata="0.0.0.0")
            else:
                dns_answer = reply.getlayer(DNS).an[0]
        dns_response = DNS(
                          id = packet[DNS].id, # DNS replies must have the same ID as requests
                          qr = 1,              # 1 for response, 0 for query 
                          aa = 0,              # Authoritative Answer
                          rcode = 0,           # 0, nicio eroare http://www.networksorcery.com/enp/protocol/dns.htm#Rcode,%20Return%20code
                          qd = packet.qd,      # request-ul original
                          an = dns_answer)     # obiectul de reply
        print('response:')
        print (dns_response.summary())
        simple_udp.sendto(bytes(dns_response), adresa_sursa)
        
simple_udp.close()
output_file.close()
