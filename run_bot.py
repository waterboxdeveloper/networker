#!/usr/bin/env python3

import sys
import os

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from networker_bot.main import main  # type: ignore

if __name__ == "__main__":
    main()