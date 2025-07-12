# main.py

import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from app.ui import run_app

if __name__ == "__main__":
    run_app()
