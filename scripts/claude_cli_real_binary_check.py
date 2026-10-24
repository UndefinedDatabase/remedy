"""Operator amendment amend1024-one-real-order, D2: one REAL call of this machine's `claude` program
through Remedy's claude-cli adapter, with the declared isolation in force.

The call is harmless: a builder with `allowed-tools` is asked to create one file in a fresh
temporary folder, and nothing else. The record names the result, the duration and the environment
the child got — names only, never a value — and is written to
`evidence/current/claude_cli_real_binary_check.json`. It costs one paid call; run it by hand:

    python3 scripts/claude_cli_real_binary_check.py
"""
from __future__ import annotations

import json
import os
import shutil
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

OUT = REPO_ROOT / "evidence" / "current" / "claude_cli_real_binary_check.json"
PROMPT = ("Create a file named hello.txt in the current directory whose only content is the line "
          "'hello from the isolated worker'. Do nothing else and do not read any other file.")


def main() -> int:
    from packages.orchestration.pingpong_provider import ClaudeCliProvider
    from packages.orchestration.worker_adapter_slot import (
        adapter_child_env,
        adapter_isolation_record,
        install_worker_adapters,
    )
    from packages.providers.adapters.adapter_registry import WORKER_ADAPTERS_BY_REF
    from packages.providers.adapters.claude_cli_reference import _ISOLATION_ENV_ALLOWLIST

    install_worker_adapters(WORKER_ADAPTERS_BY_REF)
    child_env = adapter_child_env("claude-cli") or {}
    workdir = Path(tempfile.mkdtemp(prefix="remedy-claude-check-"))
    provider = ClaudeCliProvider(cwd=str(workdir), write_mode="allowed-tools")
    started = time.monotonic()
    error = ""
    output = None
    try:
        output = provider.build(PROMPT)
    except (RuntimeError, OSError, ValueError) as exc:   # the record says what failed
        error = f"{type(exc).__name__}: {exc}"[:1000]
    seconds = round(time.monotonic() - started, 1)
    target = workdir / "hello.txt"
    created = target.read_text(encoding="utf-8").strip() if target.is_file() else None
    usage = getattr(output, "usage_actuals", None) or {}
    record = {
        "schema_v": "claude_cli_real_binary_check_v1",
        "checked_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "claude_path": shutil.which("claude"),
        "cli_version": provider._resolve_version(),
        "ok": not error and created == "hello from the isolated worker",
        "error": error,
        "seconds": seconds,
        "file_created": created is not None,
        "file_content": created,
        "tokens": {key: usage.get(key) for key in ("input_tokens", "output_tokens", "cache_read",
                                                   "cache_creation", "num_turns")},
        "isolation": adapter_isolation_record("claude-cli"),
        "env_names_passed": sorted(child_env),
        "env_names_declared": sorted(_ISOLATION_ENV_ALLOWLIST),
        "env_names_declared_but_unset_here": sorted(set(_ISOLATION_ENV_ALLOWLIST) - set(os.environ)),
        "argv_tail": provider._adapter_argv("claude", "builder", "<prompt>", "", "")[3:],
    }
    shutil.rmtree(workdir, ignore_errors=True)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({key: record[key] for key in ("ok", "error", "seconds", "file_created")}))
    return 0 if record["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
