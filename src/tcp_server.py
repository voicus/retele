# TCP Server
import socket
import logging
import time
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
sock.bind(server_address)
logging.info("Serverul a pornit pe %s si portnul portul %d", adresa, port)
sock.listen(5)
while True:
    logging.info('Asteptam conexiui...')
    conexiune, address = sock.accept()
    logging.info("Handshake cu %s", address)
    
    while True:
        data = conexiune.recv(1024)
        logging.info('Content primit: "%s"', data)
        time.sleep(2)
        mesaj = get_random_string()
        conexiune.send(mesaj.encode('utf-8'))
    conexiune.close()
sock.close()
