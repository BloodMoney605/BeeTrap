# BeeTrap

WiFi honeypot y evil twin proxy para auditoria de seguridad.
Crea puntos de acceso falsos, suplanta paginas de login de servicios conocidos
y captura credenciales en entornos de prueba controlados.

> Solo para uso educativo y auditorias con autorizacion explicita.
> El uso indebido es responsabilidad del usuario.

## Funcionalidades

- Punto de acceso WiFi con hostapd (modo AP, WMM, 802.11g/n)
- Resuelve todo el DNS a la IP del honeypot con dnsmasq
- Captive portal funcional en Android, iOS, Windows y Firefox
- Paginas de login falsas para 7 plataformas
- Botones de redes sociales funcionales (Facebook, Google, X)
- Captura de credenciales en consola y archivo (.txt)
- Proxy reverso para URLs personalizadas
- Soporte HTTPS con certificado autofirmado
- Medidas de seguridad avanzadas (subred aleatoria, hostname, TTL spoof, IPv6 off, tmpfs, machine-id random, core dumps off)
- Barra de progreso en cleanup
- Restauracion completa del sistema al salir (MAC, iptables, NetworkManager, hostname, TZ, IPv6)

## Requisitos

- Linux con kernel reciente
- hostapd, dnsmasq, iw, iptables
- Interfaz WiFi que soporte modo AP
- Python 3.6+
- Permisos de root

### Instalar dependencias

```bash
sudo apt install hostapd dnsmasq iw iptables python3 python3-pip
pip3 install -r requirements.txt
```

## Instalacion

### Local (sin sudo)

```bash
git clone https://github.com/tuusuario/BeeTrap.git
cd BeeTrap
./run.sh
```

### Sistema (acceso global)

```bash
sudo cp run.sh /usr/local/bin/beetrap
sudo chmod +x /usr/local/bin/beetrap
sudo beetrap
```

## Uso

```bash
sudo python3 beetrap.py
```

1. Elegir pagina a suplantar (Facebook, Instagram, Google, X, LinkedIn, GitHub, TikTok)
2. Configurar SSID, interfaz WiFi y puerto del proxy
3. Elegir medidas de seguridad (opcional)
4. Conectar dispositivo victima al WiFi falso
5. Las credenciales aparecen en consola y se guardan en captures/

### Modo Proxy (solo reverso)

Editar proxy.py directamente o configurar tu propio entry point.

## Estructura

```
BeeTrap/
├── beetrap.py                  # Entry point
├── run.sh                      # Shell wrapper para path fijo
├── requirements.txt
├── README.md
├── .gitignore
├── scripts/
│   └── diagnostico.sh
├── beetrap/
│   ├── __init__.py
│   ├── main.py                 # Menu y orquestacion
│   ├── access_point.py         # hostapd + dnsmasq
│   ├── firewall.py             # iptables
│   ├── proxy.py                # Proxy reverso + captive portal
│   ├── templates.py            # Paginas de login HTML (7)
│   ├── config.py               # Configuracion y PRESETS
│   ├── capture.py              # Logging de capturas
│   ├── rewrite.py              # Reescribe URLs en respuestas
│   └── stealth.py              # Medidas de seguridad avanzadas
├── credentials/                # Certificados SSL
│   ├── cert.pem
│   └── key.pem
├── captures/                   # Capturas de credenciales
│   └── credentials/
└── scripts/
    └── diagnostico.sh
```

## Medidas de seguridad

### Basicas (1)

- Cambia la MAC de la interfaz WiFi
- Bloquea movimiento lateral entre clientes
- Aisla la interfaz del honeypot
- Deshabilita logs del sistema
- Namespace de red aislado

### Identidad y ubicacion (2)

- Subred IP aleatoria cada ejecucion
- Zona horaria falsa (pais aleatorio)
- Hostname del sistema cambiado

### Huella digital de red (3)

- TTL spoofing (128 o 255)
- TCP timestamps desactivados
- IPv6 desactivado
- Vendor class DHCP aleatorio
- Tiempo de concesion DHCP variable

### Contra-analisis forense (4)

- Core dumps del kernel desactivados
- /etc/machine-id aleatorio
- /tmp y /var/log montados en tmpfs
- Limpieza de bash_history, journalctl, dmesg al salir

## Captive Portal

El proxy responde automaticamente a las verificaciones de conectividad de los
siguientes sistemas operativos:

| OS | Endpoint | Respuesta esperada |
|---|---|---|
| Android | connectivitycheck.gstatic.com/generate_204 | 302 redirect a /login |
| iOS | captive.apple.com/hotspot-detect.html | HTML con meta refresh |
| Windows | msftconnecttest.com/connecttest.txt | 302 redirect a /login |
| Firefox | detectportal.firefox.com | 302 redirect a /login |
| Debian | network-test.debian.org | 302 redirect a /login |

## Capturas

Formato: `{target}_{email}_{timestamp}.txt`

```
Tiempo: 20260601_152706
Target: accounts.google.com
IP: 10.77.195.234
Email: victima@ejemplo.com
Password: supersecreto123
```

## Solucion de problemas

**El AP no aparece**
Verificar que la interfaz soporte modo AP:
```bash
iw list | grep "AP"
```

**El dispositivo no se conecta**
Verificar que no haya procesos conflictivos:
```bash
sudo systemctl stop NetworkManager
sudo killall wpa_supplicant dnsmasq
```

**El captive portal no se abre**
Verificar reglas de iptables:
```bash
sudo iptables -t nat -L PREROUTING
```

**El proxy no responde**
Verificar que el puerto este libre:
```bash
ss -tulnp | grep 8080
```

## Creditos

Desarrollado por BloodMoney605

## Licencia

Este proyecto se distribuye con fines educativos y de auditoria de seguridad.
No me hago responsable del mal uso que se le pueda dar.
