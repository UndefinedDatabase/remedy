"""Make the package importable when the suite runs from this directory.

The bench materialises this project as a standalone copy and runs its suite
inside it, so the copy has to be self-sufficient — no installed package.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
