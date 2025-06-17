# tcp_server.py
import socket
import logging
import threading
import time
import random

logging.basicConfig(format='[%(asctime)s] %(message)s', level=logging.INFO)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

ip = '0.0.0.0'  # ascultă pe toate interfețele
port = 10000
sock.bind((ip, port))
sock.listen(5)

logging.info(f"Server pornit pe {ip}:{port}")

def send_loop(connection):
    """Trimite mesaje random către client la fiecare 2 secunde."""
    while True:
        try:
            mesaj = f"Mesaj server {random.randint(100, 999)}"
            connection.send(mesaj.encode())
        except Exception:
            # Dacă s-a închis conexiunea ieșim din thread
            break
        time.sleep(2)


while True:
    conn, addr = sock.accept()
    logging.info(f"Conexiune de la {addr}")

    # Thread pentru trimiterea de mesaje către client
    threading.Thread(target=send_loop, args=(conn,), daemon=True).start()

    while True:
        data = conn.recv(1024)
        if not data:
            break
        logging.info(f"Mesaj primit: {data.decode()}")

    conn.close()
