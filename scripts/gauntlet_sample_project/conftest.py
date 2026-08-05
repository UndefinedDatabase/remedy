"""Make the package importable when the suite runs from this directory.

The gauntlet materialises this project as a standalone copy and runs
``python3 -m pytest tests -q`` inside it, so the copy has to be
self-sufficient — no installed package, no PYTHONPATH from outside.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
