"""The adapter registry (F151 T003, DECISION F151 D5).

Resolves a `WorkerProviderSpec`'s `adapter_ref` (`packages/orchestration/worker_adapters.py`)
to the concrete `WorkerAdapter` it names: the v1 record DESCRIBES a worker, and the v2 adapter
its reference names EXECUTES the contract for it (D5 (1)). `remedy worker show` is the product
path that reaches an adapter through this registry (D5 (3)); orchestration never imports it or
anything else under `packages/providers/adapters/` (the import guard of D5 (4)).
"""
from __future__ import annotations

from packages.contracts.adapter_contract import WorkerAdapter
from packages.providers.adapters.claude_cli_reference import ClaudeCliReferenceAdapter

# WHY: one place maps a worker spec's stable adapter_ref to the adapter class it names, so a
# caller never hard-codes a provider's adapter_ref string a second time.
WORKER_ADAPTERS_BY_REF: dict[str, type[WorkerAdapter]] = {
    "claude-cli": ClaudeCliReferenceAdapter,
}


def resolve_worker_adapter(adapter_ref: str) -> WorkerAdapter | None:
    """Return a default-constructed adapter for `adapter_ref`, or None for an unknown or empty one."""
    adapter_cls = WORKER_ADAPTERS_BY_REF.get(adapter_ref)
    if adapter_cls is None:
        return None
    return adapter_cls()
