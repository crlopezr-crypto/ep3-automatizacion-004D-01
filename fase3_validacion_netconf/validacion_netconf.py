#!/usr/bin/env python3
import sys
import os
import datetime
import yaml
from ncclient import manager
from lxml import etree

# Metadatos
print("=" * 60)
print("Script  : validacion_netconf.py")
print(f"Fecha   : {datetime.datetime.now()}")
print(f"Host VM : {os.uname().nodename}")
print("=" * 60)

# Cargar variables
vars_path = "/home/devasc/ep3-automatizacion-004D-01/vars/vars-004D-01.yaml"
with open(vars_path) as f:
    v = yaml.safe_load(f)

router_ip     = v["router"]["ip"]
usuario       = v["router"]["usuario"]
password      = v["router"]["password"]
exp_hostname  = v["cliente"]["hostname"]
exp_loopback  = v["router"]["loopback_ip"]
exp_mask      = v["router"]["loopback_mask"]
exp_wan       = v["router"]["descripcion_wan"]
exp_ntp       = v["router"]["ntp_server"]

# Filtro XML
filtro = """
<filter>
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
  </native>
</filter>
"""

# Conectar via NETCONF
print("\nConectando via NETCONF...")
with manager.connect(
    host=router_ip,
    port=830,
    username=usuario,
    password=password,
    hostkey_verify=False,
    allow_agent=False,
    look_for_keys=False
) as m:
    reply = m.get_config(source="running", filter=filtro)
    xml_raw = reply.xml

# Guardar XML crudo
output_dir = "/home/devasc/ep3-automatizacion-004D-01/fase3_validacion_netconf/evidencias"
os.makedirs(output_dir, exist_ok=True)
xml_path = os.path.join(output_dir, "rpc_reply_raw.xml")
with open(xml_path, "w") as f:
    f.write(xml_raw)
print(f"XML guardado en: {xml_path}")

# Parsear XML
root = etree.fromstring(xml_raw.encode())
ns = {
    "nc": "urn:ietf:params:xml:ns:netconf:base:1.0",
    "ios": "http://cisco.com/ns/yang/Cisco-IOS-XE-native",
    "ios-if": "http://cisco.com/ns/yang/Cisco-IOS-XE-native",
}

def get_text(root, xpath):
    try:
        result = root.xpath(xpath, namespaces=ns)
        return result[0].text.strip() if result and result[0].text else ""
    except:
        return ""

# Extraer valores
got_hostname = get_text(root, "//ios:native/ios:hostname")
got_loopback = get_text(root, "//ios:native/ios:interface/ios:Loopback/ios:ip/ios:address/ios:primary/ios:address")
got_mask     = get_text(root, "//ios:native/ios:interface/ios:Loopback/ios:ip/ios:address/ios:primary/ios:mask")
got_wan      = get_text(root, "//ios:native/ios:interface/ios:GigabitEthernet/ios:description")
ntp_results = root.xpath("//*[local-name()='ip-address']", namespaces=ns)
got_ntp = ntp_results[0].text.strip() if ntp_results else ""
# Comparar
print("\n--- REPORTE DE VALIDACION NETCONF ---")
resultados = []

def verificar(criterio, esperado, obtenido):
    ok = esperado.strip() == obtenido.strip()
    estado = "[OK]" if ok else "[FAIL]"
    print(f"{estado} {criterio}")
    print(f"      Esperado : {esperado}")
    print(f"      Obtenido : {obtenido}")
    resultados.append(ok)

verificar("Hostname corporativo", exp_hostname, got_hostname)
verificar("IP Loopback",          exp_loopback, got_loopback)
verificar("Mascara Loopback",     exp_mask,     got_mask)
verificar("Descripcion WAN",      exp_wan,      got_wan)
verificar("Servidor NTP",         exp_ntp,      got_ntp)

print("\n--- RESULTADO GLOBAL ---")
if all(resultados):
    print("RESULTADO: CONFORME")
else:
    total = sum(resultados)
    print(f"RESULTADO: NO CONFORME ({total}/5 criterios OK)")