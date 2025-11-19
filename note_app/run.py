#!/usr/bin/env python3
"""
Launcher script for the Ultimate Note Taking App.
"""

import sys
import os

# Add the current directory to the path to import modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import main

if __name__ == "__main__":
    main()