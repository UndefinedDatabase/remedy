"""F289 R1 G3 — parity tool: `_cmd_doctor_core`'s output is byte-identical before
and after doctor_core_report() (DECISION F289 D1, T5_F289.md T002, S5).

Takes two tree paths (the base checkout at `d0239fa3` and the round's tree at
C4) and, for EACH tree, runs five scenarios in a fresh `python3 -B` subprocess
whose working directory is that tree, calling `_cmd_doctor_core` once with
`json=True` and once with `json=False` and capturing stdout. Every `REMEDY_`
variable is removed from the child's environment except those a scenario
itself sets, and `packages.orchestration.budget_guard.FREE_DISK_PROBE` is
patched to a constant so the free-disk figure cannot differ between runs.

Prints one line per scenario and mode with both trees' sha256 and whether they
are equal, and a final line `PARITY: <bool>`.

Usage:
    python3 -B f289-r1-parity.py <base_tree> <par_tree>
"""
from __future__ import annotations

import hashlib
import os
import subprocess
import sys

#: Executed in a fresh child process, cwd = the tree under test. Reads which
#: scenario and json mode to run from its own environment, patches exactly what
#: that scenario names, and calls `_cmd_doctor_core` — whose stdout the PARENT
#: process captures untouched.
_CHILD_SCRIPT = r'''
import argparse
import os
import tempfile
from pathlib import Path

import packages.orchestration.budget_guard as budget_guard
import packages.orchestration.config as config_mod
import packages.orchestration.dead_model_list as dead_model_list
from apps.cli.commands import worker_facade_cmd

# Fixed across every scenario and both trees, so the free-disk figure itself
# can never be the reason two runs differ.
budget_guard.FREE_DISK_PROBE = lambda: 123456789


class _FakeConfig:
    """Only `get` -- the one accessor the doctor uses on RemedyConfig."""

    def __init__(self, values):
        self._values = values

    def get(self, key):
        return self._values.get(key)


scenario = os.environ["F289_PARITY_SCENARIO"]
json_mode = os.environ["F289_PARITY_JSON"] == "1"

if scenario == "a":
    pass  # as shipped
elif scenario == "b":
    from packages.orchestration.dead_model_list import DeadModelEntry
    from packages.orchestration.model_aliases import resolve_model_alias

    model_id = resolve_model_alias("claude-flagship")
    entries = (DeadModelEntry(id=model_id, reason="retired by the provider", superseded_by=""),)
    dead_ids = frozenset({model_id, "dead-configured-id"})
    dead_model_list.load_dead_models = lambda path=None: entries
    dead_model_list.dead_model_ids = lambda path=None: dead_ids
    config_mod.get_config = lambda: _FakeConfig({"orchestrator.model": "dead-configured-id"})
elif scenario == "c":
    pass  # REMEDY_ZZ_NOT_A_SETTING and REMEDY_UI_PORT are set by the parent's env
elif scenario == "d":
    def _boom(path=None):
        raise dead_model_list.DeadModelListError("dead_models.json: unreadable")
    dead_model_list.load_dead_models = _boom
    dead_model_list.dead_model_ids = _boom
elif scenario == "e":
    empty_dir = tempfile.mkdtemp()
    worker_facade_cmd.remedy_scripts_dir = lambda: Path(empty_dir)
else:
    raise SystemExit(f"unknown scenario {scenario!r}")

ns = argparse.Namespace(json=json_mode)
worker_facade_cmd._cmd_doctor_core(ns)
'''

#: One entry per scenario: its label, and the extra `REMEDY_` variables (only)
#: it sets. Every scenario removes every OTHER `REMEDY_` variable first.
_SCENARIOS: tuple[tuple[str, dict[str, str]], ...] = (
    ("a_as_shipped", {}),
    ("b_dead_model_and_configured_id", {}),
    ("c_unknown_and_unparsable_env_variable", {
        "REMEDY_ZZ_NOT_A_SETTING": "1",
        "REMEDY_UI_PORT": "eighty-secret",
    }),
    ("d_dead_model_loaders_raise", {}),
    ("e_empty_scripts_dir", {}),
)


def _scenario_letter(label: str) -> str:
    return label.split("_", 1)[0]


def _child_env(extra_remedy_vars: dict[str, str], scenario_letter: str, json_mode: bool) -> dict[str, str]:
    """The base environment, every `REMEDY_` variable stripped, plus this scenario's own."""
    env = {k: v for k, v in os.environ.items() if not k.startswith("REMEDY_")}
    env.update(extra_remedy_vars)
    env["F289_PARITY_SCENARIO"] = scenario_letter
    env["F289_PARITY_JSON"] = "1" if json_mode else "0"
    return env


def _run(tree: str, scenario_letter: str, extra_remedy_vars: dict[str, str], json_mode: bool) -> bytes:
    env = _child_env(extra_remedy_vars, scenario_letter, json_mode)
    result = subprocess.run(
        [sys.executable, "-B", "-c", _CHILD_SCRIPT],
        cwd=tree,
        env=env,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"child failed in {tree!r} scenario {scenario_letter!r} json={json_mode}: "
            f"exit {result.returncode}\nstdout={result.stdout!r}\nstderr={result.stderr!r}"
        )
    return result.stdout


def main(base_tree: str, par_tree: str) -> bool:
    all_equal = True
    for label, extra in _SCENARIOS:
        letter = _scenario_letter(label)
        for json_mode in (True, False):
            base_out = _run(base_tree, letter, extra, json_mode)
            par_out = _run(par_tree, letter, extra, json_mode)
            base_hash = hashlib.sha256(base_out).hexdigest()
            par_hash = hashlib.sha256(par_out).hexdigest()
            equal = base_hash == par_hash
            all_equal = all_equal and equal
            mode_word = "json" if json_mode else "text"
            print(f"{label} {mode_word}: base={base_hash} par={par_hash} equal={equal}")
    print(f"PARITY: {all_equal}")
    return all_equal


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("usage: f289-r1-parity.py <base_tree> <par_tree>")
    ok = main(sys.argv[1], sys.argv[2])
    raise SystemExit(0 if ok else 1)
