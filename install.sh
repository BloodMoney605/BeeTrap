#!/bin/bash

if [ "$EUID" -ne 0 ]; then
    echo "Ejecutar con sudo: sudo bash install.sh"
    exit 1
fi

echo "Instalando BeeTrap..."
echo

echo "[1/5] Instalando dependencias del sistema..."
apt-get update
apt-get install -y hostapd dnsmasq iw iptables tor python3 python3-pip openssl git
echo ""

echo "[2/5] Instalando dependencias Python..."
pip3 install requests[socks]
echo ""

echo "[3/5] Generando certificado SSL..."
mkdir -p credentials
if [ ! -f credentials/cert.pem ]; then
    openssl req -x509 -newkey rsa:2048 -keyout credentials/key.pem \
        -out credentials/cert.pem -days 365 -nodes \
        -subj "/CN=beetrap"
fi
echo "  OK"
echo ""

echo "[4/5] Instalando comando global..."
rm -f /usr/local/bin/beetrap
ln -s "$(pwd)/run.sh" /usr/local/bin/beetrap
echo "  OK"
echo ""

echo "[5/5] Verificando..."
python3 -c "from beetrap.main import main" && echo "  instalacion correcta"
echo ""

echo "BeeTrap instalado. Ejecutar:"
echo "  sudo beetrap"
echo ""
