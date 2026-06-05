#!/bin/bash
set -e

if [ "$EUID" -ne 0 ]; then
    echo "Ejecutar con sudo: sudo bash install.sh"
    exit 1
fi

echo "Instalando BeeTrap..."
echo

echo "[1/5] Instalando dependencias del sistema..."
apt-get update -qq
apt-get install -y -qq hostapd dnsmasq iw iptables tor python3 python3-pip openssl 2>/dev/null
echo "  OK"

echo "[2/5] Instalando dependencias Python..."
pip3 install -q -r requirements.txt 2>/dev/null || pip3 install requests[socks] 2>/dev/null
echo "  OK"

echo "[3/5] Generando certificado SSL..."
mkdir -p credentials
if [ ! -f credentials/cert.pem ]; then
    openssl req -x509 -newkey rsa:2048 -keyout credentials/key.pem \
        -out credentials/cert.pem -days 365 -nodes \
        -subj "/CN=beetrap" 2>/dev/null
    echo "  OK"
else
    echo "  ya existe"
fi

echo "[4/5] Instalando comando global..."
cp run.sh /usr/local/bin/beetrap
chmod +x /usr/local/bin/beetrap
echo "  OK"

echo "[5/5] Verificando..."
python3 -c "from beetrap.main import main" 2>/dev/null && echo "  instalacion correcta" || echo "  error en la instalacion"

echo
echo "BeeTrap instalado. Ejecutar:"
echo "  sudo beetrap"
echo
