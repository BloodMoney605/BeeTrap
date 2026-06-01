#!/bin/bash
ORIGEN="$(readlink -f "${BASH_SOURCE[0]}")"
RUTA="$(cd "$(dirname "$ORIGEN")" && pwd)"
cd "$RUTA" || { echo "Error: no se encuentra BeeTrap en $RUTA"; exit 1; }
exec python3 beetrap.py "$@"
