"""Concrete worker adapters (F151 T003): one module per provider, each wrapping that
provider's existing call path instead of re-implementing it. Orchestration never imports
anything from this package; only a future registry linkage and each adapter's own tests do.
"""
from __future__ import annotations
