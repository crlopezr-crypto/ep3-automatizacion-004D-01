#!/usr/bin/env python3
import os
import datetime
import yaml

# Cargar variables
vars_path = "/home/devasc/ep3-automatizacion-004D-01/vars/vars-004D-01.yaml"
with open(vars_path) as f:
    v = yaml.safe_load(f)

alumno   = v["alumno"]["codigo"]
nombre   = v["alumno"]["nombre"]
empresa  = v["cliente"]["empresa"]
hostname = v["cliente"]["hostname"]

# Leer output NETCONF
netconf_path = "/home/devasc/ep3-automatizacion-004D-01/fase3_validacion_netconf/evidencias/output_validacion_netconf.txt"
with open(netconf_path) as f:
    netconf_txt = f.read()
netconf_ok = "RESULTADO: CONFORME" in netconf_txt

# Leer output RESTCONF
restconf_path = "/home/devasc/ep3-automatizacion-004D-01/fase4_validacion_restconf/evidencias/output_validacion_restconf.txt"
with open(restconf_path) as f:
    restconf_txt = f.read()
restconf_ok = "RESULTADO: CONFORME" in restconf_txt

# Leer diff
diff_dir = "/home/devasc/ep3-automatizacion-004D-01/fase5_reporte/evidencias/diff_004D-01"
diff_files = os.listdir(diff_dir) if os.path.exists(diff_dir) else []
diff_ok = len(diff_files) > 0

# Resultado global
compliance = netconf_ok and restconf_ok and diff_ok

# Generar certificado
cert_path = "/home/devasc/ep3-automatizacion-004D-01/fase5_reporte/evidencias/certificado_compliance_004D-01.txt"

contenido = f"""
==============================================================
     CERTIFICADO DE COMPLIANCE — IMPLEMENTACION DE RED
==============================================================

Alumno          : {nombre}
Codigo          : {alumno}
Empresa cliente : {empresa}
Hostname router : {hostname}
Fecha           : {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

--------------------------------------------------------------
RESULTADO DE VALIDACIONES
--------------------------------------------------------------

Validacion NETCONF  : {"CONFORME" if netconf_ok  else "NO CONFORME"}
Validacion RESTCONF : {"CONFORME" if restconf_ok else "NO CONFORME"}
Diff baseline/final : {"DETECTADO" if diff_ok    else "SIN CAMBIOS"}

--------------------------------------------------------------
RESULTADO GLOBAL DE COMPLIANCE
--------------------------------------------------------------

{"CONFORME — El equipo cumple con todos los parametros corporativos" if compliance else "NO CONFORME — Revisar validaciones fallidas"}

El dispositivo {hostname} ha sido aprovisionado exitosamente
y esta listo para operar en la red de {empresa}.

==============================================================
"""

with open(cert_path, "w") as f:
    f.write(contenido)

print(contenido)
print(f"Certificado guardado en: {cert_path}")