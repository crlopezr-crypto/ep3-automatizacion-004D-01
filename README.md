# EP3 — Implementación de Automatización de Red con Compliance Auditado

**Alumno:** Lopez Reinun Cristopher  
**Código:** 004D-01  
**Curso:** DRY7122 — Programación y Redes Virtualizadas  
**Empresa cliente:** LogisticaNorte SA  

---

## 1. Objetivo del proyecto

Se implementó el ciclo completo de aprovisionamiento automatizado de un router Cisco CSR1kv para la empresa LogisticaNorte SA. El objetivo fue incorporar el equipo a la red corporativa aplicando configuración estándar mediante herramientas de automatización, y certificar su compliance mediante validación independiente.

---

## 2. Alcance

Se configuró el hostname corporativo, banner de acceso, servidor NTP, descripción de interfaz WAN e interfaz Loopback de gestión. También se habilitaron los servicios NETCONF, RESTCONF y HTTP seguro. Quedó fuera del alcance la configuración de routing dinámico y políticas de seguridad avanzadas. Las herramientas utilizadas fueron pyATS/Genie, Ansible, ncclient y Python requests.

---

## 3. Infraestructura utilizada

| Componente | Detalle |
|---|---|
| Router | Cisco CSR1kv — IOS-XE 16.9 |
| IP del router | 192.168.160.132 |
| Estación de trabajo | DEVASC VM — Ubuntu (labvm) |
| Herramientas | pyATS/Genie, Ansible, ncclient, Python 3, requests |

---

## 4. Tecnologías empleadas y justificación

- **pyATS/Genie:** Se usó en Fase 1 y Fase 5 para capturar el estado del router vía SSH antes y después del aprovisionamiento, permitiendo comparar cambios de forma estructurada.
- **Ansible:** Se usó en Fase 2 para aplicar la configuración corporativa de forma automatizada e idempotente, garantizando reproducibilidad.
- **NETCONF (ncclient):** Se usó en Fase 3 para validar la configuración aplicada consultando el árbol XML completo del router de forma independiente a Ansible.
- **RESTCONF (requests):** Se usó en Fase 4 para verificar recursos específicos de configuración en formato JSON mediante endpoints HTTP, complementando la validación NETCONF.

---

## 5. Configuración aplicada

| Parámetro | Valor aplicado |
|---|---|
| Hostname | RTR-LOGNORTE |
| IP Loopback10 | 10.4.1.1 / 255.255.255.0 |
| Descripción WAN | Enlace-WAN-Santiago |
| Banner MOTD | ACCESO RESTRINGIDO - LOGNORTE |
| Servidor NTP | 1.1.1.1 |
| NETCONF | Habilitado (puerto 830) |
| RESTCONF | Habilitado |
| HTTP seguro | Habilitado |

---

## 6. Resultados de validación

| Criterio | NETCONF | RESTCONF |
|---|---|---|
| Hostname corporativo | CONFORME | CONFORME |
| IP Loopback | CONFORME | CONFORME |
| Máscara Loopback | CONFORME | — |
| Descripción WAN | CONFORME | CONFORME |
| Servidor NTP | CONFORME | CONFORME |

---

## 7. Conclusiones

El dispositivo RTR-LOGNORTE fue aprovisionado exitosamente y entregado a operaciones cumpliendo todos los parámetros corporativos de LogisticaNorte SA. La validación independiente mediante NETCONF y RESTCONF confirmó que la configuración aplicada por Ansible es correcta y consistente. El diff generado por Genie evidencia los cambios realizados respecto al estado inicial del equipo.
