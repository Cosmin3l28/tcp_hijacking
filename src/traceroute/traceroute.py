import socket
import struct
import time
import requests

MAX_HOPS = 30
TIMEOUT = 2.0
DEST_PORT = 33434

def is_private_ip(ip):
    private_prefixes = ('10.', '192.168.', '172.')
    return any(ip.startswith(prefix) for prefix in private_prefixes)

def get_location(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}", timeout=2)
        data = response.json()
        if data["status"] == "success":
            city = data.get("city", "")
            region = data.get("regionName", "")
            country = data.get("country", "")
            return f"{city}, {region}, {country}"
    except:
        pass
    return "Locație necunoscută"

def traceroute(dest_name):
    try:
        dest_addr = socket.gethostbyname(dest_name)
    except socket.gaierror:
        print(f"Nu pot rezolva adresa pentru {dest_name}")
        return

    print(f"Traceroute către {dest_name} ({dest_addr}), maxim {MAX_HOPS} hop-uri:")

    for ttl in range(1, MAX_HOPS + 1):
        recv_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

        recv_socket.settimeout(TIMEOUT)
        recv_socket.bind(("", DEST_PORT))
        send_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)

        start_time = time.time()
        send_socket.sendto(b"", (dest_addr, DEST_PORT))

        curr_addr = None
        try:
            _, curr_addr = recv_socket.recvfrom(512)
            elapsed = (time.time() - start_time) * 1000
            curr_addr = curr_addr[0]
            if is_private_ip(curr_addr):
                location = "(adresă privată)"
            else:
                location = get_location(curr_addr)

            print(f"{ttl:2}  {curr_addr:15}  {elapsed:.2f} ms  →  {location}")
        except socket.timeout:
            print(f"{ttl:2}  *")
        finally:
            recv_socket.close()
            send_socket.close()

        if curr_addr == dest_addr:
            break

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Utilizare: python traceroute.py <destinație>")
    else:
        traceroute(sys.argv[1])
