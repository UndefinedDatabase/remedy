"""Shared prompt facts for structured provider calls.

Extracted from ``flight_plan._cheap_repo_facts`` (F069): the mission compiler
needs the same cheap "what does this repo look like" block the flight planner
puts in front of its provider, and a SECOND copy of it would be two answers to
one question — the one thing the feature file's Orchestrator brief forbids.

Deliberately cheap: a single directory listing, capped, never recursive. A
prompt-facts helper that walks a repository is a helper that makes every
provider call slow and every prompt expensive, so this one does not.
"""
from __future__ import annotations

import os

#: How many names of each kind travel in a prompt. Facts are context, not an
#: inventory — past this point they cost tokens without changing the answer.
MAX_FACT_ENTRIES = 20


def repo_facts_block(root: str | None = None) -> str:
    """The top-level shape of ``root`` (default: the working directory).

    Returns prompt-ready lines, or an honest placeholder — never a partial
    listing presented as a whole one. Hidden entries are omitted: a provider
    reasoning about ``.git`` or ``.venv`` is reasoning about the wrong thing.
    """
    lines: list[str] = []
    cwd = root or os.getcwd()
    try:
        entries = sorted(os.listdir(cwd))
        dirs = [e for e in entries if os.path.isdir(os.path.join(cwd, e))
                and not e.startswith(".")]
        files = [e for e in entries if os.path.isfile(os.path.join(cwd, e))
                 and not e.startswith(".")]
        if dirs:
            lines.append(f"Top-level dirs: {', '.join(dirs[:MAX_FACT_ENTRIES])}")
        if files:
            lines.append(f"Top-level files: {', '.join(files[:MAX_FACT_ENTRIES])}")
    except OSError:
        lines.append("(repo listing unavailable)")
    return "\n".join(lines) if lines else "(no repo facts available)"
