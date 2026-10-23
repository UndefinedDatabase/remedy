"""The worker adapter slot (F315 T002, DECISION F315 D2).

Orchestration imports the worker adapter contract and never a concrete adapter (the import guard
of `tests/contracts/test_adapter_import_guard.py`). The wiring layer therefore fills this slot
once per process: `main` in `apps/cli/grouped.py` installs the adapter registry's classes before
any command runs, and `ClaudeCliProvider` asks the slot for the adapter that builds each call's
command line. Remedy deliberately keeps no second command-line builder beside the adapter, so an
empty slot is an error and never a fallback (AGENTS.md, "Replacing is deleting").
"""
from __future__ import annotations

import json
from collections.abc import Callable, Mapping
from typing import Any

from packages.contracts.adapter_contract import CliInvocation, InvocationOptions, WorkerAdapter
from packages.orchestration.token_actuals import UsageActuals, parse_cli_result_detailed

#: Adapter reference to the factory (an adapter class) the wiring layer installed for it.
_INSTALLED_WORKER_ADAPTERS: dict[str, Callable[..., WorkerAdapter]] = {}


class WorkerAdapterNotInstalled(RuntimeError):
    """A provider asked for an adapter reference the wiring layer never installed."""


# WHY: the one door through which the wiring layer hands concrete adapters to orchestration.
def install_worker_adapters(adapters: Mapping[str, Callable[..., WorkerAdapter]]) -> None:
    """Install `adapters`, each adapter reference mapped to its factory, replacing what was there."""
    _INSTALLED_WORKER_ADAPTERS.clear()
    _INSTALLED_WORKER_ADAPTERS.update(adapters)


# WHY: a provider builds the adapter for its own settings at call time, from the installed factory.
def installed_worker_adapter(adapter_ref: str, **settings: Any) -> WorkerAdapter:
    """Build the installed adapter for `adapter_ref` with `settings`; raise when none is installed."""
    factory = _INSTALLED_WORKER_ADAPTERS.get(adapter_ref)
    if factory is None:
        raise WorkerAdapterNotInstalled(
            f"no worker adapter is installed for {adapter_ref!r}; the command line installs the "
            "adapter registry before any command runs")
    return factory(**settings)


# WHY: the provider holds its schema as the compact sorted string the wire carries, and the
# contract takes the schema object, so the string is read back here; the adapter writes it
# again with the same separators and key order, which gives the same bytes.
def adapter_cli_argv(
    adapter_ref: str, role: str, prompt: str, *, model: str, json_schema: str = "",
    resume: str = "", **settings: Any,
) -> list[str]:
    """The command line the installed adapter builds for one call of `role`."""
    adapter = installed_worker_adapter(adapter_ref, **settings)
    invocation = adapter.build_invocation(role, (prompt,), InvocationOptions(
        model=model, output_schema=json.loads(json_schema) if json_schema else None,
        resume_ref=resume or None))
    if not isinstance(invocation, CliInvocation):
        raise TypeError(f"adapter {adapter_ref!r} built {type(invocation).__name__}, not a command line")
    return list(invocation.argv)


# WHY: the installed adapter maps a call's usage (DECISION F315 D3); the contract answers None
# without saying why, so only then does the shared envelope reader name the reason the
# provider records ("is_error", "usage_missing", ...).
def adapter_usage_actuals(adapter_ref: str, raw: str, **settings: Any) -> tuple[UsageActuals | None, str]:
    """The usage the installed adapter maps from `raw`, with `"ok"` or the reason it has none."""
    mapped = installed_worker_adapter(adapter_ref, **settings).map_usage(raw)
    if mapped is not None:
        return mapped.actuals, "ok"
    return None, parse_cli_result_detailed(raw)[1]
