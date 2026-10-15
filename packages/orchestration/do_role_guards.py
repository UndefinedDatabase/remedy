"""Two refusals `remedy do` makes before any step (operator amendment amend1014b, D1 and D5)."""
from __future__ import annotations

from pathlib import Path


def non_writing_provider_refusal(role: str, provider: str) -> str:
    """The refusal sentence for a raw Ollama builder or repair provider, else "" (D1).

    A raw Ollama call returns text, not a change, so it may not be a mutating role's provider;
    Pi is the local agentic one. It is never silently read as Pi.
    """
    if provider != "ollama" or role not in ("builder", "repair"):
        return ""
    return (f"--{role}-provider ollama cannot write files: a raw Ollama call returns text, not a "
            f"change. Use --{role}-provider pi, the local agentic provider (Pi plus the same "
            f"Ollama model), or omit the flag. Nothing was run.")


def unrepresentable_baseline(repo_path: str | Path) -> str:
    """"" when the target's working tree can be captured, else the one sentence saying why not.

    A dirty tree is never the reason: dirt is the baseline. Used to refuse a run before any step.
    """
    from packages.orchestration.dirty_baseline import DirtyBaselineUnsupported, capture_dirty_baseline

    try:
        capture_dirty_baseline(repo_path)
    except DirtyBaselineUnsupported as exc:
        return str(exc)
    return ""
