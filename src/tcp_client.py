# tcp_client.py
import socket
import logging
import time
import random
import threading

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


def send_loop(connection):
    """Trimite mesaje random către server la fiecare 2 secunde."""
    while True:
        try:
            mesaj = f"Mesaj client {random.randint(1, 100)}"
            connection.send(mesaj.encode())
        except Exception:
            break
        time.sleep(2)


def recv_loop(connection):
    """Primește mesaje de la server și le afișează."""
    while True:
        data = connection.recv(1024)
        if not data:
            break
        logging.info(f"Răspuns primit: {data.decode()}")


send_thread = threading.Thread(target=send_loop, args=(sock,), daemon=True)
recv_thread = threading.Thread(target=recv_loop, args=(sock,), daemon=True)
send_thread.start()
recv_thread.start()

send_thread.join()
recv_thread.join()
