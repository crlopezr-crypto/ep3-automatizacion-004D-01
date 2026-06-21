# EP3 — Implementación de Automatización de Red con Compliance Auditado

**Alumno:** Lopez Reinun Cristopher  
**Código:** 004D-01  
**Curso:** DRY7122 — Programación y Redes Virtualizadas  
**Empresa cliente:** LogisticaNorte SA  
**Repositorio:** ep3-automatizacion-004D-01  

---

## 1. Objetivo del proyecto

Se implementó el ciclo completo de aprovisionamiento automatizado de un router Cisco CSR1kv para la empresa LogisticaNorte SA. El objetivo fue incorporar el equipo a la red corporativa aplicando la configuración estándar definida por la empresa mediante herramientas de automatización, y certificar el cumplimiento de dicha configuración mediante validación independiente usando protocolos de gestión de red (NETCONF y RESTCONF). El resultado final es un equipo documentado, auditado y listo para operar en producción.

---

## 2. Alcance

**Dentro del alcance:**
- Documentación del estado inicial del router antes de cualquier cambio (baseline)
- Habilitación de servicios de automatización: NETCONF, RESTCONF y HTTP seguro
- Aplicación de configuración corporativa: hostname, banner, NTP, descripción WAN e interfaz Loopback de gestión
- Validación independiente de la configuración mediante NETCONF (ncclient) y RESTCONF (requests)
- Generación de reporte de compliance comparando estado inicial vs estado final
- Registro auditado de toda la actividad en repositorio GitHub con historial de commits

**Fuera del alcance:**
- Configuración de protocolos de routing dinámico (OSPF, BGP, EIGRP)
- Implementación de políticas de seguridad avanzadas (ACLs, ZBF, AAA)
- Configuración de VLANs o interfaces adicionales más allá de la Loopback de gestión
- Integración con sistemas de monitoreo externos

---

## 3. Infraestructura utilizada

| Componente | Detalle |
|---|---|
| Router | Cisco CSR1kv — IOS-XE 16.9 |
| IP del router | 192.168.160.132 |
| Puerto NETCONF | 830 |
| Estación de trabajo | DEVASC VM — Ubuntu Linux (hostname: labvm) |
| Sistema operativo VM | Ubuntu 20.04 LTS |
| Python | 3.x |
| Ansible | 2.x con colección cisco.ios |
| pyATS / Genie | Última versión disponible en DEVASC |
| ncclient | Librería Python para NETCONF |
| requests | Librería Python para RESTCONF/HTTP |

---

## 4. Tecnologías empleadas y justificación

**pyATS / Genie:** Utilizado en Fase 1 y Fase 5 para capturar el estado del router antes y después del aprovisionamiento. Se eligió porque permite conectarse vía SSH sin requerir NETCONF habilitado previamente, lo que lo hace ideal para documentar el estado inicial. Genie genera archivos JSON estructurados que permiten comparación automatizada mediante `genie diff`.

**Ansible:** Utilizado en Fase 2 para aplicar la configuración corporativa de forma automatizada e idempotente. Se eligió porque permite definir el estado deseado del dispositivo en un playbook declarativo, garantizando que múltiples ejecuciones produzcan el mismo resultado sin errores. El uso de `vars_files` asegura que los valores del cliente estén centralizados y no hardcodeados.

**NETCONF (ncclient):** Utilizado en Fase 3 para validación independiente. Se eligió porque opera sobre el modelo de datos YANG del dispositivo, devolviendo el árbol de configuración completo en XML, lo que permite verificar con precisión cada parámetro aplicado sin depender de la interpretación de texto plano.

**RESTCONF (Python requests):** Utilizado en Fase 4 como segunda validación independiente. Se eligió porque permite consultar recursos específicos de configuración mediante URLs HTTP y obtener respuestas en formato JSON, complementando la validación NETCONF con un protocolo más ligero y granular.

---

## 5. Configuración aplicada

| Parámetro | Valor aplicado | Comando IOS-XE |
|---|---|---|
| Hostname | RTR-LOGNORTE | `hostname RTR-LOGNORTE` |
| IP Loopback10 | 10.4.1.1 / 255.255.255.0 | `ip address 10.4.1.1 255.255.255.0` |
| Descripción WAN | Enlace-WAN-Santiago | `description Enlace-WAN-Santiago` |
| Banner MOTD | ACCESO RESTRINGIDO - LOGNORTE | `banner motd` |
| Servidor NTP | 1.1.1.1 | `ntp server 1.1.1.1` |
| NETCONF | Habilitado (puerto 830) | `netconf-yang` |
| RESTCONF | Habilitado | `restconf` |
| HTTP seguro | Habilitado | `ip http secure-server` |

---

## 6. Resultados de validación

### NETCONF (5 criterios)

| Criterio | Esperado | Obtenido | Resultado |
|---|---|---|---|
| Hostname corporativo | RTR-LOGNORTE | RTR-LOGNORTE | CONFORME |
| IP Loopback | 10.4.1.1 | 10.4.1.1 | CONFORME |
| Máscara Loopback | 255.255.255.0 | 255.255.255.0 | CONFORME |
| Descripción WAN | Enlace-WAN-Santiago | Enlace-WAN-Santiago | CONFORME |
| Servidor NTP | 1.1.1.1 | 1.1.1.1 | CONFORME |

### RESTCONF (4 criterios)

| Criterio | Esperado | Obtenido | Resultado |
|---|---|---|---|
| Hostname corporativo | RTR-LOGNORTE | RTR-LOGNORTE | CONFORME |
| IP Loopback | 10.4.1.1 | 10.4.1.1 | CONFORME |
| Descripción WAN | Enlace-WAN-Santiago | Enlace-WAN-Santiago | CONFORME |
| Servidor NTP | 1.1.1.1 | 1.1.1.1 | CONFORME |

---

## 7. Conclusiones

El dispositivo RTR-LOGNORTE fue aprovisionado exitosamente y entregado a operaciones cumpliendo el 100% de los parámetros corporativos definidos por LogisticaNorte SA. La validación independiente mediante NETCONF confirmó 5/5 criterios CONFORME, y la validación mediante RESTCONF confirmó 4/4 criterios CONFORME.

El diff generado por Genie entre el baseline inicial y el snapshot final evidencia de forma objetiva los cambios realizados durante el aprovisionamiento, incluyendo el cambio de hostname de CSR1kv a RTR-LOGNORTE y la adición de interfaces y servicios de gestión.

El proceso fue completamente automatizado y auditado: cada fase quedó registrada en el repositorio GitHub con commits fechados, permitiendo trazabilidad completa de qué se hizo, cuándo y cómo. El playbook de Ansible demostró ser idempotente, ejecutándose dos veces con resultado consistente.
