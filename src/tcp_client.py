# tcp_client.py
import socket
import logging
import time
import random

logging.basicConfig(format='[%(asctime)s] %(message)s', level=logging.INFO)

server_ip = '198.7.0.2'  # IP-ul containerului server
port = 10000

while True:
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((server_ip, port))
        logging.info("Conectat la server")
        break
    except Exception as e:
        logging.warning(f"Conexiune eșuată, retry in 1s... {e}")
        time.sleep(1)

while True:
    mesaj = f"Mesaj random {random.randint(1, 100)}"
    sock.send(mesaj.encode())
    raspuns = sock.recv(1024)
    logging.info(f"Răspuns primit: {raspuns.decode()}")
    time.sleep(2)
