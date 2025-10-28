#!/usr/bin/env python3
"""
C.H.A.R.L.O.T.T.E. MVP - Main Entry Point

Cybernetic Heuristic Assistant for Recon, Logic, Offensive Tactics, Triage & Exploitation

Usage:
    python charlotte.py
    python -m core.main
"""

import sys
from pathlib import Path

# Add project root to path
ROOT = Path(__file__).parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

if __name__ == "__main__":
    from core.main import main
    sys.exit(main())
