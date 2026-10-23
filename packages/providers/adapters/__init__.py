"""Concrete worker adapters (F151 T003): one module per provider, each wrapping that
provider's existing call path instead of re-implementing it. Orchestration never imports
anything from this package; its own registry (`adapter_registry.py`), the wiring layer under
`apps/` that `remedy worker show` runs through, and each adapter's own tests do.
"""
from __future__ import annotations
