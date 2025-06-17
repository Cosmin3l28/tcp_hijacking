# tcp_server.py
import socket
import logging

logging.basicConfig(format='[%(asctime)s] %(message)s', level=logging.INFO)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

ip = '0.0.0.0'  # ascultă pe toate interfețele
port = 10000
sock.bind((ip, port))
sock.listen(5)

logging.info(f"Server pornit pe {ip}:{port}")

while True:
    conn, addr = sock.accept()
    logging.info(f"Conexiune de la {addr}")
    while True:
        data = conn.recv(1024)
        if not data:
            break
        logging.info(f"Mesaj primit: {data.decode()}")
        reply = f"Serverul a primit: {data.decode()}"
        conn.send(reply.encode())
    conn.close()
