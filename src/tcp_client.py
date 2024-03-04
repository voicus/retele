# TCP client
import socket
import logging
import time
import sys
import random
import string

def get_random_string():
    return str(''.join(random.choices(string.ascii_lowercase, k=4)))

logging.basicConfig(format = u'[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', level = logging.NOTSET)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=socket.IPPROTO_TCP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

port = 10000
adresa = '198.7.0.2'
server_address = (adresa, port)

try:
    logging.info('Handshake cu %s', str(server_address))
    sock.connect(server_address)
    while True:
        time.sleep(2)
        mesaj = get_random_string()
        sock.send(mesaj.encode('utf-8'))
        data = sock.recv(1024)
        logging.info('Content primit: "%s"', data)
finally:
    logging.info('closing socket')
    sock.close()
