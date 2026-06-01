#!/usr/bin/env python3
import sys
import os

ruta = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ruta)

from beetrap.main import main

if __name__ == "__main__":
    main()
