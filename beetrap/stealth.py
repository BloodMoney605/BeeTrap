import os
import sys
import time
import random
import subprocess
import string


def _comando(cmd, check=True):
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
        if check and r.returncode != 0:
            print(f"  [!] fallo: {cmd}")
            print(f"  [!] {r.stderr.strip()}")
        return r
    except (subprocess.TimeoutExpired, KeyboardInterrupt):
        return subprocess.CompletedProcess(args=cmd, returncode=-1, stdout="", stderr="")


def _id_aleatorio(longitud=8):
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=longitud))


def zona_horaria_falsa(guardar_en=None):
    husos = [
        "Asia/Tokyo", "Asia/Shanghai", "Asia/Dubai", "Asia/Kolkata",
        "Europe/Moscow", "Europe/Berlin", "Europe/London", "Europe/Paris",
        "America/New_York", "America/Chicago", "America/Denver",
        "America/Los_Angeles", "America/Sao_Paulo", "America/Argentina/Buenos_Aires",
        "Africa/Cairo", "Africa/Lagos", "Australia/Sydney", "Pacific/Auckland",
    ]
    original = _comando("timedatectl show --property=Timezone --value 2>/dev/null", check=False).stdout.strip()
    if guardar_en is not None:
        guardar_en.append(original or "UTC")

    elegida = random.choice([h for h in husos if h != original])
    _comando(f"timedatectl set-timezone {elegida} 2>/dev/null || ln -sf /usr/share/zoneinfo/{elegida} /etc/localtime", check=False)
    print(f"      zona horaria: {elegida}")


def restaurar_zona_horaria(zona):
    if zona:
        _comando(f"timedatectl set-timezone {zona} 2>/dev/null || ln -sf /usr/share/zoneinfo/{zona} /etc/localtime", check=False)


def hostname_aleatorio(guardar_en=None):
    original = _comando("hostname", check=False).stdout.strip()
    if guardar_en is not None:
        guardar_en.append(original)

    prefijos = ["thinkpad", "latitude", "optiplex", "inspiron", "macbook",
                 "surface", "galaxy", "nexus", "pixel", "oneplus",
                 "vivo", "xiaomi", "redmi", "hp", "lenovo", "asus"]
    prefijo = random.choice(prefijos)
    sufijo = _id_aleatorio(4)
    nuevo = f"{prefijo}-{sufijo}"

    _comando(f"hostname {nuevo}", check=False)
    _comando(f"echo {nuevo} > /proc/sys/kernel/hostname", check=False)
    print(f"      hostname: {nuevo}")


def restaurar_hostname(hostname):
    if hostname:
        _comando(f"hostname {hostname}", check=False)
        _comando(f"echo {hostname} > /proc/sys/kernel/hostname", check=False)


def subred_aleatoria():
    segundo = random.randint(1, 254)
    tercero = 0
    while True:
        tercero = random.randint(1, 254)
        if tercero != 66:
            break
    return {
        "net": f"10.{segundo}.{tercero}",
        "gw": f"10.{segundo}.{tercero}.1",
        "start": f"10.{segundo}.{tercero}.10",
        "end": f"10.{segundo}.{tercero}.250",
    }


def ttl_spoof(iface):
    ttl = random.choice([128, 255])
    _comando(f"iptables -t mangle -A POSTROUTING -o {iface} -j TTL --ttl-set {ttl}", check=False)
    print(f"      TTL: {ttl}")


def tcp_timestamps_off():
    _comando("sysctl -w net.ipv4.tcp_timestamps=0 2>/dev/null", check=False)
    print("      TCP timestamps: off")


def ipv6_off():
    _comando("sysctl -w net.ipv6.conf.all.disable_ipv6=1 2>/dev/null", check=False)
    _comando("sysctl -w net.ipv6.conf.default.disable_ipv6=1 2>/dev/null", check=False)
    print("      IPv6: desactivado")


def restaurar_ipv6():
    _comando("sysctl -w net.ipv6.conf.all.disable_ipv6=0 2>/dev/null", check=False)
    _comando("sysctl -w net.ipv6.conf.default.disable_ipv6=0 2>/dev/null", check=False)


def core_dumps_off():
    _comando("ulimit -c 0 2>/dev/null", check=False)
    _comando("sysctl -w kernel.core_pattern=/dev/null 2>/dev/null", check=False)
    print("      core dumps: off")


def machine_id_random(guardar_en=None):
    original = ""
    if os.path.exists("/etc/machine-id"):
        with open("/etc/machine-id") as f:
            original = f.read().strip()
        if guardar_en is not None:
            guardar_en.append(original)
        nuevo = _id_aleatorio(32)
        _comando(f"echo {nuevo} > /etc/machine-id 2>/dev/null", check=False)
        print("      machine-id: randomizado")


def restaurar_machine_id(mid):
    if mid:
        _comando(f"echo {mid} > /etc/machine-id 2>/dev/null", check=False)


def tmpfs_montar():
    _comando("mount -t tmpfs tmpfs /tmp -o size=256M 2>/dev/null", check=False)
    _comando("mount -t tmpfs tmpfs /var/log -o size=128M 2>/dev/null", check=False)
    print("      /tmp y /var/log: tmpfs")


def limpiar_historial():
    _comando("> ~/.bash_history 2>/dev/null", check=False)
    _comando("> ~/.zsh_history 2>/dev/null", check=False)
    _comando("history -c 2>/dev/null", check=False)
    _comando("dmesg -c 2>/dev/null", check=False)
    _comando("journalctl --rotate 2>/dev/null", check=False)
    _comando("journalctl --vacuum-time=1s 2>/dev/null", check=False)
    _comando("rm -rf /var/log/*.log /var/log/*.gz /var/log/syslog* 2>/dev/null", check=False)


def dhcp_lease_variable():
    minutos = random.randint(30, 1440)
    return f"{minutos}m"


def dhcp_vendor_random():
    vendors = [
        "MSFT 5.0", "MSFT 98", "udhcp 1.30", "dhcpcd-5.5.6",
        "Android-10", "Android-11", "Android-12", "Android-13",
        "iOS-17.0", "iOS-16.0", "iOS-15.0",
        "Linux 6.1.0", "Linux 5.15.0", "Linux 6.5.0",
        "Windows 10.0.19045", "Windows 10.0.22631",
    ]
    return random.choice(vendors)
