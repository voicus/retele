import socket
import traceback
import requests
import geopandas as gpd
import matplotlib.pyplot as plt
from scapy.all import IP, ICMP


MAX_TTL = 32
TOKEN = "767c65cee1dd5b"

udp_send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, proto=socket.IPPROTO_UDP)
icmp_recv_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
icmp_recv_socket.settimeout(3)

def plot_data(x, y):
    world = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
    world.plot(color="blue")
    plt.plot(x, y, '-x', color="red")
    plt.show()

def traceroute(ip, port=33434):
    print(ip)
    x = []
    y = []
    for ttl in range(1, MAX_TTL):
        udp_send_sock.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, ttl)
        udp_send_sock.sendto(b'salut', (ip, port))

        addr = 'done!'
        try:
            data, addr = icmp_recv_socket.recvfrom(63535)
            packet = IP(data)
            if ICMP in packet:
                icmp_layer = packet[ICMP]
                if icmp_layer.type == 11 and icmp_layer.code == 0:
                    location = requests.get(f"https://ipinfo.io/{addr[0]}?token={TOKEN}").json()
                    if "bogon" in location:
                        print(f"{ttl}. {addr[0]} bogon ip")
                        continue
                    city = location["city"] if "city" in location else None
                    region = location["region"] if "region" in location else None
                    country = location["country"] if "country" in location else None
                    hostname = location["hostname"] if "hostname" in location else None
                    if "loc" in location:
                        a,b = map(float, location["loc"].split(","))
                        x.append(a)
                        y.append(b)
                    print(f"{ttl}. {addr[0]}: Name: {hostname} City: {city} Region: {region} Country: {country}")
                    if addr[0] == ip:
                        break
        except Exception as e:
            print("Socket timeout ", str(e)) 
    plot_data(y, x)


def checkIP(address):
    try:
        ip = socket.gethostbyname(address)
        return ip
    except Exception as e:
        return None

ip = checkIP(input())
if ip is not None:
    traceroute(ip)
else:
    print("Invalid input!")
