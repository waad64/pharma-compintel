#!/usr/bin/env python
"""
PCI Dashboard - Main Entry Point
Pharmaceutical Competitive Intelligence Application
"""

import subprocess
import sys
import os

if __name__ == "__main__":
    # Get the directory of this script
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    
    # Run streamlit with the main app
    subprocess.run([
        sys.executable, "-m", "streamlit", "run",
        os.path.join(BASE_DIR, "src", "app", "main.py")
    ])
