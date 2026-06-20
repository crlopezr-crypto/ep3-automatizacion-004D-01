#!/usr/bin/env python3
import requests
import json
import os
import datetime
import yaml

# Deshabilitar warnings SSL
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Metadatos
print("=" * 60)
print("Script  : validacion_restconf.py")
print(f"Fecha   : {datetime.datetime.now()}")
print(f"Host VM : {os.uname().nodename}")
print("=" * 60)

# Cargar variables
vars_path = "/home/devasc/ep3-automatizacion-004D-01/vars/vars-004D-01.yaml"
with open(vars_path) as f:
    v = yaml.safe_load(f)

router_ip    = v["router"]["ip"]
usuario      = v["router"]["usuario"]
password     = v["router"]["password"]
exp_hostname = v["cliente"]["hostname"]
exp_loopback = v["router"]["loopback_ip"]
exp_wan      = v["router"]["descripcion_wan"]
exp_ntp      = v["router"]["ntp_server"]
loopback_id  = v["router"]["loopback_id"]

base_url = f"https://{router_ip}/restconf/data"
headers  = {"Accept": "application/yang-data+json"}
auth     = (usuario, password)

output_dir = "/home/devasc/ep3-automatizacion-004D-01/fase4_validacion_restconf/evidencias/responses"
os.makedirs(output_dir, exist_ok=True)

def consultar(endpoint, archivo):
    url = f"{base_url}/{endpoint}"
    r = requests.get(url, headers=headers, auth=auth, verify=False)
    data = r.json()
    path = os.path.join(output_dir, archivo)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Guardado: {archivo}")
    return data

# Consultas
print("\nEjecutando consultas RESTCONF...")
data_hostname   = consultar("Cisco-IOS-XE-native:native/hostname", "get_hostname.json")
data_loopback   = consultar(f"ietf-interfaces:interfaces/interface=Loopback{loopback_id}", "get_loopback.json")
data_interfaces = consultar("ietf-interfaces:interfaces/interface=GigabitEthernet1", "get_interfaces.json")
data_ntp        = consultar("Cisco-IOS-XE-native:native/ntp", "get_ntp.json")

# Extraer valores
got_hostname = data_hostname.get("Cisco-IOS-XE-native:hostname", "")

try:
    iface = data_loopback.get("ietf-interfaces:interface", {})
    addrs = iface.get("ietf-ip:ipv4", {}).get("address", [])
    got_loopback = addrs[0].get("ip", "") if addrs else ""
except:
    got_loopback = ""

try:
    iface_wan = data_interfaces.get("ietf-interfaces:interface", {})
    got_wan = iface_wan.get("description", "")
except:
    got_wan = ""

try:
    ntp_servers = data_ntp.get("Cisco-IOS-XE-native:ntp", {}) \
                          .get("Cisco-IOS-XE-ntp:server", {}) \
                          .get("server-list", [])
    got_ntp = ntp_servers[0].get("ip-address", "") if ntp_servers else ""
except:
    got_ntp = ""

# Comparar
print("\n--- REPORTE DE VALIDACION RESTCONF ---")
resultados = []

def verificar(criterio, esperado, obtenido):
    ok = str(esperado).strip() == str(obtenido).strip()
    estado = "[OK]" if ok else "[FAIL]"
    print(f"{estado} {criterio}")
    print(f"      Esperado : {esperado}")
    print(f"      Obtenido : {obtenido}")
    resultados.append(ok)

verificar("Hostname corporativo", exp_hostname, got_hostname)
verificar("IP Loopback",          exp_loopback, got_loopback)
verificar("Descripcion WAN",      exp_wan,      got_wan)
verificar("Servidor NTP",         exp_ntp,      got_ntp)

print("\n--- RESULTADO GLOBAL ---")
if all(resultados):
    print("RESULTADO: CONFORME")
else:
    total = sum(resultados)
    print(f"RESULTADO: NO CONFORME ({total}/4 criterios OK)")