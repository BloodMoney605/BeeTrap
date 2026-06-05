import subprocess


TRAP_NET = "10.0.66"


def _run(cmd, check=True):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"  [!] fallo: {cmd}")
        print(f"  [!] {result.stderr.strip()}")
    return result


def verificar_iptables():
    result = _run("iptables -t nat -L -n 2>/dev/null", check=False)
    return result.returncode == 0


def redirect_http_to_proxy(interface, proxy_port):
    if not verificar_iptables():
        print("  [!] iptables no disponible. Usar puerto 80 para evitar iptables.")
        return
    _run(
        f"iptables -t nat -A PREROUTING -i {interface} -p tcp --dport 80 "
        f"-j REDIRECT --to-port {proxy_port}"
    )


def block_client_to_client(interface):
    if not verificar_iptables():
        return
    _run(
        f"iptables -I FORWARD -i {interface} -o {interface} -j DROP"
    )


def isolate_interface(interface):
    if not verificar_iptables():
        return
    _run(
        f"iptables -A FORWARD -i {interface} ! -d {TRAP_NET}.0/24 -j DROP"
    )
    _run(
        f"iptables -A FORWARD -o {interface} ! -s {TRAP_NET}.0/24 -j DROP"
    )


def flush_all():
    _run("iptables -t nat -F", check=False)
    _run("iptables -F", check=False)
    _run("iptables -X", check=False)
