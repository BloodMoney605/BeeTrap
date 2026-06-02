#!/bin/bash
echo "BeeTrap - Diagnostico"
echo

echo "herramientas:"
which hostapd >/dev/null && echo "  [OK] hostapd" || echo "  [FAIL] hostapd"
which dnsmasq >/dev/null && echo "  [OK] dnsmasq" || echo "  [FAIL] dnsmasq"
which iw >/dev/null && echo "  [OK] iw" || echo "  [FAIL] iw"
which iptables >/dev/null && echo "  [OK] iptables" || echo "  [FAIL] iptables"
echo

IFACE=$(iw dev 2>/dev/null | grep Interface | awk '{print $2}')
echo "interfaz WiFi detectada: ${IFACE:-ninguna}"
echo

if [ -n "$IFACE" ]; then
  iw list 2>/dev/null | grep -q "AP" && echo "  [OK] modo AP soportado" || echo "  [FAIL] modo AP no soportado"
  echo "  canal $(iw dev $IFACE info 2>/dev/null | grep channel | awk '{print $2}')"
fi
echo

echo "procesos actuales:"
pgrep -x hostapd >/dev/null && echo "  hostapd: activo" || echo "  hostapd: detenido"
pgrep -x dnsmasq >/dev/null && echo "  dnsmasq: activo" || echo "  dnsmasq: detenido"
echo

echo "reglas iptables activas:"
iptables -t nat -L PREROUTING -n 2>/dev/null | grep REDIRECT | head -3 || echo "  ninguna"
echo

echo "certificados:"
ls -l "$(dirname "$0")/../credentials/" 2>/dev/null || echo "  no encontrados"
