import subprocess


GATEWAY = "10.0.66.1"
HONEY_NET = "10.0.66"


def _run(cmd, check=True):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"  [!] fallo: {cmd}")
        print(f"  [!] {result.stderr.strip()}")
    return result


def redirect_http_to_proxy(interface, proxy_port):
    _run(
        f"iptables -t nat -A PREROUTING -i {interface} -p tcp --dport 80 "
        f"-j REDIRECT --to-port {proxy_port}"
    )


def drop_https_on_interface(interface):
    _run(
        f"iptables -t nat -A PREROUTING -i {interface} -p tcp --dport 443 "
        f"-j DROP"
    )


def redirect_https_to_proxy(interface):
    _run(
        f"iptables -t nat -A PREROUTING -i {interface} -p tcp --dport 443 "
        f"-j REDIRECT --to-port 443"
    )


def block_client_to_client(interface):
    _run(
        f"iptables -I FORWARD -i {interface} -o {interface} -j DROP"
    )


def isolate_interface(interface):
    _run(
        f"iptables -A FORWARD -i {interface} ! -d {HONEY_NET}.0/24 -j DROP"
    )
    _run(
        f"iptables -A FORWARD -o {interface} ! -s {HONEY_NET}.0/24 -j DROP"
    )


def flush_all():
    _run("iptables -t nat -F", check=False)
    _run("iptables -F", check=False)
    _run("iptables -X", check=False)
