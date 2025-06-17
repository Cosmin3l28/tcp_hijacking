import folium
import requests
import re

# Calea către fișierul .txt generat de traceroute
fisier_input = "traceroute_baidu.txt"

# Funcție pentru a verifica dacă IP-ul este privat
def is_private_ip(ip):
    return (
        ip.startswith("10.") or
        ip.startswith("192.168.") or
        ip.startswith("172.")
    )

# Citim IP-urile din fișier
ipuri_publice = []
with open(fisier_input, "r") as f:
    for linie in f:
        match = re.search(r"(\d{1,3}(?:\.\d{1,3}){3})", linie)
        if match:
            ip = match.group(1)
            if not is_private_ip(ip) and ip not in ipuri_publice:
                ipuri_publice.append(ip)

# Cerem locația pentru fiecare IP public
puncte = []
for ip in ipuri_publice:
    try:
        r = requests.get(f"http://ip-api.com/json/{ip}", timeout=3)
        data = r.json()
        if data["status"] == "success":
            lat = data["lat"]
            lon = data["lon"]
            label = f"{ip} - {data.get('city', '')}, {data.get('regionName', '')}, {data.get('country', '')}"
            puncte.append((lat, lon, label))
    except:
        pass

# Verificăm dacă avem puncte
if not puncte:
    print("Nu s-au găsit IP-uri publice valide pentru hartă.")
    exit()

# Creăm harta centrată pe primul punct
harta = folium.Map(location=[puncte[0][0], puncte[0][1]], zoom_start=3)

# Adăugăm punctele și legăturile
for lat, lon, label in puncte:
    folium.Marker([lat, lon], popup=label).add_to(harta)

folium.PolyLine([(lat, lon) for lat, lon, _ in puncte], color="blue").add_to(harta)

# Salvăm harta
harta.save("harta_baidu.html")
print("✅ Harta a fost generată: harta_baidu.html")
